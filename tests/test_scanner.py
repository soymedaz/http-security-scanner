import unittest

from src.scanner import normalize_url


class TestScanner(unittest.TestCase):

    def test_add_https_to_domain(self):
        result = normalize_url("example.com")

        self.assertEqual(
            result,
            "https://example.com"
        )

    def test_keep_https(self):
        result = normalize_url(
            "https://example.com"
        )

        self.assertEqual(
            result,
            "https://example.com"
        )

    def test_keep_http(self):
        result = normalize_url(
            "http://example.com"
        )

        self.assertEqual(
            result,
            "http://example.com"
        )

    def test_reject_empty_url(self):
        with self.assertRaises(ValueError):
            normalize_url("")

    def test_reject_invalid_url(self):
        with self.assertRaises(ValueError):
            normalize_url(
                "this is not a valid URL"
            )


if __name__ == "__main__":
    unittest.main()