import telebot, os, random
from django.conf import settings

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from utils.response import Response
from utils import question_bank
from dotenv import load_dotenv

load_dotenv(override=True)
BOT_TOKEN = os.getenv('TELEGRAM_BOT_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_response(message):
    """response to the start command"""

    username = message.from_user.username
    start_message = f"""
Hi @<b>{username}</b> 😊, I am TestMyKnowledgeBot.

Choose the area you want to test your knowledge below
"""
    
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Football ⚽️⚽️", callback_data=Response.FOOTBALL.value),
        InlineKeyboardButton("Science 🧪🧪", callback_data=Response.SCIENCE.value),

    )
    bot.send_message(message.chat.id, start_message, reply_markup=markup, parse_mode="HTML")



@bot.callback_query_handler(func=lambda call: call.data in [Response.FOOTBALL.value, Response.SCIENCE.value])
def handle_query(call):
    """Handles user's query"""
    
    chat_id = call.message.chat.id
    
    if call.data == Response.FOOTBALL.value:
        question = get_question(question_bank.football_questions_and_answers)
        formatted_question = f"<b>{question}</b>"
        
        markup = InlineKeyboardMarkup()
        options = question_bank.football_questions_and_answers[question]['options']
        markup.row_width = 1
        
        for option in options:

            question_and_answer = f"{question}|{option}"
            print(question_and_answer, len(question_and_answer))
            markup.add(
            InlineKeyboardButton(option, callback_data=question_and_answer)
        )
    
    if call.data == Response.SCIENCE.value:
        question = get_question(question_bank.science_questions_and_answers)
        formatted_question = f"<b>{question}</b>"
        print(formatted_question)

        
        markup = InlineKeyboardMarkup()
        options = question_bank.science_questions_and_answers[question]['options']
        markup.row_width = 1
        
        for option in options:
            question_and_answer = f"{question}|{option}" 
            print(len(question_and_answer), question_and_answer)
            markup.add(
            InlineKeyboardButton(option, callback_data=question_and_answer)
        )
    bot.send_message(call.message.chat.id, formatted_question, reply_markup=markup, parse_mode="HTML")

        
@bot.callback_query_handler(func=lambda call: '|' in call.data )
def handle_answer_to_question(call):
    """This handle user's answer to question"""

    chat_id = call.message.chat.id
    question_and_answer = call.data

    question = question_and_answer.split('|')[0]
    answer = question_and_answer.split('|')[1]
    
    
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    

    if question in question_bank.football_questions_and_answers :
        correct_answer_from_question_bank =  question_bank.football_questions_and_answers[question]['answer']
        if answer == correct_answer_from_question_bank:
            category = Response.FOOTBALL.value
            response_message = f"""
Your answer, <b>{answer}</b> is correct 🎉.
"""      

        if answer != correct_answer_from_question_bank:
            category = Response.FOOTBALL.value

            response_message = f"""
Your answer, <b>{answer}</b> is incorrect, the correct answer is <b>{correct_answer_from_question_bank}</b>.
"""     
    
    if question in question_bank.science_questions_and_answers :
        correct_answer_from_question_bank = question_bank.science_questions_and_answers[question]['answer']
        if answer == correct_answer_from_question_bank:
            category = Response.SCIENCE.value
            response_message = f"""
Your answer, <b>{answer}</b> is correct 🎉.
"""      

        if answer != correct_answer_from_question_bank:
            category = Response.SCIENCE.value

            response_message = f"""
Your answer, <b>{answer}</b> is incorrect, the correct answer is <b>{correct_answer_from_question_bank}</b>.
""" 
            
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.id, reply_markup=None)
    
    markup.add(
        InlineKeyboardButton("Ask More", callback_data=category),
        InlineKeyboardButton("End", callback_data="End question session"),
    )

    bot.send_message(chat_id, response_message, reply_markup=markup, parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: call.data in ["End question session"])
def handle_end_seesion(call):
    """Handle end seesion"""
    chat_id = call.message.chat.id    
    markup = InlineKeyboardMarkup()
    markup.row_width = 1

    markup.add(
        InlineKeyboardButton("Feedback", url="https://forms.gle/TCT7xzs7qjLCU2Dv9"),
        InlineKeyboardButton("Restart", callback_data="restart")
    )
    bot.send_message(chat_id, "I believe you have tested your knowledge! 😊", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ["restart"])
def handle_restart(call):
    """Handle restart of testknowledgebot"""
    chat_id = call.message.chat.id
    username = call.from_user.username
    markup = InlineKeyboardMarkup()
    markup.row_width = 1


    restart_message = f""" Let's Go @{username}  🚀🙌

Choose the area you want to test your knowledge below
"""

    markup.add(
        InlineKeyboardButton("Football ⚽️⚽️", callback_data=Response.FOOTBALL.value),
        InlineKeyboardButton("Science 🧪🧪", callback_data=Response.SCIENCE.value),
    )
    bot.send_message(chat_id, restart_message,reply_markup=markup, parse_mode="HTML")



def get_question(questions_and_answers):
    """Get question to ask user"""

    question = random.choices(list(questions_and_answers.keys()))
    return question[0]

