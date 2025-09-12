import os
from dotenv import load_dotenv

load_dotenv()

class Configs:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    PORT: int = int(os.getenv("PORT", 8000))
    ENV: str = os.getenv("ENV", "development")

configs = Configs()
