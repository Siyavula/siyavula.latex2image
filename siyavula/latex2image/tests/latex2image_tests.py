# coding=utf-8
from unittest import TestCase
from lxml import etree, html

from siyavula.latex2image.imageutils import replace_latex_with_images


class TestBaseEquationToImageConversion(TestCase):
    """Test the equation to image conversion."""

    def setUp(self):
        self.element_input = etree.Element('xml')
        self.div_input = etree.SubElement(self.element_input, 'div')
        self.div_input.set('class', 'latex-math')

    def test_complex_equation_to_png(self):
        self.div_input.text = u'\\(\\begin{{aligned}} \\vec{{F}}_{{g}} & = m\\vec{{g}} \\\\ & = (\\text{{12,7}}\\ \\text{{kg}})(\\text{{9,8}}\\ \\text{{m·s$^{{-2}}$}}) \\\\ & = \\text{{124,46}}\\ \\text{{N}}\\text{{&#181; µ &#956; μ}} &#181; µ &#956; μ \\end{{aligned}}\\'.replace('{{', '{').replace('}}', '}')
        xml = html.tostring(replace_latex_with_images(self.element_input, 'latex-math', '', ''))
        self.assertEqual(xml, '<xml><div class="latex-math"><a href="/8996d7eee5c41cdf08aa8c0e9fe42e93.png"><img src="/8996d7eee5c41cdf08aa8c0e9fe42e93.png" srcset="/b0791f40d3207d55907aa0b7df78ca1e.png 2x"></a></div></xml>')
