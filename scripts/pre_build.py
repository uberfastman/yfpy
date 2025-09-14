import os
import shutil
import sys
from pathlib import Path
from subprocess import CalledProcessError, DEVNULL, check_output

from ruamel.yaml import YAML

project_root_dir = Path(__file__).parent.parent

# add project root directory to path in order to import from VERSION.py and VERSION_PYTHON.py if needed
path = set(sys.path)
path.add(str(project_root_dir))
sys.path = list(path)

from VERSION_PYTHON import __version_minimum_python__, __version_maximum_python__  # noqa

# copy CNAME file from resources to docs
docs_dir = project_root_dir / "docs"

print("Copying CNAME file to \"/docs\" for GitHub Pages...")

cname_file_path = project_root_dir / "resources" / "documentation" / "CNAME"
shutil.copyfile(cname_file_path, docs_dir / "CNAME")

print("...successfully prepared docs for GitHub Pages.")

# noinspection PyBroadException
try:
    print("Setting __version__ value in VERSION.py with package version from git tag...")
    git_version = check_output(
        ["git", "describe", "--tag", "--abbrev=0"],
        stderr=DEVNULL
    ).decode("utf-8").strip()
    pypi_version = git_version[1:]

    with open(project_root_dir / "VERSION.py", "w") as vf:
        vf.write(
            f"# DO NOT EDIT - VERSIONING CONTROLLED BY GIT TAGS{os.linesep}"
            f"__version__ = \"{git_version[1:]}\"{os.linesep}"
        )
    print("...updated VERSION.py with latest package version.")

except CalledProcessError as e:
    from VERSION import __version__
    git_version = __version__
    print(f"...no git tag found. Defaulting to existing __version__ value in VERSION.py: v{__version__}")

docker_compose_yaml_file = project_root_dir / "compose.yaml"
if docker_compose_yaml_file.exists():
    print("Updating \"compose.yaml\" with YFPY version from git tag before packaging...")

    yaml = YAML(typ="rt")
    docker_compose_yaml = yaml.load(docker_compose_yaml_file)
    docker_compose_yaml["services"]["package"]["image"] = (
        f"{docker_compose_yaml['services']['package']['image'].split(':')[0]}:{git_version.replace('v', '')}"
    )

    yaml.default_flow_style = False
    yaml.dump(docker_compose_yaml, docker_compose_yaml_file)
    print("...updated \"compose.yaml\" with latest YFPY version.")

docker_compose_build_yaml_file = project_root_dir / "compose.build.yaml"
if docker_compose_build_yaml_file.exists():
    print("Updating \"compose.build.yaml\" with Python version from VERSION_PYTHON.py before packaging...")

    yaml = YAML(typ="rt")
    docker_compose_build_yaml = yaml.load(docker_compose_build_yaml_file)

    updated_build_args = []
    for build_arg in docker_compose_build_yaml["services"]["package"]["build"]["args"]:
        build_arg_key, build_arg_value = build_arg.split("=")
        if build_arg_key == "PYTHON_VERSION_MAJOR":
            build_arg_value = __version_maximum_python__.split(".")[0]
        elif build_arg_key == "PYTHON_VERSION_MINOR":
            build_arg_value = __version_maximum_python__.split(".")[1]
        elif build_arg_key == "PYTHON_VERSION_PATCH":
            build_arg_value = __version_maximum_python__.split(".")[2]
        updated_build_args.append(f"{build_arg_key}={build_arg_value}")
    docker_compose_build_yaml["services"]["package"]["build"]["args"] = updated_build_args

    yaml.default_flow_style = False
    yaml.dump(docker_compose_build_yaml, docker_compose_build_yaml_file)
    print("...updated \"compose.build.yaml\" with latest supported Python version.")
