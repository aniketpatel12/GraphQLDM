# setup.py

from setuptools import setup

setup(
    name='graphqldm',
    version='0.1',
    py_modules=['graphqldm'],
    install_requires=[
        'Click',
        'requests',
        'typer',
    ],
    entry_points='''
        [console_scripts]
        gqldm=graphqldm.cli:app
    ''',
)
