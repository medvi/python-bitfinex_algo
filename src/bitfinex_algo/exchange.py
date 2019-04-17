import logging
import datetime
from dataclasses import dataclass
from enum import Enum


logger = logging.getLogger('bitfinex')


class OrderStatus(Enum):
    ACTIVE = 'ACTIVE'
    EXECUTED = 'EXECUTED'


class MockExchange:
    """Mock для биржи"""

    @dataclass
    class MockOrder:
        id: int
        symbol: str
        mts_create: datetime.datetime
        mts_update: datetime.datetime
        amount: int
        order_status: OrderStatus
        price: int

    orders = []

    @staticmethod
    def new_order(
        id: int, symbol: str, mts_create: datetime.datetime,
        mts_update: datetime.datetime, amount: int,
        order_status: OrderStatus, price: int
    ):
        """Mock для создания ордера"""

        if amount > 0:
            logger.info(f'Ордер выставлен на покупку по цене {price}')
        else:
            logger.info(f'Ордер выставлен на продажу по цене {price}')

        MockExchange.orders.append(
            MockExchange.MockOrder(
                id=id, symbol=symbol, mts_create=mts_create,
                mts_update=mts_update, amount=amount,
                order_status=order_status, price=price
            )
        )

    @staticmethod
    def orders_history(start: datetime, end: datetime):
        """Mock для получения выполненных ордеров"""

        try:
            now = datetime.datetime.now()
            delta = datetime.timedelta(seconds=10)
            return filter(
                lambda x: start <= x.mts_update <= end and
                       x.mts_update < now + delta,
                MockExchange.orders
            )
        except StopIteration:
            pass
