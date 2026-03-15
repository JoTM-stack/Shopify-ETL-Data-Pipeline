from dotenv import load_dotenv
import os

load_dotenv()

SHOP = os.getenv("SHOP")
TOKEN = os.getenv("TOKEN")


DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PORT = 3306
DB_PASSWORD = "root123"
DB_NAME = "shopifystore"

if not SHOP or not TOKEN:
    raise ValueError("SHOP or TOKEN not set in .env file")
