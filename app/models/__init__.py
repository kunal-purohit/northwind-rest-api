from .customer import Customer
from .product import Product
from .order import Order, OrderDetail

from .customer import CustomerSchema
from .product import ProductSchema
from .order import OrderDetailSchema, OrderSchema

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
