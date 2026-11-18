import logging
import os
import re
from pathlib import Path

import pytest
import pytest_html
from dotenv import load_dotenv

load_dotenv()

project_path = Path(__file__).resolve().parent

reports_path = project_path / "reports"
screenshots_path = project_path / "screenshots"

log_file = reports_path / "test_execution.log"

logging.basicConfig(
    filename=log_file,
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("automation")

# Create directories if they do not exist
reports_path.mkdir(parents=True, exist_ok=True)
screenshots_path.mkdir(parents=True, exist_ok=True)

@pytest.fixture(scope="session")
def base_url():
    url = os.getenv("BASE_URL")
    if not url:
        pytest.fail("set base url in env variables")

    return url.rstrip("/")

@pytest.fixture(scope="session")
def admin_user_credentials():
    admin_email = os.getenv("ADMIN_USERNAME")
    admin_pass = os.getenv("ADMIN_PASSWORD")
    if not admin_email or not admin_pass:
        pytest.fail("set admin username and password in env variables")

    return admin_email, admin_pass

@pytest.fixture(scope="session")
def customer_user_credentials():
    customer_email = os.getenv("CUSTOMER_USERNAME")
    customer_pass = os.getenv("CUSTOMER_PASSWORD")
    if not customer_email or not customer_pass:
        pytest.fail("set customer username and password in env variables")

    return customer_email, customer_pass

@pytest.fixture(scope="function")
def app_page(page):
    page.set_default_timeout(10_000)
    yield page

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    # Process the actual test execution result
    if report.when == "call":

        test_status = "PASSED" if report.passed else "FAILED"

        # Write test execution result to log
        logger.info(
            "%s : %s",
            test_status,
            item.nodeid
        )

        # Get the Playwright page fixture
        page = item.funcargs.get("app_page")

        if page:

            # Create a safe screenshot filename
            safe_name = re.sub(
                r"[^A-Za-z0-9_.-]+",
                "_",
                item.nodeid
            )

            screenshot_file = (
                screenshots_path /
                f"{safe_name}-{test_status}.png"
            )

            try:
                # Capture screenshot
                page.screenshot(
                    path=str(screenshot_file),
                    full_page=True
                )

                logger.info(
                    "Screenshot saved: %s",
                    screenshot_file
                )

                # Attach screenshot to HTML report
                extra = getattr(report, "extras", [])

                extra.append(
                    pytest_html.extras.image(
                        str(screenshot_file),
                        name="Execution Screenshot"
                    )
                )

                report.extras = extra

            except Exception:
                logger.exception(
                    "Screenshot capture failed for %s",
                    item.nodeid
                )

        # Log failure details
        if report.failed:
            logger.error(
                "Test failure details: %s",
                report.longrepr
            )
