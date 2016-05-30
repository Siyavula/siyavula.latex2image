from unittest import TestCase

from siyavula.latex2image.equation2png import equation2png

class TestEquationConversion(TestCase):
    '''
    Tests the equation converter
    '''
    
    def setUp(self):
        self.pspictureElement = r'''\[\begin{{array}}{{rcc}}
        5x &amp; = 5y + 7 &amp; \text{{here}} \\[2pt]
        &amp; = 7 &amp;
        \end{{array}}
        \]'''
    
    def test_replace_delimiters(self):
        output_string = r'''\(\begin{{array}}{{rcc}}
        5x  &amp; = 5y + 7  &amp; \text{{here}} \\(2pt]
         &amp; = 7  &amp;
        \end{{array}}
        \)'''.replace('{{', '{').replace('}}', '}')

        assert equation2png(self.pspictureElement.replace('{{', '{').replace('}}', '}')) == output_string