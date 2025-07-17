# Unittests and Integration Tests

This project focuses on writing unit and integration tests for Python code using the `unittest` module. The goal is to ensure code reliability, correctness, and maintainability through testing.

## 📁 Directory Structure

```
.
├── client.py                  # GitHubOrgClient implementation
├── utils.py                   # Utility functions with caching and HTTP get_json
├── test_client.py             # Unit and integration tests for client.py
├── test_utils.py              # Unit tests for utils.py
├── fixtures.py                # Static payloads for integration testing
└── README.md                  # Project documentation (this file)
```

## 🔧 Features Covered

- **Unit testing**
- **Integration testing**
- **Mocking external HTTP requests**
- **Memoization testing**
- **PEP8 Compliance** using `pycodestyle`
- **Parameterized tests** with `parameterized`

## 🧪 Running Tests

```bash
$ python3 -m unittest discover
```

Or run a specific file:

```bash
$ python3 test_client.py
```

## ✅ Lint Check (PEP8)

To check for style issues, run:

```bash
$ pycodestyle test_client.py
```

Fix issues like:
- E501: line too long
- W291: trailing whitespace
- W293: blank line with whitespace

## 🧰 Tools Used

- `unittest`
- `unittest.mock`
- `parameterized`
- `requests`
- `pycodestyle`

## 💾 Setup

Install dependencies:

```bash
$ pip install requests parameterized pycodestyle
```

## 📝 Author

Akindipe Muheez