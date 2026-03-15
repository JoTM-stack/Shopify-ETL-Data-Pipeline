import logging

from extract.shopify_client import ShopifyClient
from transform.product_transformer import ProductTransformer
from load.mysql_loader import MySQLLoader


logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def run():

    try:

        logger.info("\n")
        logger.info("Starting Shopify ETL pipeline")

        # 1 Extract
        logger.info("Step 1: Fetching Shopify product data")

        client = ShopifyClient()
        products = client.get_products()

        logger.info(f"{len(products)} products retrieved")

        # 2 Setup database
        logger.info("Step 2: Preparing database")

        loader = MySQLLoader()
        loader.setup()

        # 3 RAW LOAD
        logger.info("Step 3: Storing raw API response")

        for product in products:
            loader.insert_raw(product)

        # 4 Transform
        logger.info("Step 4: Transforming product data")

        transformer = ProductTransformer()
        staging_rows = transformer.transform(products, client)

        logger.info(f"{len(staging_rows)} staging rows generated")

        # 5 STAGING LOAD
        logger.info("Step 5: Loading staging table")

        loader.insert_staging(staging_rows)

        # 6 FINAL LOAD
        logger.info("Step 6: Loading final products table")

        loader.insert(staging_rows)

        logger.info("Pipeline completed successfully")

    except Exception as e:

        logger.error(f"Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    run()