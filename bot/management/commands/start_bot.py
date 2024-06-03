from django.core.management.base import BaseCommand
import telebot

TOKEN = '7206021194:AAGgjLtgDvBfkN8f9FC3ja6ySKEVZKUklOY'
WEBHOOK_URL = 'http://localhost:8000/bot/webhook/'

bot = telebot.TeleBot(TOKEN)

class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **kwargs):
        bot.remove_webhook()
        bot.set_webhook(url=WEBHOOK_URL)
        self.stdout.write('Webhook set at {}'.format(WEBHOOK_URL))
