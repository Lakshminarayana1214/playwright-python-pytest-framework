# Playwright Automation Framework with Python and Pytest

## 1. Project Overview

This project is an end-to-end UI automation testing framework developed using:

- Python
- Playwright
- Pytest
- Pytest-HTML
- Page Object Model (POM)
- JSON-based test data management
- Environment variables using Python Dotenv

The framework automates the **Practice Software Testing – Toolshop** web application.

Application URL: https://practicesoftwaretesting.com/

The primary objective is to build a reusable, maintainable and scalable automation framework that supports functional testing, regression testing, positive and negative scenarios, and browser-based UI validation.

### Key objectives

1. Automate application workflows using Playwright.
2. Implement Page Object Model for reusable page actions.
3. Maintain test data separately using JSON files.
4. Use Pytest fixtures for browser and application setup.
5. Manage credentials securely using `.env`.
6. Execute tests individually, by module, or using markers.
7. Generate HTML execution reports.
8. Capture screenshots and investigate failures.
9. Support maintainable test code and reusable functions.

---

# 2. Technology Stack and Requirements

| Technology | Purpose |
|---|---|
| Python 3.11 | Programming language |
| Playwright | Browser automation |
| Pytest | Test execution and test management |
| pytest-playwright | Playwright integration with Pytest |
| pytest-html | HTML test reports |
| python-dotenv | Environment variable management |
| JSON | External test data storage |
| VS Code / PyCharm | Development IDE |
| Chromium | Browser execution |

### Prerequisites

Install the following before setting up the framework:

- Python 3.11 or compatible version
- Visual Studio Code or PyCharm
- Google Chrome, Microsoft Edge, or Chromium
- Git (optional, for version control)

Verify Python installation:

```powershell
python --version
```

Verify pip:

```powershell
pip --version
```

---

# 3. Project Folder Structure

The framework follows the Page Object Model design pattern.

```text
playwright_automation/
│
├── .venv/
│
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   └── admin_products_page.py
│
├── reports/
│   └── .gitkeep
│
├── screenshots/
│   └── .gitkeep
│
├── test_data/
│   ├── login_data.json
│   ├── test_cases.csv
│   └── admin_product_page.json
│
├── tests/
│   ├── __init__.py
│   ├── test_login.py
│   └── test_admin_products.py
│
├── .env
├── .env.example
├── .gitignore
├── conftest.py
├── pytest.ini
├── README.md
└── requirements.txt
```

**Note:** The Admin Products test filename above follows the existing project filename `test_admin_prodcts.py`. If your actual file is named `test_admin_products.py`, use that spelling in the execution commands.

### Folder responsibilities

