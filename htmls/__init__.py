from builtins import str
from builtins import map
from builtins import object
import re
import textwrap
from xml.sax.saxutils import quoteattr
from lxml.html import tostring
from lxml.cssselect import CSSSelector
import html5lib


__version__ = "3.0.0"


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
    return re.sub(r'(\s|\\xa0)+', ' ', text).strip()


def encode_attributes(iterable):
    """
    Encode an iterable of ``(attributename, attributevalue)`` pairs
    as XML attibutes.

    Example:

        >>> encode_attributes([('class', 'btn')]) == 'class="btn"'
        True
    """
    return ' '.join([
        u'{}={}'.format(attribute, quoteattr(value))
        for attribute, value in iterable])


def prettify_text(text, indent=''):
    """
    Dedent and reindent the given text.

    Example:

        >>> prettify_text('   Test') == 'Test'
        True
        >>> prettify_text('       Test', indent='  ') == '  Test'
        True
    """
    text = textwrap.dedent(text).strip()
    out = []
    for line in text.split('\n'):
        out.append(u'{}{}'.format(indent, line))
    return u'\n'.join(out)


class PrettifyElement(object):
    def __init__(self, element, indentspace='    '):
        self.indentspace = indentspace
        self.out = []
        self._prettify_element(element)

    def _prettify_element(self, element, indentcount=0):
        indent = self.indentspace * indentcount
        if element.tag:
            attributes = u''
            if element.attrib:
                attributes = u' {}'.format(encode_attributes(list(element.items())))
            self.out.append(u'{indent}<{tag}{attributes}>'.format(
                indent=indent, tag=element.tag, attributes=attributes))
        if element.text and element.text.strip():
            textindent = indent
            if element.tag and element.text:
                # Make sure we indent correctly when we have a tag with
                # text as only child
                textindent = indent + self.indentspace
            text = prettify_text(element.text, textindent)
            self.out.append(text)
        for childelement in element.getchildren():
            self._prettify_element(childelement, indentcount=indentcount + 1)

        if element.tag:
            self.out.append(u'{}</{}>'.format(indent, element.tag))

        # Handle text between two elements (below the current element)
        if element.tail and element.tail.strip():
            text = prettify_text(element.tail, indent)
            self.out.append(text)

    def __str__(self):
        return u'\n'.join(self.out)


def _get_all_text_in_element(rootelement):
    alltext = []

    def _collect_text_in_element(element, root=True):
        if element.text and element.text.strip():
            alltext.append(element.text)
        for childelement in element.getchildren():
            _collect_text_in_element(childelement, root=False)
        if not root and element.tail and element.tail.strip():
            alltext.append(element.tail)

    _collect_text_in_element(rootelement)
    return alltext


class Element(object):
    def __init__(self, element):
        self.element = element

    def __str__(self):
        return tostring(self.element)

    def prettify(self, **kwargs):
        return str(PrettifyElement(self.element, **kwargs))

    def prettyprint(self):
        print(self.prettify())

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

    @property
    def alltext(self):
        """
        Get all text within this element and all child elements.

        Iterates over all the text nodes within this element, including any
        text nodes in child nodes and joins them into a single string.
        """
        alltext = u''.join(_get_all_text_in_element(self.element))
        return alltext

    @property
    def alltext_normalized(self):
        """
        Get :meth:`.alltext`, normalized using :func:`.normalize_whitespace`.
        """
        return normalize_whitespace(self.alltext).strip()

    def __getitem__(self, elementattribute):
        """
        Get the value of an attribute.
        """
        return self.element.attrib[elementattribute]

    def get(self, elementattribute, default=None):
        """
        Get the value of an attribute, defaulting to ``default``.
        """
        return self.element.get(elementattribute, default)

    @property
    def cssclasses(self):
        """
        Get the CSS classes as a list.
        """
        return re.split(r'\s+', self['class'].strip())

    @property
    def cssclasses_set(self):
        """
        Get the CSS classes as a set.
        """
        return set(re.split(r'\s+', self['class'].strip()))

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

    def __str__(self):
        return tostring(self.parsed)

    def prettify(self, **kwargs):
        return str(PrettifyElement(self.parsed.getroot(), **kwargs))

    def prettyprint(self):
        print(self.prettify())

    def list(self, cssselector):
        """
        Get a list of elements matching the given CSS selector.

        Returns:
            List of :class:`.Element` objects.
        """
        selector = CSSSelector(cssselector)
        return list(map(Element, selector(self.parsed)))

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
