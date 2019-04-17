import logging
import unittest

from bitfinex_algo.cli import load_config, validate_config
from bitfinex_algo import cli as c

logger = logging.getLogger('bitfinex')


class ConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    def test_load_config(self):
        self.assertIsNone(load_config('tests/config/invalid_config_1.yaml'))

        self.assertDictEqual(
            validate_config(load_config('tests/config/valid_config_5.yaml')),
            {
                c.LEVELS: [{
                    c.BUY_PRICE: 95,
                    c.SELL_PRICE: 100,
                    c.ORDER_SIZE: 100,
                    c.ORDER_COUNT: 2
                }, {
                    c.BUY_PRICE: 100,
                    c.SELL_PRICE: 105,
                    c.ORDER_SIZE: 100,
                    c.ORDER_COUNT: 1
                }],
                c.UPDATE_FREQUENCY: 3,
            }
        )

    def test_validate_config(self):
        for i in range(2, 5):
            with self.subTest(i=i):
                config = load_config(f'tests/config/invalid_config_{i}.yaml')
                self.assertIsNone(validate_config(config))
