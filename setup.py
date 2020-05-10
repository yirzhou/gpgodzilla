from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    url="https://github.com/yirzhou/gpgodzilla",
    author="Yiren Zhou",
    author_email="yiren.chow@gmail.com",
    name="gpgodzilla",
    version="0.0.1",
    description="Modify large text file line by line and encrypt with GnuPG.",
    py_modules=["gpgodzilla"],
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
