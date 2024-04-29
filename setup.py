# setup.py

from setuptools import setup, find_packages

setup(
    name='graphqldm',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gqldm = graphqldm.cli:main'
        ]
    },
    install_requires=[
        'requests',
    ],
)