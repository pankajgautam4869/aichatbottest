# Chat Test Framework

## Overview
This framework is designed for automated testing of chat applications using Playwright and Python. It includes comprehensive test suites for chat functionality, security testing, and widget testing.

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher (for Playwright)
- Git

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scriptsctivate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install
```

5. Install Node.js dependencies (if any):
```bash
npm install
```

## Configuration

1. Update the configuration in `config/config.json`:
```json
{
    "base_url": "your-application-url",
    "auth": {
        "email": "your-email",
        "password": "your-password"
    },
    "viewport_sizes": {
        "desktop": {"width": 1280, "height": 800},
        "mobile": {"width": 375, "height": 667}
    }
}
```

## Running Tests

### Running All Tests
```bash
pytest
```

### Running Security Tests with HTML Report
```bash
# Create reports directory if it doesn't exist
mkdir -p reports

# Run security tests with HTML report
python3 -m pytest tests/test_security.py -v --html=reports/security_test_report.html --self-contained-html
```

### Running Chat Widget Tests with HTML Report
```bash
# Run chat widget tests with HTML report
python3 -m pytest tests/test_chat_widget.py -v --html=reports/chat_widget_test_report.html 
```

### Running Tests with Different Viewports
```bash
# Run tests for desktop viewport
pytest -m desktop

# Run tests for mobile viewport
pytest -m mobile
```

### Running Tests with Different Languages
```bash
# Run tests in English (default)
pytest --language=en

# Run tests in Arabic
pytest --language=ar
```

## Test Reports

After running tests, you can find the HTML reports in the `reports` directory:
- `reports/security_test_report.html` - Security test results
- `reports/chat_widget_test_report.html` - Chat widget test results
- `reports/screenshots/` - Test failure screenshots
- `reports/videos/` - Test execution videos (if enabled)

## Project Structure

```
├── config/             # Configuration files
├── data/              # Test data files
├── pages/             # Page Object Models
├── reports/           # Test reports and artifacts
├── tests/             # Test files
│   ├── test_security.py
│   ├── test_chat_widget.py
│   └── conftest.py
├── utils/             # Utility functions
├── requirements.txt   # Python dependencies
├── pytest.ini        # Pytest configuration
└── README.md         # This file
```

## Features

- Cross-browser testing with Playwright
- Responsive testing (desktop and mobile viewports)
- Multi-language support (English and Arabic)
- Security testing suite
- Chat widget testing
- HTML test reports
- Screenshot capture on test failures
- Video recording of test execution
- Retry mechanism for flaky tests

## Troubleshooting

1. If you encounter browser installation issues:
```bash
playwright install --force
```

2. If you see SSL certificate errors:
```bash
# Add --ignore-ssl-errors flag
pytest --ignore-ssl-errors
```

3. For timeout issues, adjust the timeout in `conftest.py`:
```python
@pytest.fixture(scope="function")
def browser_context(browser: Browser) -> BrowserContext:
    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        ignore_https_errors=True,
        timeout=30000  # Adjust timeout as needed
    )
    return context
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
# aichatbottest
