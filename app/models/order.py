from ..database import db, ma
from marshmallow import fields


class OrderDetail(db.Model):
    __tablename__ = "OrderDetails"

    OrderID = db.Column(db.Integer, db.ForeignKey("Orders.OrderID"), primary_key=True)
    ProductID = db.Column(
        db.Integer, db.ForeignKey("Products.ProductID"), primary_key=True
    )

    UnitPrice = db.Column(db.Numeric(10, 2))
    Quantity = db.Column(db.SmallInteger)
    Discount = db.Column(db.Numeric(10, 2))

    product = db.relationship("Product")

    def __repr__(self):
        return f"<OrderDetail Order:{self.OrderID} Product:{self.ProductID}>"


class Order(db.Model):
    __tablename__ = "Orders"

    OrderID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerID = db.Column(db.String(5), db.ForeignKey("Customers.CustomerID"))
    EmployeeID = db.Column(db.Integer)
    OrderDate = db.Column(db.Date)
    RequiredDate = db.Column(db.Date)
    ShippedDate = db.Column(db.Date)
    ShipVia = db.Column(db.Integer)
    Freight = db.Column(db.Numeric(10, 2))
    ShipName = db.Column(db.String(100))
    ShipAddress = db.Column(db.String(255))
    ShipCity = db.Column(db.String(100))
    ShipRegion = db.Column(db.String(50))
    ShipPostalCode = db.Column(db.String(20))
    ShipCountry = db.Column(db.String(50))

    # Relationship to OrderDetails
    details = db.relationship(
        "OrderDetail", backref="order", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Order {self.OrderID}>"


class OrderDetailSchema(ma.Schema):
    ProductID = fields.Integer()
    UnitPrice = fields.Decimal(places=2)
    Quantity = fields.Integer()
    Discount = fields.Decimal(places=2)
    product = fields.Nested("ProductSchema", only=("ProductID", "ProductName"))


class OrderSchema(ma.Schema):
    OrderID = fields.Integer()
    CustomerID = fields.String(required=True)
    EmployeeID = fields.Integer()
    OrderDate = fields.Date(format="%Y-%m-%d", required=True)
    RequiredDate = fields.Date(format="%Y-%m-%d")
    ShippedDate = fields.Date(format="%Y-%m-%d")
    ShipVia = fields.Integer()
    Freight = fields.Decimal(places=2)
    ShipName = fields.String()
    ShipAddress = fields.String()
    ShipCity = fields.String()
    ShipRegion = fields.String()
    ShipPostalCode = fields.String()
    ShipCountry = fields.String()
    details = fields.Nested(OrderDetailSchema, many=True)
