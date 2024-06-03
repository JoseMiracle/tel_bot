# myapp/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telebot.types import Update
from .bot import bot

import telebot


# TOKEN = '7206021194:AAGgjLtgDvBfkN8f9FC3ja6ySKEVZKUklOY'
# bot = telebot.TeleBot(TOKEN)

WEBHOOK_URL = 'https://dbcc-102-89-23-215.ngrok-free.app/bot/webhook/'

bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)


@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        json_str = request.body.decode('UTF-8')
        update = Update.de_json(json_str)
        bot.process_new_updates([update])
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'forbidden'}, status=403)
