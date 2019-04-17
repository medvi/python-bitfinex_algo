"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mbitfinex_algo` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``bitfinex_algo.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``bitfinex_algo.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import traceback
import datetime
import logging
import time
import sys

import mysql.connector
import yaml

from bitfinex_algo.queries import NEW_ORDER, ACTIVE_ORDER, UPDATE_ORDER_STATUS
from bitfinex_algo.exchange import MockExchange, OrderStatus


logger = logging.getLogger('bitfinex')


LEVELS = 'levels'
BUY_PRICE = 'buy-price'
SELL_PRICE = 'sell-price'
ORDER_SIZE = 'order-size'
ORDER_COUNT = 'order-count'
UPDATE_FREQUENCY = 'update-frequency'


class OrderController:
    """Класс управляет информацией об ордерах и их состоянии в бд"""

    def __enter__(self):
        self.cnx = mysql.connector.connect(
            user='root', password='root', port='3306',
            host='db', database='bitfinex_algo',
        )
        self.cursor = self.cnx.cursor(named_tuple=True)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.cnx.close()
        self.cursor.close()
        if exc_type:
            logger.error(f'exc_type: {exc_type}')
            logger.error(f'exc_value: {exc_value}')
            logger.error(f'exc_traceback: {exc_traceback}')

    def create_order(self, buy_price: int, sell_price: int, order_size: int):
        """Создать ордер на бирже и в бд"""

        now = datetime.datetime.now()
        params = {
            'symbol': 'tBITUSD',
            'mts_create': now,
            'mts_update': now + datetime.timedelta(seconds=10),
            'amount': order_size,
            'order_status': OrderStatus.ACTIVE.value,
        }

        extra_params = {'buy_price': buy_price, 'sell_price': sell_price}
        self.cursor.execute(NEW_ORDER, {**params, **extra_params})
        self.cnx.commit()

        extra_params = {
            'id': self.cursor.lastrowid,
            'price': buy_price if order_size > 0 else sell_price
        }
        MockExchange.new_order(**params, **extra_params)

    def update_orders(self):
        """
        Проверить текущее состояние активных ордеров и
        обновить его, если нужно
        """

        self.cursor.execute(ACTIVE_ORDER)
        active_orders = self.cursor.fetchall()

        now = datetime.datetime.now()
        orders_history = MockExchange.orders_history(
            now - datetime.timedelta(seconds=4),
            now
        )

        executed_orders_id = []
        for mock_order in orders_history:
            try:
                order = next(filter(
                    lambda x: x.id == mock_order.id,
                    active_orders
                ))
            except StopIteration:
                continue

            if order.amount > 0:
                logger.info(f'Ордер куплен по цене {mock_order.price}')
            else:
                logger.info(f'Ордер продан по цене {mock_order.price}')

            executed_orders_id.append((order.id, ))
            self.create_order(order.buy_price, order.sell_price, -order.amount)

        self.cursor.executemany(UPDATE_ORDER_STATUS, executed_orders_id)
        self.cnx.commit()


def load_config(path: str):
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError:
        logger.error(
            f'Invalid config.yaml structure:\n{traceback.format_exc()}'
        )
        return None


def validate_config(config: dict):
    if config is not None:
        for level in config[LEVELS]:
            for key, value in level.items():
                if not isinstance(value, int) or value <= 0:
                    logger.error(f'Invalid config.yaml values: {config}')
                    return None

    return config


def main(argv=sys.argv):
    """
    Args:
        argv (list): List of arguments

    Returns:
        int: A return code

    Parses the config.yaml and runs the trading robots.
    """

    config = validate_config(load_config('./config/config.yaml'))
    if config is None:
        return 2

    controller = OrderController()

    are_created = False
    while True:
        try:
            with controller:
                if not are_created:
                    for level in config[LEVELS]:
                        for _ in range(level[ORDER_COUNT]):
                            controller.create_order(
                                buy_price=level[BUY_PRICE],
                                sell_price=level[SELL_PRICE],
                                order_size=level[ORDER_SIZE],
                            )
                        are_created = True

                while True:
                    time.sleep(config[UPDATE_FREQUENCY])
                    controller.update_orders()
        except KeyboardInterrupt:
            logger.error(f'{traceback.format_exc()}')
            return 0
        except mysql.connector.errors.DatabaseError:
            logger.error(f'Database error:\n{traceback.format_exc()}\n')
            return 1
        except KeyError:
            logger.error(
                f'Invalid config.yaml structure:\n{traceback.format_exc()}\n'
            )
            return 2
        except (
            mysql.connector.errors.InterfaceError,
            ConnectionRefusedError
        ):
            logger.error(f'Database error:\n{traceback.format_exc()}\n')
            logger.error('Try to reconnect to the database...')
            time.sleep(3)
