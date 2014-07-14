from setuptools import setup, find_packages
from soupq import version


setup(
    name='htmlq',
    description='Minimalistic CSS query library using lxml. Designed for testing HTML output (from Django, web.py, ...).',
    version=version,
    license='BSD',
    url='https://github.com/espenak/soupq',
    author='Espen Angell Kristiansen',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=[
        'lxml'
    ],
    include_package_data=True,
    long_description='See https://github.com/espenak/soupq',
    zip_safe=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Programming Language :: Python'
    ],
    test_suite='tests'
)
