import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nicoclient",
    version="1.1.0",
    author="Jaeseo Park",
    author_email="jaeseopark@icloud.com",
    description="A python client to interact with nicovideo.jp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lekordable/nicoclient",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    install_requires=['requests', 'beautifulsoup4'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Natural Language :: English"
    ]
)
