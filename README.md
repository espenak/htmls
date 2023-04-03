# htmls

## Usage

### Requirements
Htmls requires `lxml <http://lxml.de/>`. lxml requires libxml2 and libxslt,
so you have to install those libraries. You do not need to install lxml,
htmls will pull it in as a dependency.

Tested with Python 3.8 and 3.10.

#### Tip for Mac OSX
How to install libxml2 and libxslt is described in their docs, but their
docs does not mention that libxml2 and libxslt is available in Homebrew
for OSX. You can install them with::
```
$ brew install libxml2 libxslt
```

### Install
When you have install libxml2 and libxslt, you can install htmls with:: 
```
$ pip install htmls
```

#### Usage example
```python
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
        self.assertEqual(selector.count('a'), 2)
        button = selector.one('a.btn')  # Single htmls.Element
        with self.assertRaises(htmls.NotExactlyOneMatchError):
            button = selector.one('a')  # Fails because the a selector matches 2 elements.
        buttons = selector.list('a.btn')  # List of htmls.Element

        # Debugging
        print selector.prettify()  # Or selector.prettyprint()
        print button.prettify()  # Or button.prettyprint()

        # Find the text of an element with normalized whitespace
        self.assertEqual(selector.one('a.btn').text_normalized, 'Cruel World')

        # Working with CSS classes
        self.assertTrue(selector.one('a.btn').hasclass('btn-default'))
        self.assertTrue(selector.one('a.btn').hasclasses(['btn-default', 'btn-lg']))
        self.assertFalse(selector.one('a.btn').hasclasses(['btn-default', 'btn-lg', 'invalidclass']))

        # Working with attributes
        self.assertEqual(selector.one('a.btn')['href'], '#cruel')
        self.assertTrue(selector.one('a.btn').hasattribute('href'), '#cruel')
```

The example above is also available in ``tests/test_example.py``.

## Develop
### Use conventional commits for GIT commit messages
See https://www.conventionalcommits.org/en/v1.0.0/.
You can use this git commit message format in many different ways, but the easiest is:

- Use commitizen: https://commitizen-tools.github.io/commitizen/commit/
- Use an editor extension, like https://marketplace.visualstudio.com/items?itemName=vivaxy.vscode-conventional-commits for VScode.
- Just learn to write the format by hand (can be error prone to begin with, but it is fairly easy to learn).


### Install hatch and commitizen
NOTE: You only need hatch if you need to build releases, and you
only need commitizen for releases OR to make it easy to follow
conventional commits for your commit messages
(see _Use conventional commits for GIT commit messages_ above).

First install pipx with:
```
$ brew install pipx
$ pipx ensurepath
```

Then install hatch and commitizen:
```
$ pipx install hatch 
$ pipx install commitizen
```

See https://github.com/pypa/pipx, https://hatch.pypa.io/latest/install/
and https://commitizen-tools.github.io/commitizen/ for more install alternatives if
needed, but we really recommend using pipx since that is isolated.


### Install development dependencies

Install a local python version with pyenv:
```
$ pyenv install 3.10
$ pyenv local 3.10
```

Create virtualenv:
```
$ ./recreate-virtualenv.sh
```

> Alternatively, create virtualenv manually (this does the same as recreate-virtualenv.sh):
> ```
> $ python -m venv .venv
> ```

Install dependencies in a virtualenv:
```
$ .venv/bin/pip install -v ".[dev,test]"
```

### Tests
```
$ pytest
```

## Documentation
We have no HTML API docs at this time. This is a very small library,
it is less than 200 lines of well documented code. So just read ``htmls.py``,
or use ``pydoc htmls`` after you have installed the library.

Also check out the code in ``tests/test_htmls.py``. We have 100% test coverage,
and the tests are good examples.


## How to release htmls

Release (create changelog, increment version, commit and tag the change) with:
```
$ cz bump
$ git push && git push --tags
```

NOTE:
- ``cz bump`` only works if conventional commits (see section about that above) is used.
- ``cz bump`` can take a specific version etc, but it automatically select the correct version
  if conventional commits has been used correctly. See https://commitizen-tools.github.io/commitizen/.
- The ``cz`` command comes from ``commitizen`` (install documented above).

Release to pypi:
```
$ hatch build -t sdist
$ hatch publish
$ rm dist/*              # optional cleanup
```
