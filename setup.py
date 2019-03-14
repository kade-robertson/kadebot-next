from setuptools import find_packages, setup

import src

long_desc = ""
try:
    import pypandoc
    long_desc = pypandoc.convert('README.md', 'rst', extra_args=('--eol', 'lf'))
except (IOError, ImportError):
    long_desc = open('README.md').read()

requirements = []
with open('requirements.txt') as reqs:
    requirements = [req.strip() for req in reqs.readlines()]

setup(
    name="kadebot",
    version="0.1.0",
    description="Telegram chat bot, using message intent to improve chat",
    long_description=long_desc,
    classifiers=["Programming Language :: Python :: 3.6", "Programming Language :: Python :: 3.7"],
    entry_points={'console_scripts': ['kadebot = src:main']},
    keywords="kadebot telegram chat bot intent wit.ai",
    author="Kade Robertson",
    author_email="kade@kaderobertson.pw",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.6, <4')
