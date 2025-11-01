from flask import Blueprint, request, jsonify
from ..services import OrderService
from ..models import order_schema, orders_schema
from ..database import db

order_bp = Blueprint("order", __name__)


@order_bp.route("/orders", methods=["GET"])
def get_orders():
    """Endpoint to get all orders."""
    try:
        orders = OrderService.get_all()
        result = orders_schema.dump(orders)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


@order_bp.route("/orders", methods=["POST"])
def add_order():
    """Endpoint to insert a new order."""
    json_data = request.get_json(silent=True)
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400

    try:
        data = order_schema.load(json_data, partial=True)
    except Exception as err:
        return jsonify(err), 400

    try:
        new_order = OrderService.create(data)
        return order_schema.jsonify(new_order), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error inserting order: {str(e)}"}), 500


@order_bp.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    """Endpoint to get an order by ID."""
    order = OrderService.get_by_id(order_id)

    if order:
        return order_schema.jsonify(order), 200
    return jsonify({"message": f"Order ID {order_id} not found"}), 404


@order_bp.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    """Endpoint to update an existing order."""
    json_data = request.get_json()

    try:
        data = order_schema.load(json_data, partial=True)
    except Exception as err:
        return jsonify(err), 400

    updated_order = OrderService.update(order_id, data)

    if updated_order:
        return order_schema.jsonify(updated_order), 200
    return jsonify({"message": f"Order ID {order_id} not found"}), 404


@order_bp.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    """Endpoint to delete an order."""
    deleted = OrderService.delete(order_id)

    if deleted:
        return jsonify({"message": f"Order ID {order_id} successfully deleted"}), 204
    return jsonify({"message": f"Order ID {order_id} not found"}), 404


@order_bp.route("/orders/history/<string:customer_id>", methods=["GET"])
def get_customer_history(customer_id):
    """Endpoint to get order history for a specific customer."""
    history_data = OrderService.get_customer_history(customer_id)

    if history_data is None:
        return jsonify({"message": f"Customer ID {customer_id} not found"}), 404

    if not history_data:
        return jsonify({"message": f"Customer ID {customer_id} has no orders"}), 200

    return jsonify(history_data), 200
