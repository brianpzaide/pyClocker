from setuptools import setup, find_packages


setup(
    name='pyClocker',
    version='1.0.0',
    description='this package helps measure time spent on coding each day',
    author='brianpzaide',
    url='https://github.com/brianpzaide/pyClocker',
    install_requires=[
                      "matplotlib==3.6.3",
                      "typer==0.9.0",
                      "tabulate==0.9.0"],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pyClocker = pyClocker.__main__:main',
        ],
    },
)