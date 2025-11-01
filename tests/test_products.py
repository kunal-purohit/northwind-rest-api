from unittest.mock import MagicMock
from flask import Response
import json

# Mock data
MOCK_PRODUCT = {
    "ProductID": 10,
    "ProductName": "Queso Cabrales",
    "UnitPrice": 21.00,
    "UnitsInStock": 22,
    "Discontinued": False,
}

PRODUCT_API_ROOT = "/api/products"


def test_get_all_products_success(client, mocker):
    """Tests GET /products returns a list of products."""
    mock_service = mocker.patch("app.services.product_service.ProductService.get_all")
    mock_schema = mocker.patch("app.routes.product_routes.products_schema")

    mock_product_instance = MagicMock()
    mock_service.return_value = [mock_product_instance]
    mock_schema.dump.return_value = [MOCK_PRODUCT]

    response = client.get(PRODUCT_API_ROOT)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["ProductID"] == 10
    assert mock_service.called


def test_get_product_by_id_found(client, mocker):
    """Tests GET /products/<id> returns 200 when product exists."""
    mock_service = mocker.patch("app.services.product_service.ProductService.get_by_id")
    mock_schema = mocker.patch("app.routes.product_routes.product_schema")

    mock_product = MagicMock()
    mock_service.return_value = mock_product

    mock_response = Response(
        json.dumps(MOCK_PRODUCT), status=200, mimetype="application/json"
    )
    mock_schema.jsonify.return_value = mock_response

    response = client.get(f"{PRODUCT_API_ROOT}/10")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["ProductName"] == MOCK_PRODUCT["ProductName"]


def test_get_product_by_id_not_found(client, mocker):
    """Tests GET /products/<id> returns 404 when product doesn't exist."""
    mock_service = mocker.patch("app.services.product_service.ProductService.get_by_id")
    mock_service.return_value = None

    response = client.get(f"{PRODUCT_API_ROOT}/999")

    assert response.status_code == 404


def test_create_product_success(client, mocker):
    """Tests POST /products returns 201 on successful creation."""
    mock_service = mocker.patch("app.services.product_service.ProductService.create")
    mock_schema = mocker.patch("app.routes.product_routes.product_schema")

    new_data = {"ProductName": "New Item", "UnitPrice": 12.50}
    new_product_response = {**new_data, "ProductID": 99}

    mock_new_product = MagicMock()
    mock_service.return_value = mock_new_product

    mock_schema.load.return_value = new_data
    mock_response = Response(
        json.dumps(new_product_response), status=201, mimetype="application/json"
    )
    mock_schema.jsonify.return_value = mock_response

    response = client.post(
        PRODUCT_API_ROOT, data=json.dumps(new_data), content_type="application/json"
    )
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data["ProductName"] == "New Item"
    assert mock_service.called


def test_create_product_no_input(client):
    """Tests POST /products returns 400 when no data provided."""
    response = client.post(PRODUCT_API_ROOT, content_type="application/json")

    assert response.status_code == 400
    assert (
        b"Failed to decode JSON" in response.data
        or b"No input data provided" in response.data
    )


def test_create_product_validation_failure(client, mocker):
    """Tests POST /products returns 400 when UnitPrice is negative (Marshmallow validation)."""
    invalid_data = {"ProductName": "Bad Item", "UnitPrice": -5.00}

    response = client.post(
        PRODUCT_API_ROOT, data=json.dumps(invalid_data), content_type="application/json"
    )

    assert response.status_code == 400
    data = json.loads(response.data)
    assert "UnitPrice" in data
    assert "positive" in data["UnitPrice"][0]


def test_update_product_success(client, mocker):
    """Tests PUT /products/<id> returns 200 on successful update."""
    mock_service = mocker.patch("app.services.product_service.ProductService.update")
    mock_schema = mocker.patch("app.routes.product_routes.product_schema")

    updated_product = {**MOCK_PRODUCT, "UnitPrice": 25.00}
    mock_updated_product = MagicMock()
    mock_service.return_value = mock_updated_product

    update_data = {"UnitPrice": 25.00}

    mock_schema.load.return_value = update_data
    mock_response = Response(
        json.dumps(updated_product), status=200, mimetype="application/json"
    )
    mock_schema.jsonify.return_value = mock_response

    response = client.put(
        f"{PRODUCT_API_ROOT}/10",
        data=json.dumps(update_data),
        content_type="application/json",
    )
    data = json.loads(response.data)

    assert response.status_code == 200
    assert float(data["UnitPrice"]) == 25.00
    mock_service.assert_called_once()


def test_update_product_not_found(client, mocker):
    """Tests PUT /products/<id> returns 404 when product doesn't exist."""
    mock_service = mocker.patch("app.services.product_service.ProductService.update")
    mock_schema = mocker.patch("app.routes.product_routes.product_schema")

    mock_service.return_value = None
    mock_schema.load.return_value = {"UnitPrice": 25.00}

    update_data = {"UnitPrice": 25.00}

    response = client.put(
        f"{PRODUCT_API_ROOT}/999",
        data=json.dumps(update_data),
        content_type="application/json",
    )

    assert response.status_code == 404


def test_delete_product_not_found(client, mocker):
    """Tests DELETE /products/<id> returns 404 when product is missing."""
    mock_service = mocker.patch("app.services.product_service.ProductService.delete")
    mock_service.return_value = False

    response = client.delete(f"{PRODUCT_API_ROOT}/999")

    assert response.status_code == 404


def test_delete_product_success(client, mocker):
    """Tests DELETE /products/<id> returns 204 on successful deletion."""
    mock_service = mocker.patch("app.services.product_service.ProductService.delete")
    mock_service.return_value = True

    response = client.delete(f"{PRODUCT_API_ROOT}/10")

    assert response.status_code == 204
    if response.data:
        data = json.loads(response.data)
        assert "successfully deleted" in data["message"]
    assert mock_service.called
