import os
import shutil
import subprocess
from pathlib import Path

import setuptools

from VERSION_PYTHON import __version_minimum_python__, __version_maximum_python__

version_file = Path(__file__).parent / "VERSION.py"

# noinspection PyBroadException
try:
    git_version = subprocess.check_output(["git", "describe", "--tag", "--abbrev=0"]).decode("utf-8").strip()
    pypi_version = git_version[1:]
except Exception:
    with open(version_file, "r") as vf:
        git_version = vf.read().strip().split("=")[-1].strip().replace('"', '')
        pypi_version = git_version[1:]

with open(version_file, "w") as vf:
    vf.write(
        f"# DO NOT EDIT - VERSIONING CONTROLLED BY GIT TAGS{os.linesep}__version__ = \"{git_version}\"{os.linesep}")

if Path("build").exists():
    print("Removing stale \"build\" directory before packaging...")
    shutil.rmtree("build")

if Path("dist").exists():
    print("Removing stale \"dist\" directory before packaging...")
    shutil.rmtree("dist")

if Path("yfpy.egg-info").exists():
    print("Removing stale \"yfpy.egg-info\" directory before packaging...")
    shutil.rmtree("yfpy.egg-info")

with open("README.md", "r", encoding="utf8") as docs:
    long_description = docs.read()

with open("requirements.txt", "r", encoding="utf8") as reqs:
    required = reqs.read().splitlines()

supported_python_minor_versions = [
    version for version in
    range(int(__version_minimum_python__.split(".")[-1]), (int(__version_maximum_python__.split(".")[-1]) + 1))
]

setuptools.setup(
    name="yfpy",
    version=pypi_version,
    author="Wren J. R.",
    author_email="uberfastman@uberfastman.dev",
    description="Python API wrapper for the Yahoo Fantasy Sports public API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="yahoo fantasy sports api wrapper nfl football nhl hockey mlb baseball nba basketball",
    url="https://github.com/uberfastman/yfpy",
    download_url=f"https://github.com/uberfastman/yfpy/archive/{git_version}.tar.gz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        *[f"Programming Language :: Python :: 3.{version}" for version in supported_python_minor_versions],
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Console",
        "Intended Audience :: Developers"
    ],
    python_requires=f">={__version_minimum_python__}",
    install_requires=required
)
