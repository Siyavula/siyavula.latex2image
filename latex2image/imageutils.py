"""
This module contains functions that does convertion of code and equations to
PDF and png formats

"""

from __future__ import print_function
import os
import sys
import errno
import shutil

from termcolor import colored

from . import pstikz2png
from .pstikz2png import LatexPictureError
from . import utils


def cleanup_after_latex(figpath):
    ''' clean up after the image generation
    '''
    tmpdir = os.path.dirname(figpath)
    try:
        shutil.rmtree(tmpdir)
    except OSError as exc:
        if exc.errno != errno.ENOENT:  # ENOENT - no such file or directory
            raise  # re-raise exception


def run_latex(pictype, codehash, codetext, cachepath, dpi=300):
    ''' Run the image generation for pstricks and tikz images
    '''
    # copy to local image cache in .bookbuilder/images
    image_cache_path = os.path.join(cachepath,
                                    pictype,
                                    codehash+'.png')
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
                figpath = pstikz2png.pspicture2png(codetext, iDpi=dpi)
            elif pictype == 'tikzpicture':
                figpath = pstikz2png.tikzpicture2png(codetext, iDpi=dpi)
            elif pictype == 'equation':
                figpath = pstikz2png.equation2png(codetext, iDpi=dpi)

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
