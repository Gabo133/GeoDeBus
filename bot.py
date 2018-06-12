from telegram.ext import Updater, CommandHandler
import MySQLdb

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="john",         # your username
                     passwd="megajonhy",  # your password
                     db="jonhydb")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
cur.execute("SELECT * FROM YOUR_TABLE_NAME")

# print all the first cell of all the rows
for row in cur.fetchall():
    print row[0]

db.close()

def hello(bot, update):
    update.message.reply_text(
        "Hello {} {}".format(update.message.from_user.first_name, update.message.from_user.last_name))

def get_all_conductor(bot, update):
	lista =[]
	conductores = Conductor.objects.all()
	for i in conductores:
		lista.append(i.nombre)
	for a in lista:
		update.message.reply_text(a)
 
updater = Updater('567147683:AAH06b2SV15KETB4hX1OJxePOGmBP21-vrE')
updater.dispatcher.add_handler(CommandHandler(["saludo","saludar","saludame","hola","holi","hello"], hello))
updater.dispatcher.add_handler(CommandHandler(["Muestrame todos los conductores","Todos los conductores","conductores"], get_all_conductor))

updater.start_polling()
updater.idle()