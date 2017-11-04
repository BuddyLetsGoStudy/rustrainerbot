# coding utf-8
import time
import logging


import telebot
from telebot.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)


import const
from database import Users, States
from config import token


# register the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('../logs/bot.log')
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
logger.addHandler(handler)


# main listener function
def listener(messages):
    # handle the `start` command
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        # if user is new, update the database
        if message.chat.id not in users:
            users.add(message.chat.id)

        bot.send_message(message.chat.id, "Greetings! Now you are registered as user.")

    @bot.message_handler(commands=['help'])
    def handle_help_request(message):
        # Write something useful here
        pass

    @bot.message_handler(commands=['play'])
    def handle_play_request(message):
        # Here you should send button murkup with the game logic.
        # But i'll just set user's states to the waiting.

        # send something to the new users which somehow got access
        # to the text messaging before running /start and return from the function
        # this part isn't important (and maybe already fixed by telegram) so you can just delete it.
        if message.chat.id not in users:
            bot.send_message(message.chat.id, "Firstly you need to run the /start command.")
            return

        # update state
        users[message.chat.id] = States.WAIT

    # the hardest part: FSM
    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        if message.chat.id not in users:
            bot.send_message(message.chat.id, "Firstly you need to run the /start command.")
            return

        # Firstly, you need to determine current user state.
        # Let's do it using chat.id and users table
        # user_state = <your code>

        # Ok, you got the state.
        # Now check it - and if state is IDLE - return
        # if user_state == State.IDLE:
        #     return

        # In the our case we have only 2 states: IDLE and WAIT
        # IDLE is already processed, so you can just skip
        # other checkups.

        your_logic_trigger = 'shibe doge'
        if message.text == your_logic_trigger:
            bot.send_message(message.chat.id, "You are won! 😎😎😎")

            # if session is end, set the user state again to the IDLE
            users[message.chat.id] = States.IDLE
        else:
            bot.send_message(message.chat.id, "Oh, sooo sad 😱. Maybe you'll get lucky next time.")


if __name__ == "__main__":
    # create bot
    bot = telebot.TeleBot(token)

    # create database
    users = Users()

    # set listener
    bot.set_update_listener(listener)

    # endless loop over polling
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error("An exception received while the polling: %s" % e)
            time.sleep(15)
