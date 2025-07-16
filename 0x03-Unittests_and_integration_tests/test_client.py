#!/usr/bin/env python3
"""Unittest module for testing GithubOrgClient behavior."""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get_json) -> None:
        """
        Test that GithubOrgClient.org returns the expected result
        and get_json is called exactly once with the correct URL.
        """
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.return_value = {"login": org_name}

        client = GithubOrgClient(org_name)
        result = client.org

        # Ensure get_json is called once with the expected URL
        mock_get_json.assert_called_once_with(expected_url)

        # Ensure returned data matches the mocked return value
        self.assertEqual(result, {"login": org_name})


if __name__ == "__main__":
    unittest.main()
