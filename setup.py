from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='fxdc',
    version='4.0',
    packages=find_packages(),
    author='FedxD',
    author_email='fedxdofficial@gmail.com',
    description='This Package Parses FxDC file and returns the object',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/KazimFedxD/FedxD-Data-Container',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    
)