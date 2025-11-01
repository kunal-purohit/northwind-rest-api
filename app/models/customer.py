from ..database import db, ma
from marshmallow import fields, validate


class Customer(db.Model):
    __tablename__ = "Customers"

    CustomerID = db.Column(db.String(5), primary_key=True)
    CompanyName = db.Column(db.String(40), nullable=False)
    ContactName = db.Column(db.String(30))
    ContactTitle = db.Column(db.String(30))
    Address = db.Column(db.String(60))
    City = db.Column(db.String(15))
    Region = db.Column(db.String(15))
    PostalCode = db.Column(db.String(10))
    Country = db.Column(db.String(15))
    Phone = db.Column(db.String(24))
    Fax = db.Column(db.String(24))

    # Relationship to Orders
    orders = db.relationship("Order", backref="customer", lazy="dynamic")

    def __repr__(self):
        return f"<Customer {self.CustomerID} ({self.CompanyName})>"


class CustomerSchema(ma.Schema):
    CustomerID = fields.String(
        required=True,
        validate=validate.Length(equal=5, error="CustomerID must be 5 characters."),
    )
    CompanyName = fields.String(required=True)
    ContactName = fields.String()
    ContactTitle = fields.String()
    Address = fields.String()
    City = fields.String()
    Region = fields.String()
    PostalCode = fields.String()
    Country = fields.String()
    Phone = fields.String()
    Fax = fields.String()
