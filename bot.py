# -*- coding: utf-8 -*-

import telebot
import apiai, json
import config

bot = telebot.TeleBot(config.bot_token)

@bot.message_handler(commands=["start"])
def greetings(message):
    bot.send_message(message.chat.id, 'Привет, давай пообщаемся!')

@bot.message_handler(func = lambda message: True, content_types=['text'])
def text_message(message):
    request = apiai.ApiAI(config.dialog_flow_token).text_request() # Token API of Dialogflow
    request.lang = config.bot_lang # lang of request
    request.session_id = config.dialog_flow_session # ID of dialog session (for bot learning)
    request.query = message.text # Send request to AI with user's message
    response_json = json.loads(request.getresponse().read().decode('utf-8'))
    response = response_json['result']['fulfillment']['speech'] # Retrieve json and get the answer
    # If we take answer back, we will send it to the user, else we can't understand user
    if response:
        bot.send_message(message.chat.id, text=response)
    else:
        bot.send_message(message.chat.id, text='Прости, но я тебя не понимаю(')

if __name__ == '__main__':
    bot.polling(none_stop=True)
