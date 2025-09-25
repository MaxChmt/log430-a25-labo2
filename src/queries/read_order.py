"""
Orders (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from collections import defaultdict
from db import get_sqlalchemy_session, get_redis_conn
from sqlalchemy import desc
from models.order import Order

def get_order_by_id(order_id):
    """Get order by ID from Redis"""
    r = get_redis_conn()
    return r.hgetall(order_id)

def get_orders_from_mysql(limit=9999):
    """Get last X orders"""
    session = get_sqlalchemy_session()
    return session.query(Order).order_by(desc(Order.id)).limit(limit).all()

def get_orders_from_redis(limit=9999):
    """Get last X orders"""
    r = get_redis_conn()
    order_keys = sorted(r.keys("order:*"), reverse=True)[:limit]
    orders = []
    for key in order_keys:
        orders.append(r.hgetall(key))
    return orders

def get_highest_spending_users():
    """Get report of best spender users"""
    user_map = {1: "Ada Lovelace", 2: "Adele Goldberg", 3: "Alan Turing"}
    r = get_redis_conn()
    expenses_by_user = defaultdict(float)
    order_keys = sorted(r.keys("order:*"), reverse=True)
    orders = []
    for key in order_keys:
        orders.append(r.hgetall(key))
    for order in orders:
        expenses_by_user[user_map.get(int(order['user_id']))] += float(order['total_amount'])
    highest_spending_users = sorted(expenses_by_user.items(), key=lambda item: item[1], reverse=True)
    return highest_spending_users

def get_highest_sold_items():
    """Get report of best selling products"""
    known_prices = [1999.99, 5.75, 299.75, 59.5]
    r = get_redis_conn()
    expenses_by_item = defaultdict(float)
    order_keys = sorted(r.keys("order:*"), reverse=True)
    orders = []
    for key in order_keys:
        orders.append(r.hgetall(key))
    for order in orders:
        for price in known_prices:
            amount = float(order['total_amount']) // price
            rest = float(order['total_amount']) % price
            if abs(rest) < 1e-2:
                expenses_by_item[price] += amount
                break
    highest_sold_items = sorted(expenses_by_item.items(), key=lambda item: item[1], reverse=True)
    return highest_sold_items

def get_highest_sold_items_redis():
    """Get report of best selling products from Redis"""
    r = get_redis_conn()
    product_keys = r.keys("product:*")
    products = []

    for key in product_keys:
        product_id = key.split(":")[1]
        quantity = int(r.get(key))
        products.append((product_id, quantity))
    highest_sold_items = sorted(products, key=lambda item: item[1], reverse=True)
    return highest_sold_items