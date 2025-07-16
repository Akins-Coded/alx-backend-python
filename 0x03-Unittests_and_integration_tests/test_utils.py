#!/usr/bin/env python3
"""Unittest module for testing utility functions in utils.py."""

import unittest
from typing import Mapping, Sequence, Any
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock

class TestAccessNestedMap(unittest.TestCase):
    """Test suite for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence, expected: Any) -> None:
        """Test access_nested_map returns correct value for given path."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping, path: Sequence) -> None:
        """Test access_nested_map raises KeyError with correct message on missing key."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        
        self.assertEqual(str(context.exception), repr(context.exception.args[0]))



class TestGetJson(unittest.TestCase):
    """Test suite for get_json function in utils.py."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: dict) -> None:
        """Test that get_json returns expected payload without real HTTP calls."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        with patch("utils.requests.get", return_value=mock_response) as mock_get:
            result = get_json(test_url)

            # Check that requests.get was called exactly once with the correct URL
            mock_get.assert_called_once_with(test_url)

            # Check that get_json returns the correct payload
            self.assertEqual(result, test_payload)

class TestMemoize(unittest.TestCase):
    """Test suite for memoize decorator in utils.py."""

    def test_memoize(self) -> None:
        """Test that memoize caches the result of a method."""
        class TestClass:

            def a_method(self):
                print("a_method called")
                return 42
            
            @memoize
            def a_property(self):
                return self.a_method() 
        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            test_obj = TestClass()
            # First call should invoke a_method
            result1 = test_obj.a_property

            # second call should return cached result
            result2 = test_obj.a_property

            # Ensure a_method is corect both times

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            #ensure the value is correct both times
            mock_method.assert_called_once()
            
if __name__ == "__main__":
    unittest.main()
