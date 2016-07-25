import os
import errno
import shutil
import re
import htmlentitydefs

from htmlutils import repair_equations


def mkdir_p(path):
    ''' mkdir -p functionality
    from:
    http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    '''
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def copy_if_newer(src, dest):
    ''' Copy a file from src to  dest if src is newer than dest

    Returns True if success or False if there was a problem
    '''
    success = True
    dest_dir = os.path.dirname(dest)
    if (dest_dir is None) or (src is None):
        success = False
        return success
    if not os.path.exists(dest_dir):
        mkdir_p(dest_dir)

    if os.path.exists(src):
        # check whether src was modified more than a second after dest
        # and only copy if that was the case
        srcmtime = os.path.getmtime(src)
        try:
            destmtime = os.path.getmtime(dest)
            if srcmtime - destmtime > 1:
                shutil.copy2(src, dest)

        except OSError:
            # destination doesn't exist
            shutil.copy2(src, dest)
    else:
        success = False

    return success


def unescape(text):
    '''Formats unicode characters correctly'''
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is
    return re.sub("&#?\w+;", fixup, text)


def cleanup_code(code):
    ''' Removes nested math delimiters of the form \( \) inside $ $ pairs'''
    result = re.findall(r'\$(.*?)\$', code)
    for snippet in result:
        newsnippet = snippet.replace(r'\(', ' ').replace(r'\)', ' ')
        code = code.replace(snippet, newsnippet)

    code = code.strip()

    # if align* or {align} in code we don't need delimiters
    if (r'align*' in code) or ('{align}' in code):
        if code.startswith(r'\('):
            code = code[2:]
        if code.endswith('\)'):
            code = code[:-2]

    newcode = [line for line in code.split('\n') if (not line.strip()) and (not line.strip().startswith('%'))]
    code = '\n'.join(newcode)

    code = repair_equations(code)

    return code


def unicode_replacements(latex):
    '''Takes in latex and replaces specific unicode characters with latex symbols'''
    unicode_operators = {
        "\xe2\x88\x92": '-',
        "\xc3\x97": r'\times',
        "\xc2\xb7": r'\cdot ',
    }
    unicode_superscripts = {
        "\xc2\xb0": r'\text{$^\circ$}',
        "\xe2\x81\xbb\xc2\xb9": r'^{-1}',
        "\xc2\xb2": r'^{2}',
        "\xc2\xb3": r'^{3}',
        "\xe2\x84\x83": r'^{\circ}C',
    }
    unicode_punctation_spacing = {
        "\xc2\xa0": ' ',
    }
    unicode_symbols = {
        "\xce\xa9": r'\ensuremath{\Omega}',
        "\xe2\x82\xac": r'\euro',
    }

    operations = [
        unicode_operators
        unicode_superscripts
        unicode_punctation_spacing
        unicode_symbols
        ]

    for operation in operations:
        for key, value in operation.iteritems():
            latex = latex.replace(key, value)

    return latex
