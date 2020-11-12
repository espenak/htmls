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
        buttons = selector.list('a')  # List of htmls.Element
        self.assertEqual(len(buttons), 2)

        # Debugging
        print(selector.prettify())  # Or selector.prettyprint()
        print(button.prettify())  # Or button.prettyprint()

        # Find the text of an element with normalized whitespace
        self.assertEqual(selector.one('a.btn').text_normalized, 'Cruel World')

        # Working with CSS classes
        self.assertTrue(selector.one('a.btn').hasclass('btn-default'))
        self.assertTrue(selector.one('a.btn').hasclasses(['btn-default', 'btn-lg']))
        self.assertFalse(selector.one('a.btn').hasclasses(['btn-default', 'btn-lg', 'invalidclass']))

        # Working with attributes
        self.assertEqual(selector.one('a.btn')['href'], '#cruel')
        self.assertTrue(selector.one('a.btn').hasattribute('href'), '#cruel')
