from dotenv import load_dotenv
import os


load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get('DEBUG')
API_KEY = os.environ.get("API_KEY")
