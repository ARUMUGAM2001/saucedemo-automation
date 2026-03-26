# Saucedemo Automation Framework

End-to-end UI automation framework for [saucedemo.com](https://www.saucedemo.com) built with Python, Selenium, and pytest.

---

## Tech Stack

- Python 3.14
- Selenium 4
- pytest
- pytest-html
- Page Object Model (POM)

---

## Project Structure
```
e2e_project/
├── e2e_class_Structure_flow.py   # Page classes (POM)
├── conftest.py                   # Shared pytest fixtures
├── test_e2e_class_Structure_flow.py  # Test cases
├── pytest.ini                    # pytest configuration
└── .gitignore

```

---

## Test Cases

| Test | Description |
|------|-------------|
| `test_login` | Validates successful login with valid credentials |
| `test_add_to_cart` | Adds all items to cart and validates count |
| `test_checkout` | Completes full purchase flow end to end |

---

## How to Run

**Install dependencies:**
```bash
pip install selenium pytest pytest-html
```

**Run all tests:**
```bash
pytest
```

**Run specific test:**
```bash
pytest test_e2e_class_Structure_flow.py::test_login -v
```

**Generate HTML report:**
```bash
pytest --html=report.html --self-contained-html
```

---

## Page Classes

| Class | Responsibility |
|-------|---------------|
| `BrowserConfig` | Chrome driver setup and configuration |
| `SauceDemoPage` | Base class — shared driver and wait instance |
| `LoginPage` | Login page interactions |
| `InventoryPage` | Product listing, add to cart, price validation |
| `CartPage` | Cart validation and checkout navigation |
| `CheckoutPage` | Customer info form and order completion |

---

## Author

**Arumugam**   
[GitHub](https://github.com/ARUMUGAM2001)