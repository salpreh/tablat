# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='tablat',
    version='0.1.0',
    description='Print basic tables in python',
    long_description=readme,
    author='salpreh',
    author_email='salva.perez46@gmail.com',
    url='https://github.com/salpreh/tablat',
    license=license,
    packages=find_packages(exclude=('test', 'assets', 'venv'))
)
