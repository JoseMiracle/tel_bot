import requests, os
from django.conf import settings
from dotenv import load_dotenv

load_dotenv(override=True)

API_TOKEN = os.getenv('TELEGRAM_BOT_API_KEY')

if settings.DEBUG == True:
    WEBHOOK_URL = 'http://localhost:8000/bot/webhook/'

else:
    WEBHOOK_URL = os.getenv('PROD_URL_FOR_WEBHOOK')+'bot/webhook/'

def set_webhook():
    url = f"https://api.telegram.org/bot{API_TOKEN}/setWebhook"
    data = {'url': WEBHOOK_URL}
    response = requests.post(url, data=data)
    print(response.json())

if __name__ == "__main__":
    set_webhook()
