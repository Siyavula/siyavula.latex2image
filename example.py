
import hashlib
from latex2image.imageutils import run_latex


def read_equations():
    txt = open('test-equations-short.txt', 'r').read()
    equations = [e for e in txt.split('----') if len(e.strip()) > 0]

    for i, e in enumerate(equations):
        if 'aligned' in e:
            equations[i] = e.strip()[2:-2].replace('aligned', 'align')


    return equations

if __name__ == "__main__":
    equations = read_equations()
    for i, equation in enumerate(equations):
        codehash = hashlib.md5(equation).hexdigest()
        cache_path = 'cache'
        imagepath = run_latex('equation', codehash, equation, cache_path)
        print '\n {}/{} > '.format(i+1, len(equations)) + imagepath
