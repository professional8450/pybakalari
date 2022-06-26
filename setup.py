from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

packages = [
    'pybakalari'
]

setup(
    name='pybakalari',
    version='1.0.0',
    packages=packages,
    requirements=requirements,
    url='https://github.com/professional8450/pybakalari',
    license='',
    author='professional8450',
    author_email='professional8450@gmail.com',
    description='An API wrapper for Bakaláři.'
)
