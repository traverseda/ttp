from setuptools import setup, find_packages
setup(
    name="time-tracker-plus",
    version="1.0",
    license='MIT'
    author = 'Alex Davies',
    author_email = 'traverse.da@gmail.com',
    url = 'https://github.com/traverseda/ttp',
    download_url = 'https://github.com/traverseda/ttp/archive/v1.0.tar.gz'
    packages=find_packages(),
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
