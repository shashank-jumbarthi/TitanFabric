import unittest

from backend.catalog import estimate_quote, get_fabric, list_fabrics


class CatalogTests(unittest.TestCase):
    def test_list_fabrics_can_filter_sustainable_items(self):
        fabrics = list_fabrics(sustainable=True)
        self.assertTrue(fabrics)
        self.assertTrue(all(item["sustainable"] for item in fabrics))

    def test_get_fabric_returns_none_for_unknown_id(self):
        self.assertIsNone(get_fabric("missing"))

    def test_estimate_quote_enforces_minimum_yardage(self):
        quote = estimate_quote([{"fabric_id": "tf-linen-01", "yards": 1}])
        self.assertEqual(quote["items"][0]["yards"], 25)
        self.assertGreater(quote["total"], quote["subtotal"])


if __name__ == "__main__":
    unittest.main()
