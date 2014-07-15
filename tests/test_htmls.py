import unittest

import htmls


class TestHtmls(unittest.TestCase):
    def test_list(self):
        self.assertEquals(
            len(htmls.S('<a class="btn">Tst</a>').list('a')), 1)

    def test_one(self):
        with self.assertRaises(htmls.NotExactlyOneMatchError):
            htmls.S('<a class="btn">Tst</a><a class="link">Tst2</a>').one('a')
        with self.assertRaises(htmls.NotExactlyOneMatchError):
            htmls.S('').one('a')

    def test_count(self):
        self.assertEquals(
            1,
            htmls.S('<a class="btn">Tst</a><a class="link">Tst2</a>').count('a.btn'))
        self.assertEquals(
            0,
            htmls.S('<a class="btn">Tst</a><a class="link">Tst2</a>').count('a.btn-lg'))

    def test_exists(self):
        self.assertTrue(
            htmls.S('<a class="btn">Tst</a><a class="link">Tst2</a>').exists('a.btn'))
        self.assertFalse(
            htmls.S('<a class="btn">Tst</a><a class="link">Tst2</a>').exists('a.btn-lg'))

    def test_cssclasses(self):
        self.assertEquals(
            ['btn'],
            htmls.S('<a class="btn">Tst</a>').one('a').cssclasses)
        self.assertEquals(
            ['btn', 'btn-default'],
            htmls.S('<a class="btn btn-default">Tst</a>').one('a').cssclasses)

    def test_cssclasses_set(self):
        self.assertEquals(
            set(['btn']),
            htmls.S('<a class="btn">Tst</a>').one('a').cssclasses_set)
        self.assertEquals(
            set(['btn', 'btn-default']),
            htmls.S('<a class="btn btn-default">Tst</a>').one('a').cssclasses_set)

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
        self.assertEquals(
            'Tst',
            htmls.S('<a class="btn">Tst</a>').one('a').text)

    def test_tag(self):
        self.assertEquals(
            'a',
            htmls.S('<a class="btn">Tst</a>').one('a').tag)

    def test_text_normalized(self):
        self.assertEquals(
            'Hello world',
            htmls.S('<a class="btn">Hello world</a>').one('a').text_normalized)
        self.assertEquals(
            'Hello world',
            htmls.S('<a class="btn">   Hello\n\tworld\n\t</a>').one('a').text_normalized)
