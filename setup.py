from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyidaungsu",
    version="0.0.7",
    author="Kaung Htet San",
    author_email="kaung@htetsan.me",
    description="Python library for Myanmar language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kaunghtetsan275/pyidaungsu",
    download_url = 'https://github.com/kaunghtetsan275/pyidaungsu/archive/0.0.7.tar.gz',
    install_requires=['numpy','python-crfsuite'],
    packages=find_packages(),
    package_data={'pyidaungsu': ['pyidaungsu/model/*']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)