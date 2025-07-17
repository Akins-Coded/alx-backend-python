#!/usr/bin/env python3
"""Unittest module for testing GithubOrgClient behavior."""
import unittest
from unittest.mock import patch, PropertyMock
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

    def test_public_repos_url(self) -> None:
        """
        Test that the _public_repos_url property returns the correct URL
        based on the org's repos_url.
        """
        expected = "https://api.github.com/orgs/test-org/repos"
        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": expected
            }
            client = GithubOrgClient("test-org")
            result = client._public_repos_url
            self.assertEqual(result, expected)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Unit-test GithubOrgClient.public_repos with mocks"""
        mock_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "mit"}},
        ]
        mock_get_json.return_value = mock_repos_payload

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = (
                "https://api.github.com/orgs/test-org/repos"
            )

            client = GithubOrgClient("test-org")
            result = client.public_repos()

            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)

            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test-org/repos"
            )


if __name__ == "__main__":
    unittest.main()
