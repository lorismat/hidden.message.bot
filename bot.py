import time
import random
import json
import telebot

#### server setup ####
import os
from flask import Flask, request
server = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
####
#Below is your bot token
TOKEN = "118XXXXXXX:AAEXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
bot = telebot.TeleBot(token=TOKEN)

print('loading...')
#### db setup ####

# Setup the dev & prod env of the DB
ENV = 'prod'

if ENV == 'dev':
    server.debug = True
    # local database
    server.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localuser@localhost/localdb'
else:
    server.debug = False
    # production database, given with the following command: heroku config --app name_of_app   
    server.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgresDBaddress'

server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create the DB object
db = SQLAlchemy(server)

# Select a model
class Messages(db.Model):
    # name of your table and columns, adding a key column
    __tablename__ = 'name_given_to_your_table'
    id = db.Column(db.Integer, primary_key=True)
    comments = db.Column(db.Text())
    #below are your columns to define, here only the "comments" column, fetching the messages
    def __init__(self, comments):
        self.comments = comments

    def __repr__(self):
        return '<Comment %r>' % self.comments
####

@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    bot.send_message(message.chat.id, 'Tell me more!')

@bot.message_handler(commands=['text'])
def send_random_message(message):
    #my_list generates a list from the table
    my_list = Messages.query.all()
    #txt_back fetch a random message in the list and parse it
    txt_back = my_list[random.randint(0,len(my_list)-1)]
    txt_back = str(txt_back)[10:][:-2]
    bot.send_message(message.chat.id, txt_back)

@bot.message_handler(commands=['addtext'])
def send_random_message(message):
    add_text = str(message.text).replace('/addtext ','')
    if (add_text != '/addtext') and (add_text != '/addtext@yourBotName'):
        data = Messages(add_text)
        db.session.add(data)
        db.session.commit()
        time.sleep(1)
        bot.send_message(message.chat.id, "added!")
    else:
        time.sleep(1)
        bot.send_message(message.chat.id, "Mmmh... You probably didn't add any text. Try again with /addtext Your Poetry and Text")

#### Heroku server setup, to be removed in sandbox ####
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    # prod, url being your Heroku app url
    bot.set_webhook(url='https://your_app_name.herokuapp.com/' + TOKEN)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
####

