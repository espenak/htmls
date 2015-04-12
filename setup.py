from setuptools import setup, find_packages


setup(
    name='htmls',
    description='Makes it easy to write use CSS selectors with HTML in your unit tests.',
    version='0.9.6',
    license='BSD',
    url='https://github.com/espenak/htmls',
    author='Espen Angell Kristiansen',
    author_email='post@espenak.net',
    packages=find_packages(),
    install_requires=[
        'lxml',
        'html5lib',
        'cssselect',
        'future'
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
