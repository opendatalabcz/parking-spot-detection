from distutils.core import setup
from setuptools import find_packages

requires = [
    'six>=1.10.0',
]

if __name__ == "__main__":
    setup(
        name="parking_spot_detection",
        version="0.0.1",
        packages=find_packages(),
        author='Jiri Groh',
        author_email='email@email.com',
        install_requires=requires,
        description='',
        include_package_data=True,
    )