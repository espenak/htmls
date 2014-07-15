import re
from lxml.html import tostring
from lxml.cssselect import CSSSelector
import html5lib


class NotExactlyOneMatchError(Exception):
    """
    Raised when :meth:`.Q.one` does not match exactly one element.
    """


def normalize_whitespace(text):
    """
    Normalize whitespace. Strips the string of whitespace in both ends,
    and replaces all consecutive whitespace characters (including tabs,
    newlines and nonbreak space) with a single space.
    """
    return re.sub('(\s|\\xa0)+', ' ', text).strip()


class Element(object):
    def __init__(self, element):
        self.element = element

    def __unicode__(self):
        return tostring(self.element)

    def __str__(self):
        return unicode(self).encode('utf-8')

    @property
    def tag(self):
        """
        Get the tag name of the element. Always lowecase.
        """
        return self.element.tag.lower()

    @property
    def text(self):
        """
        Get the the unicode text within text nodes of the element.
        """
        return self.element.text

    @property
    def text_normalized(self):
        """
        Get :meth:`.text`, normalized using :func:`.normalize_whitespace`.
        """
        return normalize_whitespace(self.element.text)

    def __getitem__(self, elementattribute):
        """
        Get the value of an attribute.
        """
        return self.element.attrib[elementattribute]

    @property
    def cssclasses(self):
        """
        Get the CSS classes as a list.
        """
        return re.split('\s+', self['class'])

    @property
    def cssclasses_set(self):
        """
        Get the CSS classes as a set.
        """
        return set(re.split('\s+', self['class']))

    def hasclass(self, cssclass):
        """
        Returns ``True`` if the given CSS class is among the CSS classes.
        """
        return cssclass in self.cssclasses

    def hasclasses(self, cssclasses):
        """
        Returns ``True`` if the given iterable of CSS classes is a subset
        of the CSS classes on this element.
        """
        cssclasses_set = set(cssclasses)
        return cssclasses_set.issubset(self.cssclasses_set)

    def hasattribute(self, attribute):
        """
        Returns ``True`` if the given attribute is among the attributes.
        """
        return attribute in self.element.attrib


class S(object):
    """
    An object that is optimized for testing HTML output
    with CSS selectors.
    """
    def __init__(self, html):
        """
        Parameters:
            html (string): A string/unicode containing HTML.
        """
        self.html = html
        self.parsed = self.parse_html()

    def parse_html(self, **kwargs):
        """
        Parse ``self.html``.

        Can be overridden to use a different parser than the default
        html5lib parser.

        Returns:
            A lxml ElementTree.
        """
        return html5lib.parse(self.html, treebuilder='lxml', namespaceHTMLElements=False)

    def __unicode__(self):
        return tostring(self.parsed)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def list(self, cssselector):
        """
        Get a list of elements matching the given CSS selector.

        Returns:
            List of :class:`.Element` objects.
        """
        selector = CSSSelector(cssselector)
        return map(Element, selector(self.parsed))

    def count(self, cssselector):
        """
        Get the number of elements matching the given CSS selector.
        """
        return len(self.list(cssselector))

    def exists(self, cssselector):
        """
        Returns ``True`` if the given CSS selector matches at least
        one element.
        """
        return bool(self.list(cssselector))
        
    def one(self, cssselector):
        """
        Get exactly one match for the given CSS selector.

        Throws:
            ValueError: If the given CSS selector does not match exactly one item.

        Returns:
            A :class:`.Element` matching the given CSS selector.
        """
        matches = self.list(cssselector)
        if len(matches) != 1:
            raise NotExactlyOneMatchError(
                '{!r} did not match a single element in '
                'the given HTML, it matched {} elements.'.format(
                    cssselector, len(matches)))
        else:
            return matches[0]
