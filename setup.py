# setup.py

import os
from setuptools import setup, find_packages

# Set the PYTHONPATH environment variable
os.environ['PYTHONPATH'] = '/path/to/GraphQLDM:' + os.environ.get('PYTHONPATH', '')

setup(
    name='graphqldm',
    version='0.1',
    py_modules=['graphqldm'],
    install_requires=[
        'Click',
        'requests',
        'typer',
        'rich',
    ],
    entry_points='''
        [console_scripts]
        gqldm=graphqldm.cli:app
    ''',
)
