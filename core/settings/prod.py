from .dev import *
from dotenv import load_dotenv


SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = ['*.onrender.com']

