from flask import Blueprint, request, jsonify
from ..services import CustomerService
from ..models import customer_schema, customers_schema
from ..database import db

customer_bp = Blueprint("customer", __name__)


@customer_bp.route("/customers", methods=["GET"])
def get_customers():
    """Endpoint to get all customers."""
    try:
        customers = CustomerService.get_all()
        result = customers_schema.dump(customers)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


@customer_bp.route("/customers", methods=["POST"])
def add_customer():
    """Endpoint to insert a new customer."""
    json_data = request.get_json(silent=True)
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400

    # Validation and deserialization using Marshmallow schema
    try:
        data = customer_schema.load(json_data, partial=True)
    except Exception as err:
        return jsonify(err.messages), 400  # type: ignore

    try:
        new_customer = CustomerService.create(data)
        return customer_schema.jsonify(new_customer), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error inserting customer: {str(e)}"}), 500


@customer_bp.route("/customers/<string:customer_id>", methods=["GET"])
def get_customer(customer_id):
    """Endpoint to get a customer by ID."""
    customer = CustomerService.get_by_id(customer_id)

    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"message": f"Customer ID {customer_id} not found"}), 404


@customer_bp.route("/customers/<string:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    """Endpoint to update an existing customer."""
    json_data = request.get_json()

    # Partial validation for update
    try:
        data = customer_schema.load(json_data, partial=True)
    except Exception as err:
        return jsonify(err), 400

    updated_customer = CustomerService.update(customer_id, data)

    if updated_customer:
        return customer_schema.jsonify(updated_customer), 200
    return jsonify({"message": f"Customer ID {customer_id} not found"}), 404


@customer_bp.route("/customers/<string:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """Endpoint to delete a customer."""
    deleted = CustomerService.delete(customer_id)

    if deleted:
        return (
            jsonify({"message": f"Customer ID {customer_id} successfully deleted"}),
            204,
        )  # 204 No Content
    return jsonify({"message": f"Customer ID {customer_id} not found"}), 404
