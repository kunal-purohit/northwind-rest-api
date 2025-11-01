from ..database import db
from ..models import Customer


class CustomerService:
    @staticmethod
    def get_all():
        return Customer.query.all()

    @staticmethod
    def get_by_id(customer_id):
        return Customer.query.get(customer_id)

    @staticmethod
    def create(data):
        new_customer = Customer(**data)
        db.session.add(new_customer)
        db.session.commit()
        return new_customer

    @staticmethod
    def update(customer_id, data):
        customer = Customer.query.get(customer_id)
        if not customer:
            return None

        # Simple attribute update loop
        for key, value in data.items():
            setattr(customer, key, value)

        db.session.commit()
        return customer

    @staticmethod
    def delete(customer_id):
        customer = Customer.query.get(customer_id)
        if not customer:
            return False

        db.session.delete(customer)
        db.session.commit()
        return True
