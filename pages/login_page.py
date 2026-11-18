from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    # Identifying the locators
    email_locator = '[id="email"]'
    password_locator = '//input[@id="password"]'
    login_locator = '[type="submit"]'
    eye_locator = 'button:has(svg[data-icon="eye"])'
    eye_slash_locator = 'button:has(svg[data-icon="eye-slash"])'
    def __init__(self, page:Page):
        super().__init__(page)
    #opening the URL
    def open_login_url(self, base_url):
        self.open(f"{base_url}/auth/login")

    # entering the email id
    def enter_email(self, email):
        self.page.locator(self.email_locator).fill(email)

    # entering the password
    def enter_password(self, password):
        self.page.locator(self.password_locator).fill(password)

    #clikcing on the login button
    def click_login(self):
        self.page.locator(self.login_locator).click()

    def click_eye_login(self):
        self.page.locator(self.eye_locator).click()

    def click_eye_slash_login(self):
        self.page.locator(self.eye_slash_locator).click()

    # performing the login function
    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()







