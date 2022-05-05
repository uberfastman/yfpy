import os
import shutil
import subprocess
from pathlib import Path

import setuptools

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

docs_path = Path("docs")
docs_index_path = docs_path / "index.html"
if docs_index_path.exists():
    print("Removing stale \"sphinx docs\" content before packaging...")
    shutil.rmtree(docs_path)
    sphinx_docs_path = Path("docs-sphinx") / "build" / "html"
    shutil.copytree(sphinx_docs_path, docs_path)

with open("README.md", "r", encoding="utf8") as docs:
    long_description = docs.read()

with open("requirements.txt", "r", encoding="utf8") as reqs:
    required = reqs.read().splitlines()

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
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
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
