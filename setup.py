import setuptools


def get_version():
    version = {}
    with open("pymode/version.py") as fp:
        exec(fp.read(), version)
    return version["__version__"]


with open("README.md", "r") as f:
    readme = f.read()


setuptools.setup(
    name="pymode",
    author="David Wallace",
    author_email="dwallace0723@gmail.com",
    version=get_version(),
    url="https://github.com/dwallace0723/pymode",
    description="A python client for typed interactions with the Mode Analytics API.",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Topic :: Software Development",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="mode analytics python",
    license="MIT",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=["requests>=2.22.0", "attrs>=19.3.0"],
    python_requires=">=3.6",
)
