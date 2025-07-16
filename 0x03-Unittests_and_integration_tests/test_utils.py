#!/usr/bin/env python3
"""Unittest module for testing utility functions defined in utils.py."""

import unittest
from typing import Mapping, Sequence, Any, Dict
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test suite for verifying the behavior of access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: Mapping,
        path: Sequence,
        expected: Any
    ) -> None:
        """
        Test that access_nested_map returns the correct value
        for the given nested path.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: Mapping,
        path: Sequence
    ) -> None:
        """
        Test that access_nested_map raises KeyError with the
        correct message when a key is missing in the path.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(
            str(context.exception),
            repr(context.exception.args[0])
        )


class TestGetJson(unittest.TestCase):
    """Test suite for verifying the behavior of get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(
        self,
        test_url: str,
        test_payload: Dict
    ) -> None:
        """
        Test that get_json returns the correct dictionary and that
        requests.get is called exactly once with the correct URL.
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        with patch(
            "utils.requests.get",
            return_value=mock_response
        ) as mock_get:
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test suite for verifying the behavior of the memoize decorator."""

    def test_memoize(self) -> None:
        """
        Test that memoize caches the result of a method so that
        the method is only executed once even if accessed multiple times.
        """

        class TestClass:
            """Simple test class to apply the memoize decorator."""

            def a_method(self) -> int:
                """Method that returns a fixed integer."""
                return 42

            @memoize
            def a_property(self) -> int:
                """Memoized property that calls a_method once."""
                return self.a_method()

        with patch.object(
            TestClass,
            'a_method',
            return_value=42
        ) as mock_method:
            test_obj = TestClass()
            result1 = test_obj.a_property
            result2 = test_obj.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
