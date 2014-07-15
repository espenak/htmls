from setuptools import setup, find_packages


setup(
    name='htmls',
    description=(
        'Minimalistic CSS query library using lxml. Designed for unit '
        'testing of HTML output (from Django, web.py, ...).'),
    version='0.9',
    license='BSD',
    url='https://github.com/espenak/htmls',
    author='Espen Angell Kristiansen',
    packages=find_packages(),
    install_requires=[
        'lxml',
        'html5lib',
    ],
    include_package_data=True,
    long_description='See https://github.com/espenak/htmls',
    zip_safe=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Programming Language :: Python'
    ],
    test_suite='tests'
)
