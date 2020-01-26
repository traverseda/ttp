from setuptools import setup, find_packages
setup(
    name="time-tracker-plus",
    version="1.0",
    packages=find_packages(),
    entry_points = {
        'console_scripts': ['ttp=ttp.main:cli'],
    }
    install_requires=(
        'appdirs',
        'click',
        'arrow',
        'dateparser',
        'jinja2',
        'pygments',
    )
)
