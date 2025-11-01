from flask import Blueprint, request, jsonify
from ..services.product_service import ProductService
from ..models import product_schema, products_schema
from ..database import db

product_bp = Blueprint("product", __name__)


@product_bp.route("/products", methods=["GET"])
def get_products():
    """Endpoint to get all products."""
    try:
        products = ProductService.get_all()
        result = products_schema.dump(products)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


@product_bp.route("/products", methods=["POST"])
def add_product():
    """Endpoint to insert a new product."""
    json_data = request.get_json(silent=True)
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400

    # Validation and deserialization
    try:
        data = product_schema.load(json_data, partial=True)
    except Exception as err:
        return jsonify(err.messages), 400  # type: ignore

    try:
        new_product = ProductService.create(data)
        return product_schema.jsonify(new_product), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error inserting product: {str(e)}"}), 500


@product_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """Endpoint to get a product by ID."""
    product = ProductService.get_by_id(product_id)

    if product:
        return product_schema.jsonify(product), 200
    return jsonify({"message": f"Product ID {product_id} not found"}), 404


@product_bp.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """Endpoint to update an existing product."""
    json_data = request.get_json()

    try:
        data = product_schema.load(json_data, partial=True)
    except Exception as err:
        return jsonify(err.messages), 400  # type: ignore

    updated_product = ProductService.update(product_id, data)

    if updated_product:
        return product_schema.jsonify(updated_product), 200
    return jsonify({"message": f"Product ID {product_id} not found"}), 404


@product_bp.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Endpoint to delete a product."""
    deleted = ProductService.delete(product_id)

    if deleted:
        return (
            jsonify({"message": f"Product ID {product_id} successfully deleted"}),
            204,
        )
    return jsonify({"message": f"Product ID {product_id} not found"}), 404
