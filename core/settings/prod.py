from .dev import *
from dotenv import load_dotenv
load_dotenv(override=True)



DEBUG=False
SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = ['*.onrender.com']

