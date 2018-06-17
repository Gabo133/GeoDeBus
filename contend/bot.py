from telegram.ext import Updater, CommandHandler
import MySQLdb

def llamar_db(nombre):
	db = MySQLdb.connect(host="localhost",    # your host, usually localhost
	                     user="root",         # your username
	                     passwd="gabriel12",  # your password
	                     db="GEODB")        # name of the data base

	# you must create a Cursor object. It will let
	#  you execute all the queries you need
	cur = db.cursor()

	# Use all the SQL you like
	cur.execute("SELECT * FROM {}".format(nombre))

	# print all the first cell of all the rows
	lista =[]
	for row in cur.fetchall():
	    lista.append(row)

	db.close()
	return lista

def llamar_db_nombres(nombre):
	db = MySQLdb.connect(host="localhost",    # your host, usually localhost
	                     user="root",         # your username
	                     passwd="gabriel12",  # your password
	                     db="GEODB")        # name of the data base

	# you must create a Cursor object. It will let
	#  you execute all the queries you need
	cur = db.cursor()

	# Use all the SQL you like
	cur.execute("SELECT * FROM {}".format(nombre))

	# print all the first cell of all the rows
	lista =[]
	for row in cur.fetchall():
	    lista.append(str(row[3]))

	db.close()
	return lista
def hello(bot, update):
    update.message.reply_text(
        "Hello {} {}".format(update.message.from_user.first_name, update.message.from_user.last_name))

def get_all_conductor(bot, update):
	lista = llamar_db("contend_conductor")
	for a in lista:
		update.message.reply_text("Nombre:{} Rut:{}-{}".format(a[1],a[3],a[4]))
 
def get_conductor(bot, update):
	ru = int((update.message.text).replace("/",""))
	db = MySQLdb.connect(host="localhost",    # your host, usually localhost
	                     user="root",         # your username
	                     passwd="gabriel12",  # your password
	                     db="GEODB")        # name of the data base

	# you must create a Cursor object. It will let
	#  you execute all the queries you need
	cur = db.cursor()

	# Use all the SQL you like
	cur.execute("SELECT * FROM contend_conductor WHERE rut={}".format(ru))

	# print all the first cell of all the rows
	lista =[]
	for row in cur.fetchall():
	    lista.append(row)

	db.close()
	print(lista)
	for a in lista:
		update.message.reply_text("Nombre:{} Rut:{}-{} Direccion: {} telefono: {}".format(a[1],a[3],a[4],a[6],a[7]))
all_conductor = llamar_db_nombres("contend_conductor")

updater = Updater('567147683:AAH06b2SV15KETB4hX1OJxePOGmBP21-vrE')
updater.dispatcher.add_handler(CommandHandler(["saludo","saludar","saludame","hola","holi","hello"], hello))
updater.dispatcher.add_handler(CommandHandler(["Muestrame todos los conductores","Todos los conductores","conductores"], get_all_conductor))
updater.dispatcher.add_handler(CommandHandler(all_conductor, get_conductor))

updater.start_polling()
updater.idle()