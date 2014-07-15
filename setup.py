from setuptools import setup, find_packages


setup(
    name='htmlq',
    description='Minimalistic CSS query library using lxml. Designed for testing HTML output (from Django, web.py, ...).',
    version='0.9',
    license='BSD',
    url='https://github.com/espenak/soupq',
    author='Espen Angell Kristiansen',
    packages=find_packages(),
    install_requires=[
        'lxml',
        'html5lib',
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
