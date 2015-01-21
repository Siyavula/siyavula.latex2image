
import hashlib
from latex2image.imageutils import run_latex


equation = '\(F = m \cdot a\)'
codehash = hashlib.md5(equation).hexdigest()
cache_path = '.cache'


imagepath = run_latex('equation', codehash, equation, cache_path)

print '\n\n' + imagepath
