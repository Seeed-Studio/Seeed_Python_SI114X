"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='seeed-python-si114x',
    version="1.0.1",
    description='Python library for the Grove - Sunlight Sensor (si114x). ',
    long_description=long_description,
    long_description_content_type='text/markdown',

    # The project's main homepage.
    url='https://github.com/Seeed-Studio/Seeed_Python_SI114X',

    # Author details
    author='Hansen',
    author_email='595355940@qq.com',
    
    install_requires=['Seeed-grove.py'],
    
    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Hardware',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    
    entry_points = {
    'console_scripts': [
        'seeed_si144x = seeed_si114x:main'
    ]},

    # What does your project relate to?
    keywords='seeed grove si114x  sensor i2c hardware',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    py_modules=['seeed_si114x'],
)
