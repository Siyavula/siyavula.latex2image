''' Miscellaneous functions that deals with html processing'''
import HTMLParser
import re


def repair_equations(html):
    r''' Some equations contain escaped unicode entities. Replace them with
    unicode.

    Some images have nested math environments i.e. $\(\text{blah}\)$, remove
    the inner math delimiters

    '''
    htmlparser = HTMLParser.HTMLParser()
    html = html.replace('&amp;#', '&#')
    entities = re.findall('&#.*?;', html)
    for ent in entities:
        html = html.replace(ent, htmlparser.unescape(ent))

    # some unicode needs to get replaced with math-mode symbols but they cannot
    # use those symbols if they are already in a math mode.
    return html
