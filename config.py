import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("DB_HOST", "localhost")
PORT = int(os.getenv("DB_PORT", "3306"))
USER = os.getenv("DB_USER", "root")
PASSWORD = os.getenv("DB_PASSWORD")
DATABASE = os.getenv("DB_NAME", "hotel_management")

SECRET_KEY = os.getenv("SECRET_KEY")



# HOST = "localhost"
# PORT = 3306
# USER = "root"
# PASSWORD = "Chandra@333"
# DATABASE = "hotel_management"


