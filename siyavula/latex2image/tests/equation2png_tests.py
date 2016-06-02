# coding=utf-8
from unittest import TestCase

from siyavula.latex2image.equation2png import equation2png
from siyavula.latex2image.utils import unescape, unicode_replacements

class TestBaseEquationConversion(TestCase):
    '''
    Tests the equation converter
    '''
    def test_replace_block_delimiters(self):
        input_string = r'''\[\begin{{array}}{{rcc}}
        5x &amp; = 5y + 7 &amp; \text{{here}} \\[2pt]
        &amp; = 7 &amp;
        \end{{array}}
        \]'''
        output_string = r'''\(\begin{{array}}{{rcc}}
        5x &amp; = 5y + 7 &amp; \text{{here}} \\[2pt]
        &amp; = 7 &amp;
        \end{{array}}
        \)'''
        assert equation2png(input_string) == output_string

    def test_replace_inline_delimiters(self):
        input_string = '\\(5x + y\\)'
        output_string = '\\(5x + y\\)'
        assert equation2png(input_string) == output_string

class TestUnicodeEquations(TestCase):
    '''Tests that unicode in equations is handled correctly'''
    def test_convert_quote_marks(self):
        input_string = r'\(&#8220;text&#8221;\)'
        middle_string = u'\\(\u201ctext\u201d\\)'
        output_string = '\\(\xe2\x80\x9ctext\xe2\x80\x9d\\)'
        assert unescape(input_string) == middle_string
        assert middle_string.strip().encode('utf-8') == output_string

    def test_replace_times(self):
        input_string = '\\(5 \xc3\x97 x\\)'
        output_string = r'\(5 \times x\)'
        assert unicode_replacements(input_string) == output_string

    def test_convert_superscript(self):
        input_string = u'\\(mol·g⁻¹ ℃\\)'
        middle_string = '\\(mol\xc2\xb7g\xe2\x81\xbb\xc2\xb9 \xe2\x84\x83\\)'
        output_string = r'\(mol\cdot g^{-1} ^{\circ}C\)'
        assert input_string.encode('utf-8') == middle_string
        assert unicode_replacements(middle_string) == output_string
