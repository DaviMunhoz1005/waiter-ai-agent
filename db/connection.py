import os
from dotenv import load_dotenv

load_dotenv()

db_url = (f"postgresql+psycopg://"
          f"{os.getenv('POSTGRES_USER')}:"
          f"{os.getenv('POSTGRES_PASSWORD')}@"
          f"localhost:"
          f"{os.getenv('DB_PORT')}/"
          f"{os.getenv('POSTGRES_DB')}"
          )
