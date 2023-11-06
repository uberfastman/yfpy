import os
import shutil
import subprocess
from pathlib import Path

import setuptools
from ruamel.yaml import YAML

from VERSION_PYTHON import __version_minimum_python__, __version_maximum_python__

project_root_dir = Path(__file__).parent

version_file = project_root_dir / "VERSION.py"

# noinspection PyBroadException
try:
    git_version = subprocess.check_output(["git", "describe", "--tag", "--abbrev=0"]).decode("utf-8").strip()
    pypi_version = git_version[1:]
except Exception:
    with open(version_file, "r") as vf:
        git_version = vf.read().strip().split("=")[-1].strip().replace('"', '')
        pypi_version = git_version[1:]

with open(version_file, "w") as vf:
    print("Updating \"VERSION.py\" with YFPY version from git tag before packaging...")
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

supported_python_major_versions = [
    version for version in
    range(int(__version_minimum_python__.split(".")[0]), (int(__version_maximum_python__.split(".")[0]) + 1))
]

supported_python_minor_versions = [
    version for version in
    range(int(__version_minimum_python__.split(".")[-1]), (int(__version_maximum_python__.split(".")[-1]) + 1))
]

docker_compose_yaml_file = project_root_dir / "compose.yaml"

if docker_compose_yaml_file.exists():
    print("Updating \"compose.yaml\" with YFPY version from git tag and Python version from .env before packaging...")

    yaml = YAML(typ="rt")
    docker_compose_yaml = yaml.load(docker_compose_yaml_file)
    docker_compose_yaml["services"]["package"]["image"] = (
        f"{docker_compose_yaml['services']['package']['image'].split(':')[0]}:{git_version.replace('v', '')}"
    )
    updated_build_args = []
    for build_arg in docker_compose_yaml["services"]["package"]["build"]["args"]:
        build_arg_key, build_arg_value = build_arg.split("=")
        if build_arg_key == "PYTHON_VERSION_MAJOR":
            build_arg_value = supported_python_major_versions[0]
        elif build_arg_key == "PYTHON_VERSION_MINOR":
            build_arg_value = supported_python_minor_versions[-1]
        updated_build_args.append(f"{build_arg_key}={build_arg_value}")
    docker_compose_yaml["services"]["package"]["build"]["args"] = updated_build_args

    yaml.default_flow_style = False
    yaml.dump(docker_compose_yaml, docker_compose_yaml_file)

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
        f"Programming Language :: Python :: {supported_python_major_versions[0]}",
        *[
            f"Programming Language :: Python :: {supported_python_major_versions[0]}.{version}"
            for version in supported_python_minor_versions
        ],
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
