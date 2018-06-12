from telegram.ext import Updater, CommandHandler
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from contend.models import Bus, Conductor, ConductorBus,Ruta
from django.shortcuts import redirect
from contend.forms import BusForm, SerialGpsForm, EditarBusForm, ConductorForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required

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