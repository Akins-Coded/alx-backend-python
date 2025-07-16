
---

## 🛠️ Utilities in `utils.py`

- `access_nested_map(nested_map, path)`  
  Accesses a nested dictionary structure using a sequence of keys.

- `get_json(url)`  
  Fetches and parses JSON from a remote HTTP GET request.

- `memoize(fn)`  
  Decorator that caches the result of a method the first time it is called.

Each of these functions is unit tested in `test_utils.py`.

---

## 🧪 Running Tests

### Prerequisites

- Python 3.13
- Ubuntu 18.04-compatible environment
- `parameterized` library (install with pip)

### Install Dependencies

```bash
pip install parameterized
