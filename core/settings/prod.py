from .dev import *
from dotenv import load_dotenv

DEBUG=False
SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')

