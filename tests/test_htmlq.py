import unittest

import htmlq


class TestHtmlq(unittest.TestCase):
    def test_list(self):
        self.assertEquals(
            len(htmlq.Q('<a class="btn">Tst</a>').list('a')), 1)

    def test_one(self):
        with self.assertRaises(htmlq.NotExactlyOneMatchError):
            htmlq.Q('<a class="btn">Tst</a><a class="link">Tst2</a>').one('a')
        with self.assertRaises(htmlq.NotExactlyOneMatchError):
            htmlq.Q('').one('a')

    def test_count(self):
        self.assertEquals(
            1,
            htmlq.Q('<a class="btn">Tst</a><a class="link">Tst2</a>').count('a.btn'))
        self.assertEquals(
            0,
            htmlq.Q('<a class="btn">Tst</a><a class="link">Tst2</a>').count('a.btn-lg'))

    def test_exists(self):
        self.assertTrue(
            htmlq.Q('<a class="btn">Tst</a><a class="link">Tst2</a>').exists('a.btn'))
        self.assertFalse(
            htmlq.Q('<a class="btn">Tst</a><a class="link">Tst2</a>').exists('a.btn-lg'))

    def test_cssclasses(self):
        self.assertEquals(
            ['btn'],
            htmlq.Q('<a class="btn">Tst</a>').one('a').cssclasses)
        self.assertEquals(
            ['btn', 'btn-default'],
            htmlq.Q('<a class="btn btn-default">Tst</a>').one('a').cssclasses)

    def test_cssclasses_set(self):
        self.assertEquals(
            set(['btn']),
            htmlq.Q('<a class="btn">Tst</a>').one('a').cssclasses_set)
        self.assertEquals(
            set(['btn', 'btn-default']),
            htmlq.Q('<a class="btn btn-default">Tst</a>').one('a').cssclasses_set)

    def test_hasclass(self):
        self.assertTrue(
            htmlq.Q('<a class="btn">Tst</a>').one('a').hasclass('btn'))
        self.assertFalse(
            htmlq.Q('<a class="btn">Tst</a>').one('a').hasclass('link'))

    def test_hasclasses(self):
        self.assertTrue(
            htmlq.Q('<a class="btn btn-default btn-lg">Tst</a>').one('a').hasclasses(
                ['btn', 'btn-default']))
        self.assertTrue(
            htmlq.Q('<a class="btn btn-default btn-lg">Tst</a>').one('a').hasclasses(
                ['btn', 'btn-default', 'btn-lg']))
        self.assertFalse(
            htmlq.Q('<a class="btn btn-default btn-lg">Tst</a>').one('a').hasclasses(
                ['btn', 'otherclass']))

    def test_hasattribute(self):
        self.assertTrue(
            htmlq.Q('<a class="btn">Tst</a>').one('a').hasattribute('class'))
        self.assertFalse(
            htmlq.Q('<a class="btn">Tst</a>').one('a').hasattribute('href'))

    def test_text(self):
        self.assertEquals(
            'Tst',
            htmlq.Q('<a class="btn">Tst</a>').one('a').text)

    def test_tag(self):
        self.assertEquals(
            'a',
            htmlq.Q('<a class="btn">Tst</a>').one('a').tag)

    def test_text_normalized(self):
        self.assertEquals(
            'Hello world',
            htmlq.Q('<a class="btn">Hello world</a>').one('a').text_normalized)
        self.assertEquals(
            'Hello world',
            htmlq.Q('<a class="btn">   Hello\n\tworld\n\t</a>').one('a').text_normalized)
