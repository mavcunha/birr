import string
import unittest
from unittest import mock
from unittest.mock import Mock

import passenger_wsgi


class PassengerWsgiTestCase(unittest.TestCase):


    def test_application_redirects(self):
        response = Mock()

        passenger_wsgi.application({'PATH_INFO': ''}, response)

        response.assert_called_with('303 See Other', mock.ANY)

    def test_application_uses_path_info(self):
        response = Mock()
        env = {'PATH_INFO': '/some/path'}
        passenger_wsgi.application(env, response)
        response.assert_called_with(mock.ANY, [('Location', '/some/path')])

    def test_valid_path_returns_false_for_invalid(self):
        paths = ['/some/path', '/ ', '/  ', '/$#@', '/?this=that', '   ']
        for p in paths:
            self.assertFalse(passenger_wsgi.valid_path(p), f'fail={p}')

    def test_valid_path_returns_true_for_valid(self):
        paths = ['this', 'somenumber123', '123number']
        for p in paths:
            self.assertTrue(passenger_wsgi.valid_path(p), f'fail={p}')

    def test_with_path_returns_valid_path_without_leading_slash(self):
        self.assertFalse(passenger_wsgi.with_path('/this').startswith('/'))


if __name__ == '__main__':
    unittest.main()
