import requests
import json
import logging

from config.settings import SHOP, TOKEN

logger = logging.getLogger(__name__)


class ShopifyClient:

    def __init__(self):
        self.base_url = f"https://{SHOP}/admin/api/2025-01"
        self.headers = {
            "X-Shopify-Access-Token": TOKEN,
            "Content-Type": "application/json"
        }

    def get_products(self):
        url = f"{self.base_url}/products.json"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            raw_data = response.json()

            logger.info("Successfully fetched products from Shopify")

            # return both raw response and parsed products
            return raw_data["products"]

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching products: {e}")
            raise

    def get_inventory(self, inventory_item_id):

        url = f"{self.base_url}/inventory_levels.json?inventory_item_ids={inventory_item_id}"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            raw_data = response.json()

            if raw_data["inventory_levels"]:
                return raw_data, raw_data["inventory_levels"][0]["available"]

            return raw_data, 0

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching inventory for {inventory_item_id}: {e}")
            raise