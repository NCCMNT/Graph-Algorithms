from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().split('\n')

setup(
    name = "tests",
    packages = find_packages(),
    install_requires = requirements
)