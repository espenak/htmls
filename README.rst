#####
htmls
#####

.. image:: https://travis-ci.org/espenak/htmls.svg?branch=master
    :target: https://travis-ci.org/espenak/htmls

``htmls`` makes it easy to use CSS selectors with HTML in your unit tests.


***************
Getting started
***************

Requirements
============
Htmls requires `lxml <http://lxml.de/>`_. lxml requires libxml2 and libxslt,
so you have to install those libraries. You do not need to install lxml,
htmls will pull it in as a dependency.

Should work with any fairly new version of Python. Tested with Python 2.7 and Python 3.4.

Tip for Mac OSX
---------------
How to install libxml2 and libxslt is described in their docs, but their
docs does not mention that libxml2 and libxslt is available in Homebrew
for OSX. You can install them with::

    $ brew install libxml2 libxslt


Install
=======
When you have install libxml2 and libxslt, you can install htmls with:: 

    $ pip install htmls



*******
Example
*******
.. code:: python

    import unittest
    import htmls


    class ExampleTest(unittest.TestCase):
        def test_example(self):
            selector = htmls.S("""
            <html>
                <body>
                    <a href="#hello">Hello</a>
                    <a href="#cruel" class="btn btn-default btn-lg">
                        Cruel
                        World
                    </a>
                </body>
            </html>
            """)

            # Various ways of finding elements
            self.assertEquals(selector.count('a'), 2)
            button = selector.one('a.btn')  # Single htmls.Element
            with self.assertRaises(htmls.NotExactlyOneMatchError):
                button = selector.one('a')  # Fails because the a selector matches 2 elements.
            buttons = selector.list('a.btn')  # List of htmls.Element

            # Debugging
            print selector.prettify()  # Or selector.prettyprint()
            print button.prettify()  # Or button.prettyprint()

            # Find the text of an element with normalized whitespace
            self.assertEquals(selector.one('a.btn').text_normalized, 'Cruel World')

            # Working with CSS classes
            self.assertTrue(selector.one('a.btn').hasclass('btn-default'))
            self.assertTrue(selector.one('a.btn').hasclasses(['btn-default', 'btn-lg']))
            self.assertFalse(selector.one('a.btn').hasclasses(['btn-default', 'btn-lg', 'invalidclass']))

            # Working with attributes
            self.assertEquals(selector.one('a.btn')['href'], '#cruel')
            self.assertTrue(selector.one('a.btn').hasattribute('href'), '#cruel')


The example above is also available in ``tests/test_example.py``.


****
Docs
****
We have no HTML API docs at this time. This is a very small library,
it is less than 200 lines of well documented code. So just read ``htmls.py``,
or use ``pydoc htmls`` after you have installed the library.

Also check out the code in ``tests/test_htmls.py``. We have 100% test coverage,
and the tests are good examples.



*************************
Developing htmls
*************************

Setting up the development enviroment
=====================================

Create a virtualenv::

    $ pipenv install --dev


Running the tests
=================
Once you have created a development environment, run the tests with::

    $ pipenv run python setup.py test


Release
=======
1. Update the version in ``setup.py``.
2. Add releasenote to releasenotes folder on root with name `releasenotes-<major-version>.md`.
3. Commit with ``Release <version>``.
4. Tag the commit with ``<version>``.
5. Push (``git push && git push --tags``).
6. Release to pypi (``pipenv run python setup.py sdist && pipenv run twine upload dist/htmls-<version>.tar.gz``).
