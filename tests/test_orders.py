from unittest.mock import MagicMock
from flask import Response
import json

# Mock data
MOCK_ORDER_DETAIL = {
    "ProductID": 10,
    "UnitPrice": 10.00,
    "Quantity": 5,
    "Discount": 0.0,
    "product": {"ProductID": 10, "ProductName": "Test Product"},
}
MOCK_ORDER = {
    "OrderID": 10248,
    "CustomerID": "VINET",
    "OrderDate": "1996-07-04",
    "ShipCity": "Lyon",
    "details": [MOCK_ORDER_DETAIL],
}

ORDER_API_ROOT = "/orders"


def test_get_all_orders_success(client, mocker):
    """Tests GET /orders returns a list of orders."""
    mock_service = mocker.patch("app.services.order_service.OrderService.get_all")
    mock_schema = mocker.patch("app.routes.order_routes.orders_schema")

    mock_order_instance = MagicMock()
    mock_service.return_value = [mock_order_instance]
    mock_schema.dump.return_value = [MOCK_ORDER]

    response = client.get(ORDER_API_ROOT)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["OrderID"] == 10248
    assert mock_service.called


def test_get_order_by_id_found(client, mocker):
    """Tests GET /orders/<id> returns 200 when order exists and has nested details."""
    mock_service = mocker.patch("app.services.order_service.OrderService.get_by_id")
    mock_schema = mocker.patch("app.routes.order_routes.order_schema")

    mock_order = MagicMock()
    mock_service.return_value = mock_order

    mock_response = Response(
        json.dumps(MOCK_ORDER), status=200, mimetype="application/json"
    )
    mock_schema.jsonify.return_value = mock_response

    response = client.get(f"{ORDER_API_ROOT}/10248")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["CustomerID"] == MOCK_ORDER["CustomerID"]
    assert "details" in data
    assert len(data["details"]) == 1
    assert data["details"][0]["ProductID"] == 10


def test_get_order_by_id_not_found(client, mocker):
    """Tests GET /orders/<id> returns 404 when order doesn't exist."""
    mock_service = mocker.patch("app.services.order_service.OrderService.get_by_id")
    mock_service.return_value = None

    response = client.get(f"{ORDER_API_ROOT}/99999")

    assert response.status_code == 404


def test_create_order_success(client, mocker):
    """Tests POST /orders returns 201 on successful creation, including details."""
    mock_service = mocker.patch("app.services.order_service.OrderService.create")
    mock_schema = mocker.patch("app.routes.order_routes.order_schema")

    new_order_data = {
        "CustomerID": "NEWCU",
        "OrderDate": "2023-01-01",
        "details": [{"ProductID": 1, "UnitPrice": 50, "Quantity": 1}],
    }
    new_order_response = {**new_order_data, "OrderID": 99999}

    mock_new_order = MagicMock()
    mock_service.return_value = mock_new_order

    mock_schema.load.return_value = new_order_data
    mock_response = Response(
        json.dumps(new_order_response), status=201, mimetype="application/json"
    )
    mock_schema.jsonify.return_value = mock_response

    response = client.post(
        ORDER_API_ROOT, data=json.dumps(new_order_data), content_type="application/json"
    )
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data["OrderID"] == 99999
    mock_service.assert_called_once()


def test_create_order_no_input(client):
    """Tests POST /orders returns 400 when no data provided."""
    response = client.post(ORDER_API_ROOT, content_type="application/json")

    assert response.status_code == 400
    assert (
        b"Failed to decode JSON" in response.data
        or b"No input data provided" in response.data
    )


def test_update_order_success(client, mocker):
    """Tests PUT /orders/<id> returns 200 on successful update."""
    mock_service = mocker.patch("app.services.order_service.OrderService.update")
    mock_schema = mocker.patch("app.routes.order_routes.order_schema")

    updated_order = {**MOCK_ORDER, "ShipCity": "Paris"}
    mock_updated_order = MagicMock()
    mock_service.return_value = mock_updated_order

    update_data = {"ShipCity": "Paris"}

    mock_schema.load.return_value = update_data
    mock_response = Response(
        json.dumps(updated_order), status=200, mimetype="application/json"
    )
    mock_schema.jsonify.return_value = mock_response

    response = client.put(
        f"{ORDER_API_ROOT}/10248",
        data=json.dumps(update_data),
        content_type="application/json",
    )
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["ShipCity"] == "Paris"
    mock_service.assert_called_once()


def test_update_order_not_found(client, mocker):
    """Tests PUT /orders/<id> returns 404 when order doesn't exist."""
    mock_service = mocker.patch("app.services.order_service.OrderService.update")
    mock_schema = mocker.patch("app.routes.order_routes.order_schema")

    mock_service.return_value = None
    mock_schema.load.return_value = {"ShipCity": "Paris"}

    update_data = {"ShipCity": "Paris"}

    response = client.put(
        f"{ORDER_API_ROOT}/99999",
        data=json.dumps(update_data),
        content_type="application/json",
    )

    assert response.status_code == 404


def test_get_customer_history_found(client, mocker):
    """Tests GET /orders/history/<customer_id> returns list of orders."""
    mock_service = mocker.patch(
        "app.services.order_service.OrderService.get_customer_history"
    )

    serialized_history = [
        {"OrderID": 100, "OrderDate": "1997-01-01", "CustomerID": "ALFKI"},
        {"OrderID": 99, "OrderDate": "1996-12-01", "CustomerID": "ALFKI"},
    ]
    mock_service.return_value = serialized_history

    response = client.get(f"{ORDER_API_ROOT}/history/ALFKI")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["OrderID"] == 100
    assert mock_service.called


def test_get_customer_history_customer_not_found(client, mocker):
    """Tests GET /orders/history/<customer_id> returns 404 if customer doesn't exist."""
    mock_service = mocker.patch(
        "app.services.order_service.OrderService.get_customer_history"
    )
    mock_service.return_value = None

    response = client.get(f"{ORDER_API_ROOT}/history/NONEX")

    assert response.status_code == 404


def test_get_customer_history_no_orders(client, mocker):
    """Tests GET /orders/history/<customer_id> returns 200 with message when customer has no orders."""
    mock_service = mocker.patch(
        "app.services.order_service.OrderService.get_customer_history"
    )
    mock_service.return_value = []

    response = client.get(f"{ORDER_API_ROOT}/history/ALFKI")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert "no orders" in data["message"]


def test_delete_order_success(client, mocker):
    """Tests DELETE /orders/<id> returns 204 on successful deletion."""
    mock_service = mocker.patch("app.services.order_service.OrderService.delete")
    mock_service.return_value = True

    response = client.delete(f"{ORDER_API_ROOT}/10248")

    assert response.status_code == 204
    if response.data:
        data = json.loads(response.data)
        assert "successfully deleted" in data["message"]
    assert mock_service.called


def test_delete_order_not_found(client, mocker):
    """Tests DELETE /orders/<id> returns 404 when order doesn't exist."""
    mock_service = mocker.patch("app.services.order_service.OrderService.delete")
    mock_service.return_value = False

    response = client.delete(f"{ORDER_API_ROOT}/99999")

    assert response.status_code == 404
