# This Python file uses the following encoding: utf-8

from setuptools import setup, find_packages
from os import path

# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import and use built-in open()
from io import open as io_open
import re


summary = "App that automates the downloading of movies"
project_homepage = "https://github.com/Housain-maina/PyMovieDownloader"
here = path.abspath(path.dirname(__file__))


def readall(*args):
    with io_open(path.join(here, *args), encoding="utf-8") as fp:
        return fp.read()


with open("requirements.txt") as f:
    dependencies = f.read().splitlines()

documentation = readall("README.md")

setup(
    name="pymoviedownloader",
    version="0.0.1",
    description=summary,
    long_description=documentation,
    long_description_content_type="text/markdown",
    author="Hussaini Usman",
    author_email="hussainmaina27@gmail.com",
    maintainer="Hussaini Usman",
    license="MIT",
    url=project_homepage,
    download_url=(project_homepage + "/archive/main.zip"),
    project_urls={
        "Documentation": project_homepage,
        "Tracker": (project_homepage + "/issues"),
        "Source": project_homepage + "/tree/main",
    },
    packages=find_packages(),
    keywords="python automation movie bot selenium download",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Topic :: Utilities",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Natural Language :: English",
    ],
    install_requires=dependencies,
    python_requires=">=3.5",
    platforms=["win32", "linux", "linux2", "darwin"],
    entry_points={"console_scripts": []},
)
