import json
from pathlib import Path

import pytest


@pytest.mark.api
def test_get_api_products_list(api_client):
    response = api_client.get("/products")
    assert response.status_code == 200
    # validating content response type
    assert "application/json" in response.headers["Content-Type"]
    # converting JSON data into Python dictionaries
    response_data = response.json()
    # print("API Response: ", response_data)
    print("API Response Keys: ", response_data.keys())

    assert isinstance(response_data, dict)
    assert isinstance(response_data["current_page"], int)
    assert isinstance(response_data["last_page"], int)
    assert isinstance(response_data["per_page"], int)
    assert isinstance(response_data["total"], int)
    products = response_data["data"]
    assert isinstance(products, list)
    assert len(products) > 0
    print("First product keys: ", products[0].keys())
    for product in products:
        assert isinstance(product["id"], str)
        assert isinstance(product["name"], str)
        assert isinstance(product["description"], str)
        assert isinstance(product["price"], (int, float))
        assert isinstance(product["in_stock"], (int, float))

@pytest.mark.api
def test_get_api_products_detail_by_id(api_client):
    response = api_client.get("/products")
    assert response.status_code == 200
    products_list_data = response.json()
    products = products_list_data["data"]
    assert len(products) > 0
    product_id = products[0]["id"]
    print("Product ID: ", product_id)
    response_data = api_client.get(f"/products/{product_id}")
    assert response_data.status_code == 200
    assert "application/json" in response_data.headers["Content-Type"]
    product_data = response_data.json()
    assert product_data["id"] == product_id
    assert isinstance(product_data["name"], str)
    assert isinstance(product_data["description"], str)
    assert isinstance(product_data["price"], (int, float))
    assert isinstance(product_data["is_location_offer"], bool)
    assert isinstance(product_data["is_rental"], bool)
    assert isinstance(product_data["in_stock"], bool)
    assert isinstance(product_data["is_eco_friendly"], bool)

    print("\nRetrieved Product Details:", product_data)

@pytest.mark.api
def test_create_new_product(api_client, admin_api_token):
    file_path = Path("test_data/api_products_data.json")
    with open(file_path, "r") as file:
        test_data = json.load(file)

    product_data = test_data["new_product"]
    products_response = api_client.get("/products")
    assert products_response.status_code == 200
    products = products_response.json()["data"]
    assert len(products) > 0
    existing_product = products[0]
    print("\nExisting Product Image:")
    print(existing_product["product_image"])

    print("\nExisting Product Image Keys:")
    print(existing_product["product_image"].keys())
    product_payload = {**product_data,
                       "brand_id": existing_product["brand"]["id"],
                       "category_id": existing_product["category"]["id"],
                       "product_image_id": existing_product["product_image"]["id"]}
    response = api_client.post("/products", product_payload)
    assert response.status_code == 201, f"Product creation failed: {response.status_code} - {response.text}"
    created_product = response.json()
    assert created_product["name"] == product_payload["name"]
    assert created_product["description"] == product_payload["description"]
    assert created_product["price"] == product_payload["price"]

    assert created_product["brand"]["id"] == product_payload["brand_id"]
    assert created_product["category"]["id"] == product_payload["category_id"]
    assert created_product["product_image"]["id"] == product_payload["product_image_id"]
    assert isinstance(created_product["id"], str)
    print("\nCreated Product ID:", created_product["id"])
    print("\nCreated Product Details:", created_product)



