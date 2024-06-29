from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='dumbell_tracker',
    version='1.0',
    author='Omar Salem', 
    packages=find_packages(),
    long_description=open('README.md').read()
)