import setuptools

with open("README.md", "r") as docs:
    long_description = docs.read()

with open("requirements.txt") as reqs:
    required = reqs.read().splitlines()

setuptools.setup(
    name="yffpy",
    version="2.0.0",
    author="Wren J. R.",
    author_email="wrenjr@yahoo.com",
    description="Python API wrapper for the Yahoo Fantasy Football public API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="yahoo fantasy football api wrapper sports",
    url="https://github.com/uberfastman/yffpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Console",
        "Intended Audience :: Developers"
    ],
    python_requires=">=3.5",
    install_requires=required
)
