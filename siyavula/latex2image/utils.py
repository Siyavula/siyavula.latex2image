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

    # remove blank lines and lines that start with %
    newcode = []
    for line in code.split('\n'):
        if line.strip().startswith('%'):
            continue
        if not line.strip():
            continue
        newcode.append(line)
    code = '\n'.join(newcode)

    code = repair_equations(code)

    return code


def unicode_replacements(latex):
    '''Takes in latex and replaces specific unicode characters with latex symbols'''
    latex = latex.replace("\xe2\x88\x92", '-')
    latex = latex.replace("\xc3\x97", r'\times')
    latex = latex.replace("\xc2\xa0", ' ')
    latex = latex.replace("\xce\xa9", r'\ensuremath{\Omega}')
    latex = latex.replace("\xc2\xb0", r'\text{$^\circ$}')
    latex = latex.replace("\xe2\x82\xac", r'\euro')
    return latex
