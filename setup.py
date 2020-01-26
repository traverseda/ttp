from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="time-tracker-plus",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version="1.1",
    license='MIT',
    author = 'Alex Davies',
    author_email = 'traverse.da@gmail.com',
    url = 'https://github.com/traverseda/ttp',
    download_url = 'https://github.com/traverseda/ttp/archive/v1.0.tar.gz',
    packages=find_packages(),
    package_data={
        "": ["templates/*"],
    },
    entry_points = {
        'console_scripts': ['ttp=ttp.main:cli'],
    },
    install_requires=(
        'appdirs',
        'click',
        'arrow',
        'dateparser',
        'jinja2',
        'pygments',
    )
)
