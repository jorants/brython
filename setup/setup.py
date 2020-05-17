# Always prefer setuptools over distutils
from setuptools import setup, find_packages

import os
import shutil
import sys
import codecs


# From python.org, get the verison number
def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


# Load the readme file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()





command = sys.argv[1]

if command == "sdist":
    this_dir = os.getcwd()
    root_dir = os.path.dirname(this_dir)
    release_dir = os.path.join(root_dir, "releases")

    # before creating the distribution, copy files from other locations in
    # the repository
    print("copying files...")
    src_dir = os.path.join(root_dir, "www", "src")
    brython_dir = os.path.join(this_dir, "brython")

    # copy python_minifier from /scripts into current directory
    fname = "python_minifier.py"
    shutil.copyfile(os.path.join(root_dir, "scripts", fname),
        os.path.join(brython_dir, fname))

    # create an empty subdirectory for data files
    data_dir = os.path.join(this_dir, "brython", "data")
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
    os.mkdir(data_dir)

    # copy files from /www/src into data_dir
    for fname in ["brython_stdlib.js", "unicode.txt"]:
        shutil.copyfile(os.path.join(src_dir, fname),
            os.path.join(data_dir, fname))
    shutil.copyfile(os.path.join(src_dir, "brython_no_static.js"),
        os.path.join(data_dir, "brython.js"))

    # copy files from release_dir to data_dir
    for fname in ["index.html", "README.txt"]:
        shutil.copyfile(os.path.join(release_dir, fname),
            os.path.join(data_dir, fname))

    # copy demo.html in data_dir
    with open(os.path.join(root_dir, 'www', 'demo.html'), encoding="utf-8") as f:
        demo = f.read()
    start_tag = "<!-- start copy -->"
    end_tag = "<!-- end copy -->"
    start = demo.find(start_tag)
    if start == -1:
        raise Exception("No tag <!-- start copy --> in demo.html")
    end = demo.find(end_tag)
    if end == -1:
        raise Exception("No tag <!-- end copy --> in demo.html")
    body = demo[start + len(start_tag) : end].strip()

    with open(os.path.join(release_dir, "demo.tmpl"), encoding="utf-8") as f:
        template = f.read()

    demo = template.replace("{{body}}", body)

    with open(os.path.join(data_dir, "demo.html"), "w", encoding="utf-8") as out:
        out.write(demo)

setup(
    name='brython',

    version=get_version("brython/__init__.py"),
    description='Brython is an implementation of Python 3 running in the browser',

    long_description=long_description,

    # The project's main homepage.
    url='http://brython.info',

    # Author details
    author='Pierre Quentel',
    author_email='quentel.pierre@orange.fr',

    packages=find_packages(),

    # Choose your license
    license='BSD',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Interpreters',

        'Operating System :: OS Independent',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],

    # What does your project relate to?
    keywords='Python browser',

    package_data={
        'brython': ['data/*.*']
    },
    entry_points={
        'console_scripts': [
            'brython-cli = brython.__main__:main'
            ]
    }


)
