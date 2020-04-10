import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyidaungsu",
    version="0.0.2",
    author="Kaung Htet San",
    author_email="kaung@htetsan.me",
    description="Python library for Myanmar language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kaunghtetsan275/pyidaungsu",
    download_url = 'https://github.com/kaunghtetsan275/pyidaungsu/archive/0.0.2.tar.gz',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)