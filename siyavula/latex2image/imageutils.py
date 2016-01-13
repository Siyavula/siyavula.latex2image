"""
This module contains functions that does convertion of code and equations to
PDF and png formats

"""

from __future__ import print_function
import logging
import errno
import hashlib
import lxml
import os
import shutil
import sys

from termcolor import colored

from . import pstikz2png
from .pstikz2png import LatexPictureError
from . import utils

log = logging.getLogger(__name__)


def cleanup_after_latex(figpath):
    ''' clean up after the image generation
    '''
    tmpdir = os.path.dirname(figpath)
    try:
        shutil.rmtree(tmpdir)
    except OSError as exc:
        if exc.errno != errno.ENOENT:  # ENOENT - no such file or directory
            raise  # re-raise exception


def run_latex(pictype, codehash, codetext, cachepath, dpi=300,
              pdflatexpath=None):
    ''' Run the image generation for pstricks and tikz images
    '''

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
        # send this object to pstikz2png
        try:
            if pictype == 'pspicture':
                figpath = pstikz2png.pspicture2png(codetext, iDpi=dpi, pdflatexpath=pdflatexpath)
            elif pictype == 'tikzpicture':
                figpath = pstikz2png.tikzpicture2png(codetext, iDpi=dpi, pdflatexpath=pdflatexpath)
            elif pictype == 'equation':
                figpath = pstikz2png.equation2png(codetext, iDpi=dpi, pdflatexpath=pdflatexpath)

        except LatexPictureError as lpe:
            print(colored("\nLaTeX failure", "red"))
            print(unicode(lpe))
            return None

        if figpath:
            # done. copy to image cache
            utils.copy_if_newer(figpath, image_cache_path)
            # copy the pdf also but run pdfcrop first
            utils.copy_if_newer(figpath.replace('.png', '.pdf'),
                                image_cache_path.replace('.png', '.pdf'))

            cleanup_after_latex(figpath)
    else:
        figpath = image_cache_path

    sys.stdout.flush()
    return image_cache_path


def replace_latex_with_images(xml_dom, class_to_replace, cache_path, image_path):
    '''
    This will take an xml_dom and look for all instances of a certain class that will
    then be modified to have a rendered image in place instead of a mathjax equation (which
    can't render on devices without javascript).

    Parameters:
    xml_dom:          This is an xml structure that, when rendered as a string, should produce an
                      HTML page
    class_to_replace: This is the class to look out for, whose latex content will be replace
                      by an image
    cache_path:       This is the path where the images will be saved
    image_path:       This is the URL by which the stored image can be retrieved
    '''
    for equation in xml_dom.findall('.//*[@class="{}"]'.format(class_to_replace)):
        # strip any tags found inside this element
        while len(equation) > 0:
            child = equation[0]
            lxml.etree.strip_tags(equation, child.tag)

        latex = equation.text.strip().encode('utf-8')
        latex = latex.replace("\xe2\x88\x92", '-')
        latex = latex.replace("\xc3\x97", r'\times')
        latex = latex.replace("\xc2\xa0", ' ')
        latex = latex.replace("\xce\xa9", r'\ensuremath{\Omega}')
        latex = latex.replace("\xc2\xb0", r'\text{$^\circ$}')

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
        equation.append(img)
