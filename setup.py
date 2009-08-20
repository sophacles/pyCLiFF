#!/usr/bin/env python

from distutils.core import setup

description_long = '''
pyCLiFF, the Python Command Line Filter Framework is a simple tool designed
to remove the boilerplate and annoyances from command line filters.

In *nix there is a tradition of using pipes to connact many programs together
when processing data. The programs are usually very single transformations on
text.  This text may come in from a file or from stdin, and leave via file or
stdout. This pattern is ubiquitous in *nix programming, allowing for very
powerful command line usage.   Such tools frequently (mostly?) follow the this
pattern:

1. Setup/handle arguments
2. Mainloop:
  A. Read line from input file (stdin or file)
  B. Process that line in some way
  C. Output the result of processing.
3. Cleanup and exit.

The above pattern results in many programs with a large portion of boilerplate
code, and a few dozen lines of unique application code. pyCLiFF is an attempt
to cover all the parts of a command line filter that are not unique. (Usually
this means step B above).
'''

setup(name='pyCLiFF',
      version='0.1',
      description= '''pyCLiFF, the Python Command Line Filter Framework is a simple tool designed to remove the boilerplate and annoyances from command line filters.''',
      long_description = description_long,
      author='Erich Heine',
      author_email='sophacles@gmail.com',
      url='http://github.com/sophacles/pyCLiFF/tree/master',
      classifiers=[
            "Development Status :: 3 - Alpha",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "Intended Audience :: System Administrators",
            "License :: OSI Approved :: MIT License",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: POSIX",
            "Operating System :: Unix",
            "Programming Language :: Python :: 2",
            "Topic :: Other/Nonlisted Topic",
            "Topic :: Software Development :: Libraries",
            "Topic :: System :: Shells",
            "Topic :: System :: System Shells",
            "Topic :: Terminals",
            "Topic :: Text Processing :: Filters",
            "Topic :: Utilities"],
      py_modules=['pyCLiFF']
)
