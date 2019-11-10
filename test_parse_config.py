from unittest import TestCase
from unittest.mock import patch, mock_open

import parse_config

DEFAULT_CFG = '''
# this is a comment
    # a comment starting with spaces
    # followed by an empty line
           

# quid and pro should map to quo
quid pro quo
this for that
'''


class TestBirr(TestCase):

    def setUp(self) -> None:
        patcher = patch("builtins.open", mock_open(read_data=DEFAULT_CFG))
        self.addCleanup(patcher.stop)
        self.mock_open = patcher.start()
        self.urls = parse_config.parse()

    def test_parse_raises_if_file_does_not_exist(self):
        self.mock_open.side_effect = OSError("Boom!")
        with self.assertRaises(ValueError):
            # __next__ forces parsing
            parse_config.lines('this_file_does_not_exist').__next__()

    def test_parse_returns_a_dict(self):
        self.assertIsInstance(self.urls, dict)

    def test_parse_dict_has_at_least_one_entry(self):
        self.assertGreaterEqual(len(self.urls), 1)

    def test_parse_dict_has_key_quid(self):
        self.assertIn('quid', self.urls)

    def test_parse_quid_points_to_quo(self):
        self.assertEqual('quo', self.urls['quid'])

    def test_ignore_will_return_true_for_comments(self):
        self.assertTrue(parse_config.ignore('# comment'))
        self.assertTrue(parse_config.ignore(' # comment'))
        self.assertTrue(parse_config.ignore('   # comment'))

    def test_ignore_will_return_true_for_empty_lines(self):
        self.assertTrue(parse_config.ignore(''))
        self.assertTrue(parse_config.ignore('   '))

    def test_ignore_should_ignore_if_cant_tokenize(self):
        self.assertTrue(parse_config.ignore('just_one_value_with_no_spaces'))

    def test_break_line_returns_a_tuple(self):
        self.assertIsInstance(parse_config.break_line('this is a line'), tuple)

    def test_break_line_tuple_is_value_and_list(self):
        config_item = parse_config.break_line('this is a line')
        self.assertEqual(config_item[0], 'line')
        self.assertListEqual(config_item[1], ['this', 'is', 'a'])

    def test_list_to_keys(self):
        lk = parse_config.list_to_keys('value', ['a', 'b', 'c'])
        self.assertDictEqual(lk, {'a': 'value', 'b': 'value', 'c': 'value'})

    def test_parse_config(self):
        self.assertEqual('quo', self.urls['pro'])
        self.assertEqual('that', self.urls['this'])
