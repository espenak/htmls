import unittest
import doctest
import htmls


class TestHtmls(unittest.TestCase):
    def test_list(self):
        self.assertEqual(
            len(htmls.S('<a class="btn">Tst</a>').list('a')), 1)

    def test_one(self):
        with self.assertRaises(htmls.NotExactlyOneMatchError):
            htmls.S('<a class="btn">Tst</a><a class="link">Tst2</a>').one('a')
        with self.assertRaises(htmls.NotExactlyOneMatchError):
            htmls.S('').one('a')

    def test_count(self):
        self.assertEqual(
            1,
            htmls.S('<a class="btn">Tst</a><a class="link">Tst2</a>').count('a.btn'))
        self.assertEqual(
            0,
            htmls.S('<a class="btn">Tst</a><a class="link">Tst2</a>').count('a.btn-lg'))

    def test_exists(self):
        self.assertTrue(
            htmls.S('<a class="btn">Tst</a><a class="link">Tst2</a>').exists('a.btn'))
        self.assertFalse(
            htmls.S('<a class="btn">Tst</a><a class="link">Tst2</a>').exists('a.btn-lg'))

    def test_cssclasses(self):
        self.assertEqual(
            ['btn'],
            htmls.S('<a class="btn">Tst</a>').one('a').cssclasses)
        self.assertEqual(
            ['btn', 'btn-default'],
            htmls.S('<a class="btn btn-default">Tst</a>').one('a').cssclasses)

    def test_cssclasses_extra_whitespace(self):
        self.assertEqual(
            ['btn'],
            htmls.S('<a class="  btn  ">Tst</a>').one('a').cssclasses)
        self.assertEqual(
            ['btn', 'btn-default'],
            htmls.S('<a class="   btn  btn-default  ">Tst</a>').one('a').cssclasses)

    def test_cssclasses_set(self):
        self.assertEqual(
            set(['btn']),
            htmls.S('<a class="btn">Tst</a>').one('a').cssclasses_set)
        self.assertEqual(
            set(['btn', 'btn-default']),
            htmls.S('<a class="btn btn-default">Tst</a>').one('a').cssclasses_set)

    def test_cssclasses_set_extra_whitespace(self):
        self.assertEqual(
            set(['btn']),
            htmls.S('<a class="  btn  ">Tst</a>').one('a').cssclasses_set)
        self.assertEqual(
            set(['btn', 'btn-default']),
            htmls.S('<a class="  btn  btn-default  ">Tst</a>').one('a').cssclasses_set)

    def test_hasclass(self):
        self.assertTrue(
            htmls.S('<a class="btn">Tst</a>').one('a').hasclass('btn'))
        self.assertFalse(
            htmls.S('<a class="btn">Tst</a>').one('a').hasclass('link'))

    def test_hasclasses(self):
        self.assertTrue(
            htmls.S('<a class="btn btn-default btn-lg">Tst</a>').one('a').hasclasses(
                ['btn', 'btn-default']))
        self.assertTrue(
            htmls.S('<a class="btn btn-default btn-lg">Tst</a>').one('a').hasclasses(
                ['btn', 'btn-default', 'btn-lg']))
        self.assertFalse(
            htmls.S('<a class="btn btn-default btn-lg">Tst</a>').one('a').hasclasses(
                ['btn', 'otherclass']))

    def test_hasattribute(self):
        self.assertTrue(
            htmls.S('<a class="btn">Tst</a>').one('a').hasattribute('class'))
        self.assertFalse(
            htmls.S('<a class="btn">Tst</a>').one('a').hasattribute('href'))

    def test_text(self):
        self.assertEqual(
            'Tst',
            htmls.S('<a>Tst</a>').one('a').text)

    def test_tag(self):
        self.assertEqual(
            'a',
            htmls.S('<a>Tst</a>').one('a').tag)

    def test_text_normalized(self):
        self.assertEqual(
            'Hello world',
            htmls.S('<a>Hello world</a>').one('a').text_normalized)
        self.assertEqual(
            'Hello world',
            htmls.S('<a>   Hello\n\tworld\n\t</a>').one('a').text_normalized)

    def test_alltext_normalized(self):
        self.assertEqual(
            'Hello world',
            htmls.S('<a>Hello world</a>').one('a').alltext_normalized)
        self.assertEqual(
            'Hello world. This is a test!',
            htmls.S("""
                <a>
                    <strong>Hello</strong> world.
                    <em>This is
                    a test</em>!
                </a>
            """).one('a').alltext_normalized)

    def test_prettify(self):
        pretty = htmls.S("""
            <html>
            <body>
                <a class="btn">Hello world</a>
                This is a test!
                <ul>
                <li>A test</li>
            <li>Another test</li>
                    </ul>
            </body>
            </html>
        """).prettify()
        self.assertEqual(
            pretty,
            ('<html>\n'
             '    <head>\n'
             '    </head>\n'
             '    <body>\n'
             '        <a class="btn">\n'
             '            Hello world\n'
             '        </a>\n'
             '        This is a test!\n'
             '        <ul>\n'
             '            <li>\n'
             '                A test\n'
             '            </li>\n'
             '            <li>\n'
             '                Another test\n'
             '            </li>\n'
             '        </ul>\n'
             '    </body>\n'
             '</html>'))

    def test_encode_attributes(self):
        self.assertEqual(
            htmls.encode_attributes([('a', '10'), ('b', "Hello")]),
            'a="10" b="Hello"'
        )

    def test_encode_attributes_quotes(self):
        self.assertEqual(
            htmls.encode_attributes([
                ('a', 'A "test"'),
                ('b', "Another 'test'")
            ]),
            'a=\'A "test"\' b="Another \'test\'"'
        )


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(htmls))
    return tests
