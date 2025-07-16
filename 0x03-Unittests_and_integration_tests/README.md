# Unit Testing Guide for `utils.py`

This document explains the testing process for the utility functions defined in `utils.py`.

## 📁 Project Structure


## 🧪 Tested Functions

We are testing the following functions from `utils.py`:

- `access_nested_map`
- `get_json` *(optional, not covered in this file yet)*
- `memoize` *(optional, not covered in this file yet)*

### ✔️ `access_nested_map`

This function takes a nested mapping and a path (sequence of keys) and returns the value found at that path. The function raises `KeyError` if any key is not found along the path.

---

## 🛠️ Setting Up the Environment

### 1. Install Python Dependencies

Ensure you have Python 3.6+ and the `parameterized` module installed:

```bash
pip install parameterized
