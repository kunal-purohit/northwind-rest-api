from unittest.mock import MagicMock
from flask import Response
import json

# Mock data
MOCK_CUSTOMER = {
    "CustomerID": "ALFKI",
    "CompanyName": "Alfreds Futterkiste",
    "ContactName": "Maria Anders",
    "City": "Berlin",
}

CUSTOMER_API_ROOT = "/customers"


def test_get_all_customers_success(client, mocker):
    """Tests GET /customers returns a list of customers."""
    mock_service = mocker.patch("app.services.customer_service.CustomerService.get_all")
    # Mock the schema dump method to return our expected data
    mock_schema = mocker.patch("app.routes.customer_routes.customers_schema")

    mock_customer = MagicMock()
    mock_service.return_value = [mock_customer]
    mock_schema.dump.return_value = [MOCK_CUSTOMER]

    response = client.get(CUSTOMER_API_ROOT)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["CustomerID"] == "ALFKI"
    assert mock_service.called


def test_get_customer_by_id_found(client, mocker):
    """Tests GET /customers/<id> returns 200 when customer exists."""
    mock_service = mocker.patch(
        "app.services.customer_service.CustomerService.get_by_id"
    )
    mock_schema = mocker.patch("app.routes.customer_routes.customer_schema")

    mock_customer = MagicMock()
    mock_service.return_value = mock_customer

    # Mock jsonify to return a Response object
    mock_response = Response(
        json.dumps(MOCK_CUSTOMER), status=200, mimetype="application/json"
    )
    mock_schema.jsonify.return_value = mock_response

    response = client.get(f"{CUSTOMER_API_ROOT}/ALFKI")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["CompanyName"] == MOCK_CUSTOMER["CompanyName"]


def test_get_customer_by_id_not_found(client, mocker):
    """Tests GET /customers/<id> returns 404 when customer is missing."""
    mock_service = mocker.patch(
        "app.services.customer_service.CustomerService.get_by_id"
    )
    mock_service.return_value = None

    response = client.get(f"{CUSTOMER_API_ROOT}/NONEX")

    assert response.status_code == 404


def test_create_customer_success(client, mocker):
    """Tests POST /customers returns 201 on successful creation."""
    mock_service = mocker.patch("app.services.customer_service.CustomerService.create")
    mock_schema = mocker.patch("app.routes.customer_routes.customer_schema")

    new_data = {"CustomerID": "NEWCO", "CompanyName": "New Corp"}
    mock_new_customer = MagicMock()
    mock_service.return_value = mock_new_customer

    # Mock both load (for input validation) and jsonify (for output)
    mock_schema.load.return_value = new_data
    mock_response = Response(
        json.dumps(new_data), status=201, mimetype="application/json"
    )
    mock_schema.jsonify.return_value = mock_response

    response = client.post(
        CUSTOMER_API_ROOT, data=json.dumps(new_data), content_type="application/json"
    )
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data["CustomerID"] == "NEWCO"
    assert mock_service.called


def test_create_customer_no_input(client):
    """Tests POST /customers returns 400 when no data provided."""
    response = client.post(CUSTOMER_API_ROOT, content_type="application/json")

    assert response.status_code == 400
    # Flask returns HTML error page for JSON decode errors, check response text
    assert (
        b"Failed to decode JSON" in response.data
        or b"No input data provided" in response.data
    )


def test_update_customer_success(client, mocker):
    """Tests PUT /customers/<id> returns 200 on successful update."""
    mock_service = mocker.patch("app.services.customer_service.CustomerService.update")
    mock_schema = mocker.patch("app.routes.customer_routes.customer_schema")

    updated_data = {**MOCK_CUSTOMER, "ContactName": "New Contact"}
    mock_updated_customer = MagicMock()
    mock_service.return_value = mock_updated_customer

    update_data = {"ContactName": "New Contact"}

    mock_schema.load.return_value = update_data
    mock_response = Response(
        json.dumps(updated_data), status=200, mimetype="application/json"
    )
    mock_schema.jsonify.return_value = mock_response

    response = client.put(
        f"{CUSTOMER_API_ROOT}/ALFKI",
        data=json.dumps(update_data),
        content_type="application/json",
    )
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["ContactName"] == "New Contact"
    mock_service.assert_called_once()


def test_update_customer_not_found(client, mocker):
    """Tests PUT /customers/<id> returns 404 when customer doesn't exist."""
    mock_service = mocker.patch("app.services.customer_service.CustomerService.update")
    mock_schema = mocker.patch("app.routes.customer_routes.customer_schema")

    mock_service.return_value = None
    mock_schema.load.return_value = {"ContactName": "New Contact"}

    update_data = {"ContactName": "New Contact"}

    response = client.put(
        f"{CUSTOMER_API_ROOT}/NONEX",
        data=json.dumps(update_data),
        content_type="application/json",
    )

    assert response.status_code == 404


def test_delete_customer_not_found(client, mocker):
    """Tests DELETE /customers/<id> returns 404 when customer is missing."""
    mock_service = mocker.patch("app.services.customer_service.CustomerService.delete")
    mock_service.return_value = False

    response = client.delete(f"{CUSTOMER_API_ROOT}/NONEX")

    assert response.status_code == 404
    assert mock_service.called


def test_delete_customer_success(client, mocker):
    """Tests DELETE /customers/<id> returns 204 on successful deletion."""
    mock_service = mocker.patch("app.services.customer_service.CustomerService.delete")
    mock_service.return_value = True

    response = client.delete(f"{CUSTOMER_API_ROOT}/ALFKI")

    assert response.status_code == 204
    # 204 responses may have no body or a JSON message - check what your route actually returns
    if response.data:
        data = json.loads(response.data)
        assert "successfully deleted" in data["message"]
    assert mock_service.called
