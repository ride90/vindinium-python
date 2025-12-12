"""Setup configuration for the vindinium package.

This module configures the package installation using setuptools,
including dependencies, metadata, and package discovery.
"""

from pathlib import Path
from setuptools import setup, find_packages

__author__ = 'Renato de Pontes Pereira'
__author_email__ = 'renato.ppontes@gmail.com'
__version__ = '0.2.0'
__date__ = '2025 12 12'

# Read long description from README
try:
    readme_path = Path(__file__).parent / 'README.md'
    long_description = readme_path.read_text(encoding='utf-8')
except Exception:
    long_description = ''

setup(
    name='vindinium',
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    license='MIT License',
    description='Python 3 client for vindinium.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ride90/vindinium-python',
    download_url='https://github.com/ride90/vindinium-python',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.13',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='vindinium game python ai bot',
    packages=find_packages(),
    package_data={'': ['README.md', 'LICENSE']},
    install_requires=['requests>=2.32.0'],
    python_requires='>=3.13',
)
