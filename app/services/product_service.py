from ..database import db
from ..models import Product


class ProductService:
    @staticmethod
    def get_all():
        return Product.query.all()

    @staticmethod
    def get_by_id(product_id):
        return Product.query.get(product_id)

    @staticmethod
    def create(data):
        if "Discontinued" in data:
            data["Discontinued"] = bool(data["Discontinued"])

        new_product = Product(**data)
        db.session.add(new_product)
        db.session.commit()
        return new_product

    @staticmethod
    def update(product_id, data):
        product = Product.query.get(product_id)
        if not product:
            return None

        # Simple attribute update loop
        for key, value in data.items():
            if key == "Discontinued":
                setattr(product, key, bool(value))
            else:
                setattr(product, key, value)

        db.session.commit()
        return product

    @staticmethod
    def delete(product_id):
        product = Product.query.get(product_id)
        if not product:
            return False

        db.session.delete(product)
        db.session.commit()
        return True
