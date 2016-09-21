# coding=utf-8
from unittest import TestCase

from siyavula.latex2image.equation2png import equation2png
from siyavula.latex2image.utils import unescape, unicode_replacements


class TestBaseEquationConversion(TestCase):
    """Test the equation converter."""

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
        self.assertEqual(equation2png(input_string), output_string)

    def test_replace_inline_delimiters(self):
        input_string = '\\(5x + y\\)'
        output_string = '\\(5x + y\\)'
        self.assertEqual(equation2png(input_string), output_string)

    def test_complex_equation(self):
        input_string = r'''\[\begin{{aligned}}
        \vec{{F}}_{{g}} & = m\vec{{g}} \\
        & = (\text{{12,7}}\ \text{{kg}})(\text{{9,8}}\ \text{{m·s$^{{-2}}$}}) \\
        & = \text{{124,46}}\ \text{{N}}
        \end{{aligned}}
        \]'''
        output_string = '\\(\\begin{{aligned}}\n        \\vec{{F}}_{{g}} & = m\\vec{{g}} \\\\\n        & = (\\text{{12,7}}\\ \\text{{kg}})(\\text{{9,8}}\\ \\text{{m\xc2\xb7s$^{{-2}}$}}) \\\\\n        & = \\text{{124,46}}\\ \\text{{N}}\n        \\end{{aligned}}\n        \\)'

        self.assertEqual(equation2png(input_string), output_string)


class TestUnicodeEquations(TestCase):
    """Test that unicode in equations is handled correctly."""

    def test_convert_quote_marks(self):
        input_string = r'\(&#8220;text&#8221;\)'
        middle_string = u'\\(\u201ctext\u201d\\)'
        output_string = '\\(\xe2\x80\x9ctext\xe2\x80\x9d\\)'
        self.assertEqual(unescape(input_string), middle_string)
        self.assertEqual(middle_string.strip().encode('utf-8'), output_string)

    def test_replace_times(self):
        input_string = '\\(5 \xc3\x97 x\\)'
        output_string = r'\(5 \times x\)'
        self.assertEqual(unicode_replacements(input_string), output_string)

    def test_convert_superscript(self):
        input_string = u'\\(mol·g⁻¹ ℃ x² x³\\)'
        middle_string = '\\(mol\xc2\xb7g\xe2\x81\xbb\xc2\xb9 \xe2\x84\x83 x\xc2\xb2 x\xc2\xb3\\)'
        output_string = r'\(mol\ensuremath{\cdot}g^{-1} ^{\circ}C x^{2} x^{3}\)'
        self.assertEqual(input_string.encode('utf-8'), middle_string)
        self.assertEqual(unicode_replacements(middle_string), output_string)

    def test_middot_in_text_mode(self):
        input_string = '\\text{{m·s$^{{-2}}$}}'
        middle_string = '\\text{{m\xc2\xb7s$^{{-2}}$}}'
        output_string = '\\text{{m\ensuremath{\cdot}s$^{{-2}}$}}'
        self.assertEqual(unescape(input_string), '\\text{{m\xc2\xb7s$^{{-2}}$}}')
        self.assertEqual(unicode_replacements(middle_string), output_string)

    def test_middot_mess(self):
        input_string = '\\(5 &middot; 6\\)'
        middle_string = '\\(5 \xb7 6\\)'
        output_string = r'\(5 \ensuremath{\cdot} 6\)'
        self.assertEqual(unescape(input_string), u'\\(5 \xb7 6\\)')
        self.assertEqual(unicode_replacements(middle_string), output_string)

    def test_micro_mu_in_text_mode(self):
        input_string = u'\\text{{&#181; µ &#956; μ}}'
        middle_string = '\\text{{\xb5 \xb5 \u03bc \u03bc}}'
        output_string = '\\text{{\ensuremath{\mu} \ensuremath{\mu} \ensuremath{\mu} \ensuremath{\mu}}}'
        self.assertEqual(unescape(input_string), u'\\text{{\xb5 \xb5 \u03bc \u03bc}}')
        self.assertEqual(unicode_replacements(middle_string), output_string)
