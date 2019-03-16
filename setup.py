import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nico_client",
    version="1.0.38",
    author="Jaeseo Park",
    author_email="jaeseopark@icloud.com",
    description="A python client to interact with nicovideo.jp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lekordable/nico_client",
    packages=setuptools.find_packages(exclude=["tests","tests.*"]),
    install_requires=['requests', 'nicopy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English"
    ]
)
