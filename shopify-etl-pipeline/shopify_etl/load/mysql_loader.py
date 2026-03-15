import mysql.connector
import logging
import json

from config.settings import DB_HOST, DB_USER, DB_PORT, DB_NAME, DB_PASSWORD

logger = logging.getLogger(__name__)


class MySQLLoader:

    def __init__(self):

        self.conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            port=DB_PORT,
            password=DB_PASSWORD
        )

        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT @@hostname, @@port")
        logger.info("Server and Port @ ",self.cursor.fetchall())


    def setup(self):

        try:

            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            logger.info(f"Database {DB_NAME} ready")

            self.cursor.execute(f"USE {DB_NAME}")

            # RAW TABLE
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS raw_products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                source VARCHAR(50),
                payload JSON,
                ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # STAGING TABLE
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS staging_products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_id VARCHAR(30),
                title VARCHAR(255),
                sku VARCHAR(100),
                price DECIMAL(10,2),
                inventory_quantity INT,
                missing_sku BOOLEAN,
                missing_price BOOLEAN,
                staged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # FINAL TABLE
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_id VARCHAR(30),
                title VARCHAR(255),
                sku VARCHAR(100),
                price DECIMAL(10,2),
                inventory_quantity INT
            )
            """)

            logger.info("All tables ready")

        except mysql.connector.Error as e:

            logger.error(f"Database setup failed: {e}")
            raise


    def insert_raw(self, payload):

        query = """
        INSERT INTO raw_products (source, payload)
        VALUES (%s, %s)
        """

        self.cursor.execute(query, ("shopify_api", json.dumps(payload)))
        self.conn.commit()

        logger.info("Raw data inserted")


    def insert(self, rows):

        query = """
        INSERT INTO products
        (product_id, title, sku, price, inventory_quantity)
        VALUES (%s, %s, %s, %s, %s)
        """

        try:

            data = [
                (
                    row["product_id"],
                    row["title"],
                    row["sku"],
                    row["price"],
                    row["inventory_quantity"]
                )
                for row in rows
            ]

            self.cursor.executemany(query, data)
            self.conn.commit()

            logger.info(f"{len(rows)} rows inserted")

        except mysql.connector.Error as e:

            logger.error(f"Insert failed: {e}")
            self.conn.rollback()
            raise

    def insert_staging(self, rows):

        query = """
        INSERT INTO staging_products
        (product_id, title, sku, price, inventory_quantity, missing_sku, missing_price)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """

        try:

            data = [
                (
                    row["product_id"],
                    row["title"],
                    row["sku"],
                    row["price"],
                    row["inventory_quantity"],
                    row["missing_sku"],
                    row["missing_price"]
                )
                for row in rows
            ]

            self.cursor.executemany(query, data)
            self.conn.commit()

            logger.info(f"{len(rows)} rows inserted into staging")

        except mysql.connector.Error as e:

            logger.error(f"Staging insert failed: {e}")
            self.conn.rollback()
            raise


    def close(self):

        self.cursor.close()
        self.conn.close()

        logger.info("Database connection closed")
