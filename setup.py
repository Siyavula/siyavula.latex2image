import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'termcolor',
    'lxml'
    ]

setup(name='siyavula.latex2image',
      version='1.0.0',
      description='LaTeX to image converter',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        ],
      author='Ewald Zietsman',
      author_email='ewald@siyavula.com',
      url='',
      keywords='python latex',
      namespace_packages=['siyavula',],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      )
