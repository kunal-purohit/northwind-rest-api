from ..database import db, ma
from marshmallow import fields, validate


class Product(db.Model):
    __tablename__ = "Products"

    ProductID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProductName = db.Column(db.String(100))
    SupplierID = db.Column(db.Integer)
    CategoryID = db.Column(db.Integer)
    QuantityPerUnit = db.Column(db.String(50))
    UnitPrice = db.Column(db.Numeric(10, 2))
    UnitsInStock = db.Column(db.SmallInteger)
    UnitsOnOrder = db.Column(db.SmallInteger)
    ReorderLevel = db.Column(db.SmallInteger)
    Discontinued = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Product {self.ProductID} ({self.ProductName})>"


class ProductSchema(ma.Schema):
    ProductID = fields.Integer()
    ProductName = fields.String(required=True)
    SupplierID = fields.Integer()
    CategoryID = fields.Integer()
    QuantityPerUnit = fields.String()
    UnitPrice = fields.Decimal(
        places=2,
        validate=validate.Range(min=0, error="Unit price must be positive."),
    )
    UnitsInStock = fields.Integer()
    UnitsOnOrder = fields.Integer()
    ReorderLevel = fields.Integer()
    Discontinued = fields.Boolean()
