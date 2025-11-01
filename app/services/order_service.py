from ..database import db
from ..models import Order, OrderDetail, orders_schema, Customer
from sqlalchemy import desc


class OrderService:
    @staticmethod
    def get_all():
        return Order.query.all()

    @staticmethod
    def get_by_id(order_id):
        return Order.query.filter_by(OrderID=order_id).first()

    @staticmethod
    def create(data):
        details_data = data.pop("details", [])

        new_order = Order(**data)

        for detail in details_data:
            new_detail = OrderDetail(**detail)
            new_order.details.append(new_detail)

        db.session.add(new_order)
        db.session.commit()
        return new_order

    @staticmethod
    def update(order_id, data):
        order = Order.query.get(order_id)
        if not order:
            return None

        data.pop("details", None)

        # Simple attribute update loop
        for key, value in data.items():
            setattr(order, key, value)

        db.session.commit()
        return order

    @staticmethod
    def delete(order_id):
        order = Order.query.get(order_id)
        if not order:
            return False

        db.session.delete(order)
        db.session.commit()
        return True

    @staticmethod
    def get_customer_history(customer_id):
        if not Customer.query.get(customer_id):
            return None

        history = (
            Order.query.filter_by(CustomerID=customer_id)
            .order_by(desc(Order.OrderDate))
            .all()
        )

        return orders_schema.dump(history)
