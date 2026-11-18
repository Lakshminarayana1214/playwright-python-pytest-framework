import json
from pathlib import Path

import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage

json_data = (
    Path(__file__).resolve().parent.parent / 'test_data' / 'login_data.json'
)

with open(json_data, "r", encoding="utf-8") as file:
    login_test_cases = json.load(file)['login_validation_cases']

#validating the negative test cases in json data

@pytest.mark.smoke
@pytest.mark.parametrize("json_data", login_test_cases,ids=[case["test_case"] for case in login_test_cases])
def test_login_validation(app_page,base_url,json_data):
    login_page = LoginPage(app_page)
    # opening the login page
    login_page.open_login_url(base_url)
    # entering the test data and click on login button
    login_page.login(
        json_data['email'],
        json_data['password']
    )

    for message in json_data["expected_messages"]:
        expect(app_page.get_by_text(message,exact=True)).to_be_visible()

# Verify Email and Password placeholders

@pytest.mark.smoke
def test_login_placeholders(app_page,base_url):
    login_page = LoginPage(app_page)
    login_page.open_login_url(base_url)
    expect(app_page.locator(login_page.email_locator)).to_have_attribute("placeholder","Your email")
    expect(app_page.locator(login_page.password_locator)).to_have_attribute("placeholder","Your password")

@pytest.mark.smoke
def test_password_masked(app_page,base_url):
    login_page = LoginPage(app_page)
    login_page.open_login_url(base_url)
    password_field = app_page.locator(login_page.password_locator)
    password_field.fill("welcome1")
    expect(password_field).to_have_attribute("type","password")

@pytest.mark.smoke
def test_password_visible_toggle(app_page,base_url):
    login_page = LoginPage(app_page)
    login_page.open_login_url(base_url)
    password_field = app_page.locator(login_page.password_locator)
    password_field.fill("welcome1")
    expect(password_field).to_have_attribute("type","password")
    login_page.click_eye_login()
    expect(password_field).to_have_attribute("type","text")
    login_page.click_eye_slash_login()
    expect(password_field).to_have_attribute("type", "password")

@pytest.mark.smoke
@pytest.mark.regression
def test_admin_login(app_page,base_url,admin_user_credentials):
    login_page = LoginPage(app_page)
    login_page.open_login_url(base_url)
    admin_email,admin_password = admin_user_credentials
    login_page.login(admin_email,admin_password)
    expect(app_page).not_to_have_url(f"{base_url}/auth/login")

@pytest.mark.smoke
def test_customer_login(app_page,base_url,customer_user_credentials):
    login_page = LoginPage(app_page)
    login_page.open_login_url(base_url)
    customer_email,customer_pass = customer_user_credentials
    login_page.login(customer_email,customer_pass)
    expect(app_page).not_to_have_url(f"{base_url}/auth/login")


