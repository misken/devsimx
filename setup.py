from setuptools import find_packages, setup

setup(
    name='devsimx',
    packages=find_packages("src"),
    package_dir={"": "src"},
    version='0.1.0',
    description='Example simulation development project',
    author='simdevr',
    license='MIT',
)
