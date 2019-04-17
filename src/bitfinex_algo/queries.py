NEW_ORDER = '''
    INSERT INTO bitfinex_algo.Orders
        (symbol, mts_create, mts_update, amount, 
         order_status, buy_price, sell_price)
    VALUES (
        %(symbol)s, %(mts_create)s, %(mts_update)s, %(amount)s, 
        %(order_status)s, %(buy_price)s, %(sell_price)s
    );
'''

ACTIVE_ORDER = '''
    SELECT * FROM bitfinex_algo.Orders 
    WHERE order_status='ACTIVE';
'''

UPDATE_ORDER_STATUS = '''
    UPDATE bitfinex_algo.Orders 
    SET order_status='EXECUTED' 
    WHERE id=%s;
'''