**pages/**

Contains Page Object Model classes.

Each page class maintains:
- Page locators
- Page actions
- Reusable methods
- Navigation methods

**tests/**

Contains actual Pytest test cases and assertions.

Examples:
- Login tests
- Admin navigation tests
- Product listing tests
- Product creation tests
- Product editing tests

**test_data/**

Contains external test data.

JSON files are used to separate test inputs from automation code.

**reports/**

Stores generated execution reports.

**screenshots/**

Used for storing screenshots captured during test execution, when screenshot capture is configured.

**conftest.py**

Contains shared Pytest fixtures and hooks.

**pytest.ini**

Contains Pytest configuration, test discovery settings and custom markers.

**requirements.txt**

Contains Python dependencies required by the framework.

**.env**

Contains application URL and login credentials.

---

# 4. Framework Architecture

The framework follows the Page Object Model architecture.

```text
                 Pytest Test Execution
                          |
                          |
                    conftest.py
                          |
              Browser and Page Fixtures
                          |
                          |
                     Test Files
                          |
              -----------------------
              |                     |
          Login Tests         Admin Tests
              |                     |
              |                     |
          LoginPage          AdminProductsPage
              |                     |
              -----------------------
                          |
                       BasePage
                          |
                     Playwright
                          |
                    Web Browser
                          |
                    Toolshop App
```

### Execution flow

1. Pytest discovers the test files.
2. Pytest reads the configuration from `pytest.ini`.
3. `conftest.py` provides the required fixtures.
4. The browser and page are initialized.
5. The test function executes.
6. The test creates the required Page Object.
7. Page Object methods perform browser interactions.
8. Playwright locators identify the web elements.
9. Pytest assertions validate the actual application behavior.
10. Pytest records the test result.

---

# 5. Environment Setup

## Step 1: Clone or create the project

Open PowerShell or the terminal.

```powershell
mkdir playwright_automation
cd playwright_automation
```

Open the project in your IDE.

## Step 2: Create a virtual environment

```powershell
python -m venv .venv
```

The virtual environment isolates the dependencies required by this project.

## Step 3: Activate the virtual environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

After activation, the terminal should display:

```text
(.venv) PS C:\Users\...\playwright_automation>
```

If PowerShell blocks activation, use the appropriate execution policy for your environment.

## Step 4: Install dependencies

Create `requirements.txt`:

```text
pytest>=8.0
playwright>=1.45
pytest-playwright>=0.5
python-dotenv>=1.0
pytest-html>=4.1
```

Install all dependencies:

```powershell
pip install -r requirements.txt
```

## Step 5: Install Playwright browsers

```powershell
python -m playwright install
```

Alternatively, install Chromium only:

```powershell
python -m playwright install chromium
```

Playwright requires browser binaries in addition to the Python package.

## Step 6: Verify installations

```powershell
pytest --version
```

```powershell
python -m playwright --version
```

---

# 6. Environment Variables – .env

The framework uses Python Dotenv to load configuration values.

Create a `.env` file in the project root.

Example:

```text
BASE_URL=https://practicesoftwaretesting.com

ADMIN_USERNAME=your_admin_email
ADMIN_PASSWORD=your_admin_password

CUSTOMER_USERNAME=your_customer_email
CUSTOMER_PASSWORD=your_customer_password
```

Replace the example credentials with valid application credentials.

### Why use .env?

Storing credentials directly inside Python files is not recommended.

Using `.env` provides:

- Separation of configuration and code
- Easier environment switching
- Better credential management
- Reduced risk of accidentally committing credentials

### .env.example

Create a `.env.example` file containing placeholders:

```text
BASE_URL=https://practicesoftwaretesting.com

ADMIN_USERNAME=
ADMIN_PASSWORD=

CUSTOMER_USERNAME=
CUSTOMER_PASSWORD=
```

Do not commit the actual `.env` file to Git.

---

# 7. Base Page – base_page.py

The BasePage class is the parent class for all Page Object classes.

File: `pages/base_page.py`

```python
from playwright.sync_api import Page


class BasePage:

    def __init__(self, page: Page):
        self.page = page

    def open(self, url):
        self.page.goto(
            url,
            wait_until="domcontentloaded"
        )
```

### Explanation

**Page**

`Page` is a Playwright class representing a browser tab or page.

**Constructor**

```python
def __init__(self, page: Page):
    self.page = page
```

Receives the Playwright page object and stores it for reuse.

**open()**

Navigates to the provided URL.

### Why BasePage?

Without BasePage, every page class might need to implement common navigation functionality independently.

Using inheritance allows us to reuse common functionality.

For example:

```python
class LoginPage(BasePage):
```

```python
class AdminProductsPage(BasePage):
```

Both classes inherit from BasePage.

---

# 8. Page Object Model – Login Page

File: `pages/login_page.py`

The LoginPage class contains login-page locators and reusable login actions.

Responsibilities:

- Identify email field
- Identify password field
- Identify login button
- Enter credentials
- Submit login form
- Handle password visibility

Example locator declarations:

```python
email_locator = '[id="email"]'
password_locator = '//input[@id="password"]'
login_locator = '[type="submit"]'
```

### Locator strategies

| Locator | Type |
|---|---|
| `[id="email"]` | CSS attribute selector |
| `//input[@id="password"]` | XPath |
| `[type="submit"]` | CSS attribute selector |

### Why Page Object Model?

Instead of writing the same locator and action repeatedly in every test, we define them once in the Page Object.

For example:

```python
login_page.login(
    admin_email,
    admin_password
)
```

This method can be reused across multiple login scenarios.

---

# 9. Page Object Model – Admin Products Page

File: `pages/admin_products_page.py`

This class handles Admin Product Management functionality.

### Main responsibilities

- Navigate to Admin Products
- Verify product listing
- Search for products
- Reset search
- Navigate through pagination
- Open Add Product page
- Fill product details
- Select dropdown values
- Save products
- Search for products before editing

### Locator strategy

We prefer unique IDs and application-provided `data-test` attributes.

Example:

```python
name_locator = "#name"
description_locator = "#description"
stock_locator = "#stock"
price_locator = "#price"

location_offer_locator = "#is_location_offer"

co2_rating_locator = "#co2_rating"
brand_locator = "#brand_id"
category_locator = "#category_id"
image_locator = "#product_image_id"

save_product_locator = 'button[data-test="product-submit"]'
```

### CSS selector explanation

`#name` identifies an element using its HTML ID.

`button[data-test="product-submit"]` identifies a button using its `data-test` attribute.

### Playwright form actions

For text inputs:

```python
self.page.locator(self.name_locator).fill(
    product_data["name"]
)
```

For checkboxes:

```python
self.page.locator(
    self.location_offer_locator
).set_checked(
    product_data["location_offer"]
)
```

For dropdowns:

```python
self.page.locator(
    self.category_locator
).select_option(
    label=product_data["category"]
)
```

For buttons:

```python
self.page.locator(
    self.save_product_locator
).click()
```

---

# 10. Pytest Fixtures – conftest.py

The `conftest.py` file contains shared fixtures.

Fixtures are reusable setup and teardown functions provided by Pytest.

Examples include:

- Base URL
- Admin credentials
- Customer credentials
- Application browser page

Example implementation:

```python
import os

import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def base_url():

    url = os.getenv("BASE_URL")

    if not url:
        pytest.fail(
            "Set BASE_URL in environment variables"
        )

    return url.rstrip("/")


@pytest.fixture(scope="session")
def admin_user_credentials():

    admin_email = os.getenv("ADMIN_USERNAME")
    admin_pass = os.getenv("ADMIN_PASSWORD")

    if not admin_email or not admin_pass:
        pytest.fail(
            "Set ADMIN_USERNAME and ADMIN_PASSWORD"
        )

    return admin_email, admin_pass


@pytest.fixture(scope="session")
def customer_user_credentials():

    customer_email = os.getenv("CUSTOMER_USERNAME")
    customer_pass = os.getenv("CUSTOMER_PASSWORD")

    if not customer_email or not customer_pass:
        pytest.fail(
            "Set CUSTOMER_USERNAME and CUSTOMER_PASSWORD"
        )

    return customer_email, customer_pass


@pytest.fixture(scope="function")
def app_page(page):

    page.set_default_timeout(10_000)

    yield page
```

### Understanding fixture scopes

| Scope | Description |
|---|---|
| function | Runs separately for each test function |
| class | Shared within a test class |
| module | Shared within a Python test module |
| package | Shared within a package |
| session | Shared for the entire Pytest session |

### Our framework fixture usage

**base_url – session scope**

Loads the application URL once per test session.

**admin_user_credentials – session scope**

Loads admin credentials once per session.

**customer_user_credentials – session scope**

Loads customer credentials once per session.

**app_page – function scope**

Provides an isolated Playwright page for each test function.

The `page` fixture is provided by the Playwright-Pytest integration.

---

# 11. Test Data Management – JSON

The framework stores test data separately from the test implementation.

Example:

`test_data/admin_product_page.json`

```json
{
  "valid_product": {
    "name": "Golder Hammer",
    "description": "A durable hammer created for automation testing.",
    "stock": 50,
    "price": 99.99,
    "location_offer": false,
    "item_for_rent": false,
    "co2_rating": "None",
    "brand": "Tools",
    "category": "Hammer",
    "image": "Hammer"
  },
  "updated_product": {
    "name": "Golder Hammer Updated",
    "description": "Updated product description.",
    "stock": 75,
    "price": 109.99,
    "location_offer": false,
    "item_for_rent": false,
    "co2_rating": "None",
    "brand": "Tools",
    "category": "Hammer",
    "image": "Hammer"
  }
}
```

### Reading JSON data in Python

```python
import json
from pathlib import Path

TEST_DATA_FILE = (
    Path(__file__).resolve().parents[1]
    / "test_data"
    / "admin_product_page.json"
)

with TEST_DATA_FILE.open(encoding="utf-8") as file:
    TEST_DATA = json.load(file)
```

### Accessing JSON values

```python
product_name = TEST_DATA["valid_product"]["name"]
```

```python
product_price = TEST_DATA["valid_product"]["price"]
```

### Advantages

- Test data is separate from automation code.
- Multiple test data sets can be maintained.
- Data changes do not require changing page actions.
- The same Page Object methods can be reused with different JSON values.

---

# 12. Pytest Configuration – pytest.ini

The `pytest.ini` file controls how Pytest discovers and executes tests.

Example configuration:

```ini
[pytest]

testpaths = tests

python_files = test_*.py

python_classes = Test*

python_functions = test_*

markers =
    smoke: validating login test functionality
    regression: validating regression test functionality

addopts = -v
```

The exact marker descriptions should match the project's agreed test scope.

### Explanation

**testpaths**

```ini
testpaths = tests
```

Pytest searches the `tests` directory by default.

**python_files**

```ini
python_files = test_*.py
```

Pytest discovers Python files beginning with `test_`.

Examples:

```text
test_login.py
test_admin_prodcts.py
test_api.py
```

**python_classes**

```ini
python_classes = Test*
```

Test classes beginning with `Test` can be discovered.

**python_functions**

```ini
python_functions = test_*
```

Test functions beginning with `test_` can be discovered.

**markers**

Registers custom test markers to categorize tests.

---

# 13. How Pytest Test Discovery Works

Test discovery is the process by which Pytest identifies the test files, classes and functions to execute.

### Step 1: Pytest starts execution

When we execute:

```powershell
pytest
```

Pytest looks for `pytest.ini` and reads its configuration.

### Step 2: Pytest identifies test directories

Because we configured:

```ini
testpaths = tests
```

Pytest searches the `tests` directory.

### Step 3: Pytest identifies Python files

Because we configured:

```ini
python_files = test_*.py
```

Pytest identifies files whose names match the pattern.

Examples:

```text
test_login.py
test_admin_prodcts.py
```

A file named `login.py` will not be discovered automatically under this pattern.

### Step 4: Pytest identifies test functions

Because we configured:

```ini
python_functions = test_*
```

Pytest identifies functions beginning with `test_`.

Example:

```python
def test_admin_login():
    pass
```

This function is discovered.

However:

```python
def admin_login():
    pass
```

This is not discovered automatically.

### Step 5: Pytest identifies test classes

With:

```ini
python_classes = Test*
```

A class named:

```python
class TestLogin:
    def test_valid_login(self):
        pass
```

is discoverable.

### Step 6: Fixtures are resolved

When a discovered test function requests a fixture:

```python
def test_login(app_page, base_url):
```

Pytest searches for the relevant fixtures, including those defined in `conftest.py` and the installed Playwright plugin.

### Step 7: Tests are executed

Pytest runs the discovered tests and reports:

- PASSED
- FAILED
- SKIPPED
- ERROR
- XFAIL
- XPASS

---

# 14. Pytest Test Execution Commands

## A. Execute all test cases

```powershell
pytest
```

Runs all tests discovered according to the configured Pytest settings.

## B. Execute with verbose output

```powershell
pytest -v
```

Displays individual test names and their execution results.

## C. Execute with standard output

```powershell
pytest -s
```

Displays output from `print()` statements and other captured standard output.

## D. Execute with headed browser

```powershell
pytest --headed
```

Runs the browser in visible mode.

## E. Execute with slow motion

```powershell
pytest --headed --slowmo 1000
```

Adds a delay of 1000 milliseconds between browser actions, making it easier to observe interactions.

## F. Recommended full execution command

```powershell
pytest -v -s --headed --slowmo 1000
```

This command:

1. Discovers all configured tests.
2. Displays individual test names.
3. Displays print statements.
4. Opens the browser visibly.
5. Adds a one-second delay between browser actions.

**Note:** The `--headed` and `--slowmo` options are provided by Playwright's Pytest integration.

---

# 15. Executing Individual Test Files

Execute only login tests:

```powershell
pytest tests/test_login.py -v -s --headed
```

Execute only Admin Products tests:

```powershell
pytest tests/test_admin_prodcts.py -v -s --headed
```

If your filename is `test_admin_products.py`, use that exact filename instead.

### Execute one test function

```powershell
pytest tests/test_login.py::test_valid_admin_login -v -s --headed
```

### Execute one Admin Products test

```powershell
pytest tests/test_admin_prodcts.py::test_create_new_product -v -s --headed
```

This is useful when debugging a particular scenario.

---

# 16. Pytest Markers

Markers allow us to categorize tests and execute selected groups.

We use two primary custom markers:

- smoke
- regression

### Smoke testing

Smoke testing verifies important basic application functionality.

Example:

```python
@pytest.mark.smoke
def test_valid_admin_login():
    pass
```

Execute smoke tests:

```powershell
pytest -m smoke -v -s --headed
```

### Regression testing

Regression testing checks existing functionality to ensure that application changes have not broken previously working features.

Example:

```python
@pytest.mark.regression
def test_product_listing():
    pass
```

Execute regression tests:

```powershell
pytest -m regression -v -s --headed
```

### Execute both markers

```powershell
pytest -m "smoke or regression" -v -s --headed
```

### Execute tests belonging to both markers

```powershell
pytest -m "smoke and regression" -v -s --headed
```

### Exclude a marker

```powershell
pytest -m "not regression" -v -s --headed
```

### Important distinction

`or` means either marker can match.

`and` means the test must have both markers.

`not` excludes tests with that marker.

A marker does not automatically make a test a smoke or regression test. The marker must be assigned to the test function or class.

---

# 17. Current Test Coverage

## Login Module

The Login module covers the following scenarios:

| Test ID | Scenario |
|---|---|
| TC-001 | Submit login with empty credentials |
| TC-002 | Submit invalid email format |
| TC-003 | Submit short password |
| TC-004 | Submit invalid email and password |
| TC-005 | Verify email and password placeholders |
| TC-006 | Verify password masking |
| TC-007 | Verify password visibility toggle |
| TC-008 | Login using valid admin credentials |
| TC-009 | Login using valid customer credentials |

## Admin Product Management Module

| Test ID | Scenario |
|---|---|
| TC-010 | Navigate to Admin Products section |
| TC-011 | Verify product listing |
| TC-012 | Verify product pagination |
| TC-013 | Verify previous-page navigation |
| TC-014 | Search for an existing product |
| TC-015 | Skipped – Non-existing product search |
| TC-016 | Skipped – Product filters |
| TC-017 | Validate mandatory fields |
| TC-018 | Create a new product with valid details |
| TC-019 | Verify newly created product information |
| TC-020 | Edit the newly created product – temporarily skipped |
| TC-021 | Verify updated product information – temporarily skipped |

### Current product creation behavior

After clicking Save, the application may remain on:

```text
/admin/products/add
```

Therefore, the test does not assume automatic navigation to the Products listing.

The subsequent product verification test navigates explicitly to:

```text
/admin/products
```

It searches for `Golder Hammer` and verifies that the saved product appears.

### Current editing status

The editing tests are temporarily skipped using `pytest.skip()` because the application is not currently completing the edit operation reliably.

The editing implementation is retained for future investigation.

---

# 18. Test Assertions

Pytest assertions and Playwright's `expect()` are used to validate application behavior.

Examples:

### Verify page URL

```python
expect(page).to_have_url(
    "https://practicesoftwaretesting.com/admin/products"
)
```

### Verify element visibility

```python
expect(page.locator("#name")).to_be_visible()
```

### Verify text

```python
expect(
    page.get_by_text("Name is required", exact=True)
).to_be_visible()
```

### Verify input value

```python
expect(
    page.locator("#name")
).to_have_value("Golder Hammer")
```

### Verify element count

```python
expect(
    page.locator("table tbody tr")
).to_have_count(5)
```

### Verify that an element is not visible

```python
expect(
    page.locator(".error-message")
).not_to_be_visible()
```

### Why use Playwright expect?

Playwright assertions automatically retry until the expected condition is met or the configured timeout expires.

This is generally more reliable than using fixed sleep statements.

---

# 19. HTML Test Reports

The framework uses `pytest-html` to generate an HTML execution report.

Install it using:

```powershell
pip install pytest-html
```

Execute tests with:

```powershell
pytest -v -s --html=reports/login_test_report.html --self-contained-html
```

For Admin Products:

```powershell
pytest tests/test_admin_prodcts.py -v -s --html=reports/admin_products_report.html --self-contained-html
```

### Report contents

The HTML report provides:

- Total number of tests
- Passed tests
- Failed tests
- Skipped tests
- Test names
- Execution details
- Failure information

Open the generated HTML report in a browser.

---

# 20. Screenshots and Logging

The project contains dedicated folders:

```text
screenshots/
reports/
```

Screenshots can be captured using Playwright:

```python
page.screenshot(
    path="screenshots/test_failure.png",
    full_page=True
)
```

### Capture screenshots on failure

Pytest provides the `pytest_runtest_makereport` hook, which can be used to identify whether a test passed or failed.

This hook can be used in `conftest.py` to capture screenshots based on the test result.

Example:

```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        page = item.funcargs.get("app_page")

        if page:
            page.screenshot(
                path=f"screenshots/{item.name}.png",
                full_page=True
            )
```

This is an example hook. It must be integrated with the existing `conftest.py` implementation and screenshot naming should be made unique when necessary.

### Logging

Python's built-in logging module can be used to record:

- Test execution start
- Navigation actions
- Login attempts
- Product creation actions
- Test failures
- Exceptions

Logs can be configured to be stored in the reports directory.

---

# 21. Browser Execution

Playwright supports multiple browser engines.

| Browser | Playwright engine |
|---|---|
| Chromium | Chromium |
| Firefox | Firefox |
| WebKit | WebKit |

### Chromium

```powershell
pytest --browser chromium -v -s --headed
```

### Firefox

```powershell
pytest --browser firefox -v -s --headed
```

### WebKit

```powershell
pytest --browser webkit -v -s --headed
```

### Microsoft Edge

When Microsoft Edge is installed:

```powershell
pytest --browser chromium --browser-channel msedge -v -s --headed
```

### Google Chrome

```powershell
pytest --browser chromium --browser-channel chrome -v -s --headed
```

WebKit is the browser engine used by Playwright for WebKit testing; it is not identical to testing the actual Safari application on macOS.

---

# 22. Debugging Failed Tests

When a test fails, follow this approach:

### Step 1: Identify the failed test

Look at the Pytest short test summary.

Example:

```text
FAILED tests/test_admin_prodcts.py::test_create_new_product
```

### Step 2: Read the error message

Identify whether the problem is related to:

- Locator
- Assertion
- Timeout
- URL
- Test data
- Fixture
- Application behavior

### Step 3: Run only the failed test

```powershell
pytest tests/test_admin_prodcts.py::test_create_new_product -v -s --headed --slowmo 1000
```

### Step 4: Inspect the element

Use browser Developer Tools to inspect:

- HTML element
- ID
- Name
- Class
- `data-test`
- Input type
- Dropdown options

### Step 5: Update the correct layer

| Problem | File to investigate |
|---|---|
| Incorrect locator | Page Object file |
| Incorrect test data | JSON file |
| Incorrect assertion | Test file |
| Missing fixture | conftest.py |
| Incorrect marker | pytest.ini or test file |
| Missing dependency | requirements.txt |

### Step 6: Rerun the test

Verify the correction before running the entire suite.

---

# 23. Git and Version Control

Git can be used to maintain framework changes.

Initialize Git:

```powershell
git init
```

Check modified files:

```powershell
git status
```

Add files:

```powershell
git add .
```

Commit changes:

```powershell
git commit -m "Initial Playwright automation framework"
```

### Recommended .gitignore

```text
.venv/
__pycache__/
.pytest_cache/
.env

reports/*
!reports/.gitkeep

screenshots/*
!screenshots/.gitkeep

*.pyc
```

Do not commit real passwords, generated temporary files or local virtual environments.

---

# 24. Common Pytest Commands – Quick Reference

| Requirement | Command |
|---|---|
| Run all tests | `pytest` |
| Verbose output | `pytest -v` |
| Show print statements | `pytest -s` |
| Visible browser | `pytest --headed` |
| Slow browser actions | `pytest --headed --slowmo 1000` |
| Run all tests visibly | `pytest -v -s --headed --slowmo 1000` |
| Run login module | `pytest tests/test_login.py -v -s` |
| Run Admin Products module | `pytest tests/test_admin_prodcts.py -v -s` |
| Run one test | `pytest tests/test_admin_prodcts.py::test_create_new_product -v -s` |
| Run smoke tests | `pytest -m smoke -v -s` |
| Run regression tests | `pytest -m regression -v -s` |
| Run both markers | `pytest -m "smoke or regression" -v -s` |
| Exclude regression | `pytest -m "not regression" -v -s` |
| Generate HTML report | `pytest --html=reports/report.html --self-contained-html` |
| Run on Firefox | `pytest --browser firefox -v -s` |
| Run on WebKit | `pytest --browser webkit -v -s` |
| Run on Chrome | `pytest --browser chromium --browser-channel chrome -v -s` |

---

# 25. Best Practices Followed

The following practices are followed in this framework:

1. Page Object Model for reusable page actions.
2. BasePage inheritance for common browser functionality.
3. Locators maintained separately from test assertions.
4. JSON-based test data management.
5. Environment variables for credentials.
6. Pytest fixtures for reusable setup.
7. Unique IDs and `data-test` attributes preferred for locators.
8. Playwright auto-waiting and assertions.
9. Independent test functions where possible.
10. Meaningful test function names.
11. Smoke and regression test categorization.
12. HTML report generation.
13. Screenshots for failure investigation when configured.
14. Browser-specific test execution.
15. No hardcoded credentials in source files.

---

# 26. Future Enhancements

Potential improvements for the next framework versions:

- API automation using Playwright APIRequestContext or Requests.
- Database validation using SQL.
- Allure reporting.
- CI/CD integration using GitHub Actions or Jenkins.
- Cross-browser execution.
- Data-driven testing with multiple JSON test datasets.
- Parallel test execution.
- Better failure screenshot and logging integration.
- Automated test cleanup for created products.
- Investigation and restoration of Edit Product functionality.

---

# 27. Final Execution Workflow

The normal workflow for executing this framework is:

**Step 1:** Activate the virtual environment.

```powershell
.venv\Scripts\Activate.ps1
```

**Step 2:** Verify the application URL and credentials in `.env`.

**Step 3:** Run all tests.

```powershell
pytest -v -s --headed --slowmo 1000
```

**Step 4:** Review the terminal output.

**Step 5:** Investigate failed tests individually.

**Step 6:** Generate and review the HTML report.

```powershell
pytest -v -s --html=reports/automation_report.html --self-contained-html
```

**Step 7:** Review screenshots and logs if configured.

**Step 8:** Commit verified changes to Git.

---

# Conclusion

This framework provides a structured foundation for end-to-end UI automation using Python, Playwright and Pytest.

By following Page Object Model, reusable fixtures, external test data, custom markers and reporting, the framework is designed to support maintainable automation as the application and test coverage grow.

**Framework:** Python + Playwright + Pytest  
**Design Pattern:** Page Object Model  
**Application:** Practice Software Testing – Toolshop  
**Primary Modules:** Login and Admin Product Management  
**Execution:** Pytest CLI  
**Reporting:** Pytest-HTML