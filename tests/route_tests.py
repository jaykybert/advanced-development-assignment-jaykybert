# Standard Libraries
import unittest
from main import app


class FlaskRoutesTestCase(unittest.TestCase):
    """
    Contains tests for testing website routes and the content they display.
    """

    def test_homepage_route(self):
        """
        Test that the homepage loads and returns a status
        200 (OK) code.
        """
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_homepage_content(self):
        """
        Test that the homepage displays the correct template content.
        :return:
        """
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertTrue(b'Welcome' in response.data)

    def test_products_page_route(self):
        """
        Test that the products page loads and returns a status
        200 (OK) code.
        """
        tester = app.test_client(self)
        response = tester.get('/products', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_products_page_content(self):
        """
        Test that the products page displays the correct template content.
        """
        tester = app.test_client(self)
        response = tester.get('/products', content_type='html/text')
        self.assertTrue(b'Products' in response.data)

    def test_about_us_page_route(self):
        """
        Test that the about us page loads and returns a status
        200 (OK) code.
        """
        tester = app.test_client(self)
        response = tester.get('/about', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_about_us_page_content(self):
        """
        Test that the about us page displays the correct template content.
        """
        tester = app.test_client(self)
        response = tester.get('/about', content_type='html/text')
        self.assertTrue(b'About Us' in response.data)

    def test_account_page_route(self):
        """
        Test that the account page loads and returns a status
        200 (OK) code.
        """
        tester = app.test_client(self)
        response = tester.get('/account', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_account_page_content(self):
        """
        Test that the account page displays the correct template content.
        """
        tester = app.test_client(self)
        response = tester.get('/account', content_type='html/text')
        # Compare with web-page content for logged in and logged out states.
        self.assertTrue(b'Hello' in response.data or b'log in' in response.data)
