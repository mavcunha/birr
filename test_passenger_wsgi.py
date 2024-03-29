import unittest
from mock import patch, Mock

import passenger_wsgi


@patch("passenger_wsgi.parse", return_value={'key': 'value', 'default': 'default_response'})
class PassengerWsgiTestCase(unittest.TestCase):

    def setUp(self):
        self.response = Mock()

    def test_redirect_to_default_if_path_is_empty(self, parse):
        passenger_wsgi.application({'PATH_INFO': ''}, self.response)
        self.response.assert_called_with('303 See Other', [('Location', 'default_response')])

    def test_redirect_to_default_if_path_is_missing(self, parse):
        passenger_wsgi.application({}, self.response)
        self.response.assert_called_with('303 See Other', [('Location', 'default_response')])

    def test_redirect_to_default_if_path_is_default(self, parse):
        passenger_wsgi.application({'PATH_INFO': 'default'}, self.response)
        self.response.assert_called_with('303 See Other', [('Location', 'default_response')])

    def test_valid_path_returns_false_for_invalid(self, parse):
        paths = ['/some/path', '/ ', '/  ', '/$#@', '/?this=that', '   ']
        for p in paths:
            self.assertFalse(passenger_wsgi.valid_key(p), 'fail={}'.format(p))

    def test_valid_path_returns_true_for_valid(self, parse):
        paths = ['this', 'somenumber123', '123number']
        for p in paths:
            self.assertTrue(passenger_wsgi.valid_key(p), 'fail={}'.format(p))

    def test_with_path_returns_valid_path_without_leading_slash(self, parse):
        self.assertFalse('/' in passenger_wsgi.clean_path('//this//'))

    def test_not_redirect_if_not_found(self, parse):
        passenger_wsgi.application({'PATH_INFO': '/non-existent'}, self.response)
        self.response.assert_called_with('404 Not Found', [('Content-type', 'text/plain')])

    def test_redirects_if_key_found(self, parse):
        passenger_wsgi.application({'PATH_INFO': '/key'}, self.response)
        self.response.assert_called_with('303 See Other', [('Location', 'value')])


if __name__ == '__main__':
    unittest.main()
