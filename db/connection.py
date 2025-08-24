import os
from dotenv import load_dotenv

load_dotenv()

db_url = f"postgresql+psycopg://{os.getenv('USER_DB')}:{os.getenv('PASSWORD_DB')}@localhost:{os.getenv('DB_PORT')}/{os.getenv('NAME_DB')}"

