import logging

logger = logging.getLogger(__name__)


class ProductTransformer:

    def transform(self, products, client):

        logger.info("Starting product transformation")

        staging_rows = []

        for product in products:

            for variant in product.get("variants", []):

                try:

                    inventory_raw, inventory = client.get_inventory(
                        variant.get("inventory_item_id")
                    )

                    sku = variant.get("sku")
                    price = variant.get("price")

                    staging_rows.append({
                        "product_id": str(product.get("id")),
                        "title": product.get("title"),
                        "sku": sku,
                        "price": float(price) if price else None,
                        "inventory_quantity": int(inventory) if inventory else None,

                        # Data quality flags
                        "missing_sku": sku is None or sku == "",
                        "missing_price": price is None or price == ""
                    })

                except Exception as e:

                    logger.error(
                        f"Error transforming product {product.get('id')}: {e}"
                    )

        logger.info(f"Transformation complete: {len(staging_rows)} rows created")

        return staging_rows

