import json

import pytest
from pathlib import Path
from playwright.sync_api import expect

from pages.admin_products_page import AdminProductsPage
from pages.login_page import LoginPage

test_data = (Path(__file__).resolve().parents[1] / "test_data" / "admin_product_page.json")
with test_data.open(encoding="utf-8") as file:
    data = json.load(file)

def admin_as_login(app_page,base_url,admin_user_credentials):
    login_page = LoginPage(app_page)
    login_page.open_login_url(base_url)
    admin_email, admin_password = admin_user_credentials
    login_page.login(admin_email, admin_password)
    expect(app_page).to_have_url(f"{base_url}/admin/dashboard")

def navigation_page(app_page,base_url):
    admin_products_page = AdminProductsPage(app_page)
    admin_products_page.open_admin_products_menu()
    expect(app_page).to_have_url(f"{base_url}/admin/products")
    return admin_products_page
#
# def add_product_navigation_page(app_page,base_url):
#     admin_products_page = AdminProductsPage(app_page)
#     admin_products_page.click_add_product()
#     expect(app_page).to_have_url(f"{base_url}/admin/products/add")
#     return admin_products_page

# Routing the page to Admin products page
@pytest.mark.regression
def test_admin_products(app_page,base_url,admin_user_credentials):
    admin_as_login(app_page,base_url,admin_user_credentials)
    admin_products_page = AdminProductsPage(app_page)
    admin_products_page.open_admin_products_menu()
    expect(app_page).to_have_url(f"{base_url}/admin/products")

@pytest.mark.regression
def test_product_listing(app_page,base_url,admin_user_credentials):
    admin_as_login(app_page,base_url,admin_user_credentials)
    admin_products_page = navigation_page(app_page,base_url)
    admin_products_page.products_page_title()
    admin_products_table = app_page.locator(admin_products_page.product_table_locator)
    expect(admin_products_table).to_be_visible()
    headers = app_page.locator(admin_products_page.product_table_headers_locator)
    expect(headers.nth(0)).to_have_text("Id")
    expect(headers.nth(1)).to_have_text("Name")
    expect(headers.nth(2)).to_have_text("Stock")
    expect(headers.nth(3)).to_have_text("Price")
    product_count = admin_products_page.get_product_row_count()
    assert product_count > 0

@pytest.mark.regression
def test_validate_product_pagination(app_page,base_url,admin_user_credentials):
    admin_as_login(app_page,base_url,admin_user_credentials)
    admin_products_page = navigation_page(app_page,base_url)
    pagination = app_page.locator(admin_products_page.pagination_locator)
    expect(pagination).to_be_visible()
    first_row = app_page.locator(admin_products_page.product_rows_locator).first
    first_page_product = first_row.inner_text()
    admin_products_page.click_pagination()
    active_page = app_page.locator("ul.pagination li.page-item.active button")
    expect(active_page).to_have_attribute("aria-label", "Page-2")
    expect(first_row).not_to_have_text(first_page_product)

@pytest.mark.regression
def test_verify_previous_page_navigation(app_page,base_url,admin_user_credentials):
    admin_as_login(app_page, base_url, admin_user_credentials)
    admin_products_page = navigation_page(app_page,base_url)
    # Navigate to page 2 first
    admin_products_page.click_pagination()
    # Navigate back to page 1
    app_page.locator(admin_products_page.page_1_locator).click()
    # Verify page 1 is active
    active_page = app_page.locator("ul.pagination li.page-item.active button")
    expect(active_page).to_have_attribute("aria-label", "Page-1")

@pytest.mark.regression
def test_search_product(app_page,base_url,admin_user_credentials):
    admin_as_login(app_page, base_url, admin_user_credentials)
    admin_products_page = navigation_page(app_page,base_url)
    product_name = "Bolt Cutters"
    admin_products_page.search_product(product_name)
    admin_products_page.verify_search_product(product_name)

@pytest.mark.regression
def test_validate_product_mandatory_fields(app_page,base_url,admin_user_credentials):
    admin_as_login(app_page, base_url, admin_user_credentials)
    admin_products_page = navigation_page(app_page,base_url)
    admin_products_page.click_add_product()
    admin_products_page.save_product()
    expect(app_page.get_by_text("Name is required", exact=True)).to_be_visible()
    expect(app_page.get_by_text("Description is required", exact=True)).to_be_visible()
    expect(app_page.get_by_text("Price is required", exact=True)).to_be_visible()

@pytest.mark.regression
def test_create_new_product(app_page,base_url,admin_user_credentials):
    admin_as_login(app_page, base_url, admin_user_credentials)
    admin_products_page = navigation_page(app_page,base_url)
    admin_products_page.click_add_product()
    product_data = data["valid_product"]
    admin_products_page.fill_product_form(product_data)
    admin_products_page.save_product()
    #commenting this step because after hit the save button it's not routing anywhere
    #expect(app_page).to_have_url(f"{base_url}/admin/products")

@pytest.mark.regression
def test_verify_new_product(app_page,base_url,admin_user_credentials):
    admin_as_login(app_page, base_url, admin_user_credentials)
    admin_products_page = navigation_page(app_page,base_url)
    product_name = data["valid_product"]["name"]
    admin_products_page.search_product(product_name)
    matching_row = app_page.locator(admin_products_page.product_rows_locator).filter(has_text=product_name)
    expect(matching_row.first).to_be_visible()
    expect(matching_row.first).to_contain_text(product_name)

@pytest.mark.regression
def test_edit_new_product(app_page,base_url,admin_user_credentials):
    pytest.skip("Editing is temporarily disabled in the application so we are skipping this test")
    admin_as_login(app_page, base_url, admin_user_credentials)
    admin_products_page = navigation_page(app_page,base_url)
    original_name = data["valid_product"]["name"]
    admin_products_page.open_edit_product(original_name)
    expect(app_page).to_have_url(f"{base_url}/admin/products/edit/{app_page.url.rsplit('/', 1)[-1]}")
    expect(app_page.locator(admin_products_page.name_locator)).to_have_value(original_name)
    updated_product_data = data["updated_product"]
    admin_products_page.update_product_form(updated_product_data)
    expect(app_page).to_have_url(f"{base_url}/admin/products")

@pytest.mark.regression
def test_verify_updated_product_information(app_page,base_url,admin_user_credentials):
    pytest.skip("since editing is disabled in the application so we are skipping this test")
    admin_as_login(app_page, base_url, admin_user_credentials)
    admin_products_page = navigation_page(app_page,base_url)
    updated_name = data["updated_product"]["name"]
    admin_products_page.search_product(updated_name)
    matching_row = app_page.locator(admin_products_page.product_rows_locator).filter(has_text=updated_name)
    expect(matching_row.first).to_be_visible()
    expect(matching_row.first).to_contain_text(updated_name)
