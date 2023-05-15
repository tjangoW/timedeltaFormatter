import pathlib

from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="timedeltaFormatter",

    version="0.1.0",
    description="A formatter for timedelta",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tmp",
    author="wolfgang",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    py_modules=["timedeltaFormatter"],
    python_requires=">=3.8, <4",
    project_urls={
        'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
        'Source': 'https://github.com/pypa/sampleproject/',
    }
)
