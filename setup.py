import os
import shutil
import subprocess

import setuptools

version_file = os.path.join(os.path.dirname(__file__), "VERSION")

# noinspection PyBroadException
try:
    git_version = subprocess.check_output(["git", "describe", "--tag", "--abbrev=0"]).decode("utf-8").strip()
    pypi_version = git_version[1:]
except Exception:
    with open(version_file, "r") as vf:
        git_version = vf.read().strip().split("=")[-1].strip().replace('"', '')
        pypi_version = git_version[1:]

with open(version_file, "w") as vf:
    vf.write("{}{}__version__ = \"{}\"{}".format(
        "# DO NOT EDIT - VERSIONING CONTROLLED BY GIT TAGS",
        os.linesep,
        git_version,
        os.linesep
    ))

if os.path.exists("build"):
    print("Removing stale \"build\" directory before packaging...")
    shutil.rmtree("build")

if os.path.exists("dist"):
    print("Removing stale \"dist\" directory before packaging...")
    shutil.rmtree("dist")

if os.path.exists("yfpy.egg-info"):
    print("Removing stale \"yfpy.egg-info\" directory before packaging...")
    shutil.rmtree("yfpy.egg-info")

with open("README.md", "r", encoding="utf8") as docs:
    long_description = docs.read()

with open("requirements.txt", "r", encoding="utf8") as reqs:
    required = reqs.read().splitlines()

setuptools.setup(
    name="yfpy",
    version=pypi_version,
    author="Wren J. R.",
    author_email="wrenjr@yahoo.com",
    description="Python API wrapper for the Yahoo Fantasy Sports public API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="yahoo fantasy sports api wrapper nfl football nhl hockey mlb baseball nba basketball",
    url="https://github.com/uberfastman/yfpy",
    download_url="https://github.com/uberfastman/yfpy/archive/{}.tar.gz".format(git_version),
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Console",
        "Intended Audience :: Developers"
    ],
    python_requires=">=3.5",
    install_requires=required
)
