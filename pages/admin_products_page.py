import re

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class AdminProductsPage(BasePage):
    # admin page locators
    admin_menu_locator = 'button[data-test="nav-menu"]'
    products_locator = 'a[data-test="nav-admin-products"]'
    # page title,table and rows locators
    page_title_locator = 'h1[data-test="page-title"]'
    product_table_locator = 'table.table-hover'
    product_table_headers_locator = 'table.table-hover thead th'
    product_rows_locator = 'table.table-hover tbody tr'
    # Search,add and reset locators
    add_product_locator = 'a[data-test="product-add"]'
    search_input_locator = 'input[data-test="product-search-query"]'
    search_button_locator = 'button[data-test="product-search-submit"]'
    reset_button_locator = 'button[data-test="product-search-reset"]'
    # Pagination locators
    pagination_locator = 'ul.pagination'
    page_1_locator = 'button[aria-label="Page-1"]'
    page_2_locator = 'button[aria-label="Page-2"]'
    # Adding product locators
    name_locator = '#name'
    description_locator = '#description'
    stock_locator = '#stock'
    price_locator = '#price'
    location_offer_locator = '#is_location_offer'
    item_for_rent_locator = '#is_rental'
    co2_rating_locator = '#co2_rating'
    brand_locator = '#brand_id'
    category_locator = '#category_id'
    image_locator = '#product_image_id'
    save_product_locator = 'button[data-test="product-submit"]'

    def __init__(self, page:Page):
        super().__init__(page)

    def click_admin_menu(self):
        self.page.locator(self.admin_menu_locator).click()

    def click_products_menu(self):
        self.page.locator(self.products_locator).click()

    def open_admin_products_menu(self):
        self.click_admin_menu()
        expect (self.page.locator(self.products_locator)).to_be_visible()
        self.click_products_menu()

    def products_page_title(self):
        expect(self.page.locator(self.page_title_locator)).to_have_text("Products")

    def search_product(self, product_name):
        self.page.locator(self.search_input_locator).fill(product_name)
        self.page.locator(self.search_button_locator).click()

    def verify_search_product(self, product_name):
        matching_product = self.page.locator(self.product_rows_locator).filter(has_text=product_name)
        expect(matching_product.first).to_be_visible()

    def get_product_row_count(self):
        return self.page.locator(self.product_rows_locator).count()

    def reset_product_search(self):
        self.page.locator(self.reset_button_locator).click()

    def click_pagination(self):
        self.page.locator(self.page_2_locator).click()

    def click_add_product(self):
        self.page.locator(self.add_product_locator).click()
        expect(self.page).to_have_url(re.compile(r".*/admin/products/add/?$"))

    def fill_product_form(self,product_data):
        self.page.locator(self.name_locator).fill(product_data["name"])
        self.page.locator(self.description_locator).fill(product_data["description"])
        self.page.locator(self.stock_locator).fill(product_data["stock"])
        self.page.locator(self.price_locator).fill(product_data["price"])
        self.page.locator(self.location_offer_locator).set_checked(product_data["location_offer"])
        self.page.locator(self.item_for_rent_locator).set_checked(product_data["item_for_rent"])
        self.page.locator(self.co2_rating_locator).select_option(label=product_data["co2_rating"])
        self.page.locator(self.brand_locator).select_option(label=product_data["brand"])
        self.page.locator(self.category_locator).select_option(label=product_data["category"])
        self.page.locator(self.image_locator).select_option(label=product_data["image"])

    def save_product(self):
        self.page.locator(self.save_product_locator).click()

    def open_edit_product(self, product_name):
        self.search_product(product_name)
        product_row = self.page.locator(self.product_rows_locator).filter(has_text=product_name).first
        expect(product_row).to_be_visible()
        edit_link = product_row.locator('a[data-test^="product-edit-"]')
        expect(edit_link).to_be_visible()
        edit_link.click()

    def update_product_form(self, product_data):
        self.fill_product_form(product_data)
        self.save_product()

