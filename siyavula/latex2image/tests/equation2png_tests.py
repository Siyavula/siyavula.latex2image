from unittest import TestCase

from siyavula.latex2image.equation2png import equation2png
from siyavula.latex2image.utils import unescape

class TestBaseEquationConversion(TestCase):
    '''
    Tests the equation converter
    '''
    
    def setUp(self):
        self.equation_element = r'''\[\begin{{array}}{{rcc}}
        5x &amp; = 5y + 7 &amp; \text{{here}} \\[2pt]
        &amp; = 7 &amp;
        \end{{array}}
        \]'''
    
    def test_replace_delimiters(self):
        output_string = r'''\[\begin{{array}}{{rcc}}
        5x &amp; = 5y + 7 &amp; \text{{here}} \\[2pt]
        &amp; = 7 &amp;
        \end{{array}}
        \]'''
        assert equation2png(self.equation_element) == output_string

class TestUnicodeEquations(TestCase):
    '''Tests that unicode in equations is handled correctly'''
    def test_replace_quote_marks(self):
        input_string = r'\(&#8220;text&#8221;\)'
        output_string = u'\\(\u201ctext\u201d\\)'
        assert unescape(input_string) == output_string
