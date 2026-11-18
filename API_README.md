# Toolshop API Automation Framework

## 1. Project Overview

This project implements API automation testing for the Practice Software Testing Toolshop application using:

- Python
- Pytest
- Requests
- JSON test data
- Pytest fixtures
- Bearer token authentication

The framework follows a reusable structure to support positive, negative, authentication, and response-schema validation scenarios.

**Application:** https://practicesoftwaretesting.com/

**API Base URL:** https://api.practicesoftwaretesting.com/

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Pytest | Test execution framework |
| Requests | HTTP API requests |
| JSON | External test data |
| python-dotenv | Environment variable management |
| Pytest HTML | Execution reports, if configured |

## 3. Current API Test Coverage

The following three API test cases have been implemented and successfully executed.

| Test ID | Test Scenario | HTTP Method | Endpoint | Expected Status | Result |
|---|---|---|---|---|---|
| API-001 | Retrieve product list | GET | `/products` | 200 | Passed |
| API-002 | Retrieve product details using an ID | GET | `/products/{productId}` | 200 | Passed |
| API-003 | Create a new product | POST | `/products` | 201 | Passed |
| API-004 | Update existing product details | PUT | `/products/{productId}` | Pending |

### API-001 – Retrieve Product List

- Send a GET request to `/products`.
- Validate HTTP status code.
- Validate response content type.
- Validate pagination fields.
- Validate product list.
- Validate product field data types.

### API-002 – Retrieve Product Details Using an ID

- Retrieve the product list.
- Extract a product ID dynamically.
- Send a GET request using the extracted ID.
- Validate the response status.
- Verify the returned product ID.
- Validate product information and data types.

### API-003 – Create a New Product

- Read product information from an external JSON file.
- Authenticate using admin credentials.
- Generate a Bearer access token.
- Retrieve valid brand, category, and image IDs dynamically.
- Send a POST request to create the product.
- Validate HTTP 201.
- Verify the returned product details and generated ID.

## 4. Project Structure

```text
playwright_automation/
│
├── api/
│   └── api_client.py
│
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   └── admin_products_page.py
│
├── tests/
│   ├── test_login.py
│   ├── test_admin_prodcts.py
│   └── test_api_products.py
│
├── test_data/
│   ├── login_data.json
│   ├── admin_product_page.json
│   └── api_product_data.json
│
├── reports/
├── screenshots/
│
├── conftest.py
├── pytest.ini
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
```

## 5. Prerequisites

Install the following before running the project:

- Python 3.10 or above
- Git
- Visual Studio Code or PyCharm
- Internet connection

## 6. Clone the Repository

```bash
git clone https://github.com/Lakshminarayana1214/playwright-python-pytest-framework.git
```

Navigate to the project directory:

```bash
cd playwright-python-pytest-framework
```

## 7. Create and Activate Virtual Environment

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## 8. Install Dependencies

```bash
pip install -r requirements.txt
```

Install Playwright browser binaries if you also intend to execute the UI automation tests:

```bash
python -m playwright install
```

## 9. Environment Configuration

Create a `.env` file in the project root.

Configure the required values using `.env.example` as a reference.

Typical settings include:

```env
BASE_URL=https://practicesoftwaretesting.com
API_BASE_URL=https://api.practicesoftwaretesting.com

ADMIN_USERNAME=your_admin_email
ADMIN_PASSWORD=your_admin_password

CUSTOMER_USERNAME=your_customer_email
CUSTOMER_PASSWORD=your_customer_password
```

Use valid credentials for the test environment.

**Security:** Never commit `.env` or actual credentials to GitHub. Keep `.env` in `.gitignore`.

## 10. API Automation Execution

### Execute all API tests

```bash
pytest tests/test_api_products.py -v -s
```

### Execute API-001

```bash
pytest tests/test_api_products.py::test_get_api_products_list -v -s
```

### Execute API-002

```bash
pytest tests/test_api_products.py::test_get_product_details_by_id -v -s
```

### Execute API-003

```bash
pytest tests/test_api_products.py::test_create_new_product -v -s
```

### Execute API-004

```bash
pytest tests/test_api_products.py::test_update_existing_product -v -s
```

API-004 is currently implemented but its execution result has not yet been confirmed.

## 11. Pytest Command Options

| Command | Description |
|---|---|
| `pytest -v` | Verbose test execution |
| `pytest -s` | Display print statements |
| `pytest -v -s` | Verbose execution with console output |
| `pytest -m api -v -s` | Execute tests marked as API |
| `pytest tests/test_api_products.py -v -s` | Execute API product tests |
| `pytest --collect-only` | Display discovered tests without executing |
| `pytest -q` | Quiet execution output |

### Test Discovery

Pytest discovers test files using the `test_*.py` or `*_test.py` naming conventions.

Test functions must start with `test_`.

For example:

```python
def test_get_api_products_list():
    pass
```

Pytest discovers this function automatically.

### Markers

The API tests use:

```python
@pytest.mark.api
```

Run all tests with the API marker:

```bash
pytest -m api -v -s
```

## 12. Framework Design

### API Client

The `api_client.py` module provides reusable HTTP methods:

- GET
- POST
- PUT

The client centralizes request handling, headers, authentication, and timeout configuration.

### Pytest Fixtures

Fixtures in `conftest.py` provide reusable setup functionality, including:

- API client initialization
- Admin authentication
- Bearer token generation
- Test product creation for update scenarios

### Test Data Management

Test data is maintained separately in JSON files.

Example:

`test_data/api_product_data.json`

This separates test inputs from test implementation and makes the framework easier to maintain.

## 13. Reports

If pytest-html is configured in the project, generate a report using:

```bash
pytest tests/test_api_products.py -v -s --html=reports/api_test_report.html --self-contained-html
```

Open the generated HTML report in a browser.

## 14. GitHub Repository

Repository:

https://github.com/Lakshminarayana1214/playwright-python-pytest-framework

Clone command:

```bash
git clone https://github.com/Lakshminarayana1214/playwright-python-pytest-framework.git
```

## 15. Future API Automation Scope

The following scenarios are planned for future implementation:

- API-004: Update existing product details
- API-005: Validate invalid request payloads
- API-006: Test unauthorized API requests
- API-007: Validate response status codes and response schemas

## 16. Important Notes

- Use valid test-environment credentials.
- Do not commit passwords, tokens, or `.env` files.
- Use dynamic product IDs wherever possible.
- Keep API tests independent of their execution order.
- Use reusable fixtures and API client methods.
- Validate both HTTP status codes and response content.
- Review test results before considering a scenario complete.

---

**Project:** Toolshop UI and API Automation Framework  
**Automation:** Python + Pytest + Playwright + Requests  
**Repository:** GitHub