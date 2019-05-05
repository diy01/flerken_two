import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flerken",
    version="0.0.5",
    author="david",
    author_email="author@example.com",
    description="test 01",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/diy01/flerken",
    packages=setuptools.find_packages('templates'),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
