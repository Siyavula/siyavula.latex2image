"""This module converts code and equations to PDF and/or png formats."""

from __future__ import print_function
import logging
import errno
import hashlib
import lxml
import os
import shutil
import sys
import tempfile
import subprocess

from termcolor import colored

from preambles import PsPicture_preamble, tikz_preamble, equation_preamble
from pstikz2png import tikzpicture2png, pspicture2png
from equation2png import equation2png
from utils import copy_if_newer, unescape, cleanup_code, unicode_replacements

log = logging.getLogger(__name__)


def execute(args):
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return stdout, stderr


class LatexPictureError(Exception):
    """Special Error around generating a Latex image."""

    pass


def latex2png(picture_element, preamble, return_eps=False, page_width_px=None,
              dpi=150, included_files={}, pdflatexpath=None):
    """
    Create a PNG image from latex.

    Inputs:

      pspicture_element - etree.Element

      preamble - which preamble to use, one of PsPicture_preamble, tikzpicture_preamble
      or equation_preamble

      return_eps - whether to also return the intermediate EPS file

      page_width_px - page width in pixels, used to scale the
        style:width attribute in the element.

      dpi - Will be used only if the width of the figure relative to
        the page width was not set (or the page width in pixels was not
        passed as an argument).

    Outputs:

    One or two paths, the first to the PNG, the second to the EPS.
    """
    temp_dir = tempfile.mkdtemp()
    latex_path = os.path.join(temp_dir, 'figure.tex')
    png_path = os.path.join(temp_dir, 'figure.png')
    pdf_path = os.path.join(temp_dir, 'figure.pdf')

    # can send the raw string code or a <pre> element with <code> child
    if isinstance(picture_element, (str, unicode)):
        code = picture_element
        code = cleanup_code(code)
    else:
        code = picture_element.find('.//code').text.encode('utf-8')
    code = code.replace(r'&amp;', '&').replace(r'&gt;', '>').replace(r'&lt;', '<')

    if not code:
        raise ValueError("Code cannot be empty.")

    with open(latex_path, 'wt') as fp:
        temp = unescape(preamble.replace('__CODE__', code.strip()))
        try:
            fp.write(temp)
        except UnicodeEncodeError:
            fp.write(temp.encode('utf-8'))

    for path, path_file in included_files.iteritems():
        try:
            os.makedirs(os.path.join(temp_dir, os.path.dirname(path)))
        except OSError:
            # Catch exception if path already exists
            pass
        with open(os.path.join(temp_dir, path), 'wb') as fp:
            fp.write(path_file.read())

    if not pdflatexpath:
        raise ValueError("pdflatexpath cannot be None")

    errorLog, temp = execute([pdflatexpath,
                              "-shell-escape", "-halt-on-error",
                              "-output-directory", temp_dir, latex_path])
    try:
        open(pdf_path, "rb")
    except IOError:
        raise LatexPictureError(
            "LaTeX failed to compile the image. %s \n%s" % (
                latex_path, preamble.replace('__CODE__', code.strip())))

    # crop the pdf image too
    # execute(['pdfcrop', '--margins', '1', pdfPath, pdfPath])

    execute(['convert', '-density', '%i' % dpi, pdf_path, png_path])

    return png_path


def cleanup_after_latex(figpath):
    """Clean up after the image generation."""
    tmpdir = os.path.dirname(figpath)
    try:
        shutil.rmtree(tmpdir)
    except OSError as exc:
        if exc.errno != errno.ENOENT:  # ENOENT - no such file or directory
            raise  # re-raise exception


def run_latex(pictype, codehash, codetext, cachepath, dpi=300, pdflatexpath=None):
    """Run the image generation for pstricks and tikz images."""
    # try and find pdflatex
    if pdflatexpath is None:
        path = os.environ.get('LATEX_PATH', os.environ.get('PATH'))
        texpath = [p for p in path.split(':') if 'tex' in p]
        if texpath:
            pdflatexpath = texpath[0] + '/pdflatex'
        else:
            # no custom latex installed. Try /usr/local/bin and /usr/local
            for path in ['/usr/local/bin/', '/usr/bin/']:
                texpath = os.path.join(path, 'pdflatex')
                if os.path.exists(texpath):
                    pdflatexpath = texpath
                    break

    # copy to local image cache in .bookbuilder/images
    image_cache_path = os.path.join(cachepath, pictype, codehash + '.png')
    rendered = False
    # skip image generation if it exists
    if os.path.exists(image_cache_path):
        rendered = True
        sys.stdout.write('s')

    if not rendered:
        sys.stdout.write('.')
        if pictype == 'pspicture':
            latex_code = pspicture2png(codetext)
            preamble = PsPicture_preamble()
        elif pictype == 'tikzpicture':
            latex_code = tikzpicture2png(codetext)
            preamble = tikz_preamble()
        elif pictype == 'equation':
            latex_code = equation2png(codetext)
            preamble = equation_preamble()
        try:
            figpath = latex2png(latex_code, preamble, dpi=dpi, pdflatexpath=pdflatexpath)
        except LatexPictureError as lpe:
            print(colored("\nLaTeX failure", "red"))
            print(unicode(lpe))
            return None

        if figpath:
            # done. copy to image cache
            copy_if_newer(figpath, image_cache_path)
            # copy the pdf also but run pdfcrop first
            copy_if_newer(figpath.replace('.png', '.pdf'),
                          image_cache_path.replace('.png', '.pdf'))

            cleanup_after_latex(figpath)
    else:
        figpath = image_cache_path

    sys.stdout.flush()
    return image_cache_path


def replace_latex_with_images(xml_dom, class_to_replace, cache_path, image_path):
    """
    Replace images in latex with actual image data rather than the source latex.

    This will take an xml_dom and look for all instances of a certain class that will
    then be modified to have a rendered image in place instead of a mathjax equation (which
    can't render on devices without javascript).

    Parameters:
    xml_dom:          This is an xml structure that, when rendered as a string, should produce an
                      HTML page
    class_to_replace: This is the class to look out for, whose latex content will be replace
                      by an image
    cache_path:       This is the path where the images will be saved
    image_path:       This is the host part of the url for the image
    """
    for equation in xml_dom.findall('.//*[@class="{}"]'.format(class_to_replace)):
        # strip any tags found inside this element
        while len(equation) > 0:
            child = equation[0]
            lxml.etree.strip_tags(equation, child.tag)

        latex = equation.text.strip().encode('utf-8')
        latex = unicode_replacements(latex)

        codehash = hashlib.md5(latex).hexdigest()
        try:
            run_latex('equation', codehash, latex, cache_path)
        except Exception as E:
            log.warn(
                "Failed to generate png for equation: {}\n\nException: {}\n\n"
                "Original Element: {}".format(latex, E, lxml.etree.tostring(equation)))

        # imagepath contains contains the path the created image
        # put a new img element inside the parent element
        equation.text = ''
        img = lxml.etree.Element('img')
        img.attrib['src'] = '{}/{}.png'.format(image_path, codehash)
        if equation.tag == 'div':
            a_tag = lxml.etree.SubElement(equation, 'a',
                                          {'href': '{}/{}.png'.format(image_path, codehash),
                                           'class': 'sv-action-image'})
            image_span = lxml.etree.SubElement(a_tag, 'span', {'class': 'sv-action-image__media'})
            image_span.append(img)
        else:
            equation.append(img)
