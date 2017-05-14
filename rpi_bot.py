#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
from telebot import types
import time
import os

TOKEN = ""  # SUSTITUIR POR TU TOKEN
ID = 000000 # SUSTITUIR PO TU ID NO PONER COMILLAS

userStep = {}
knownUsers = []

commands = {
        'ayuda': 'Comandos disponibles',
        'start': 'Arranca el bot',
	    'temp': 'Temperatura rpi',
	    'hd': 'Espacio en disco',
	    'cpu': 'Carga de la CPU',
	    'mem': 'Uso memoria RAM',
	    'osversion': 'Version s.o.',
	    'uptime': 'Uptime rpi',
	    'repoup': 'Actualiza repositorios',
	    'sysup': 'Actualiza sistema',
	    'distup': 'Actualiza distro',
	    'reboot': 'Reinicia rpi',
	    'shutdown': 'Apaga rpi',
}


# USER STEP
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0

# LISTENER
def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print("[" + str(m.chat.id) + "] " + str(m.chat.first_name) + ": " + m.text)

bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)


# START
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid == ID :
      userStep[cid] = 0
      time.sleep(1)
      bot.send_message(cid, "Pulsa /ayuda para ver los comandos disponibles\n")
    else:
        bot.send_message(cid, " ¡¡NO ERES MI CREADOR!!")

# AYUDA
@bot.message_handler(commands=['ayuda'])
def command_ayuda(m):
    cid = m.chat.id
    if cid == ID :

      #help_text = "Comandos disponibles: \n"
      #for key in commands:
      #  help_text += "/" + key + ": "
      #  help_text += commands[key] + "\n"
      bot.send_message(cid, "/ayuda muestra los comandos disponibles\n"
          "/start Arranca el bot\n"
          "/temp Temperatura rpi\n"
	      "/hd Espacio en disco\n"
          "/cpu Carga de la CPU\n"
          "/mem Uso memoria RAM\n"
          "/exec Ejecuta un comando\n"
	      "/osversion Version s.o.\n"
	      "/uptime Uptime rpi\n"
	      "/repoup Actualiza repositorios\n"
	      "/sysup Actualiza sistema\n"
	      "/distup Actualiza distro\n"
	      "/reboot Reinicia sistema\n"
	      "/shutdown Apaga rpi\n")
    else:
        bot.send_message(cid, " ¡¡PERMISO DENEGADO!!")

# COMANDOS
@bot.message_handler(commands=['uptime'])
def command_uptime(m):
    cid = m.chat.id
    if cid == ID :
        uptime = os.popen('uptime -p')
        bot.send_message(cid, uptime)
    else:
        bot.send_message(cid, " ¡¡PERMISO DENEGADO!!")

@bot.message_handler(commands=['temp'])
def command_temp(m):
    cid = m.chat.id
    if cid == ID :
       bot.send_message(cid, "[+] TEMPERATURAS")
       # cpu temp
       tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
       cpu_temp = tempFile.read()
       tempFile.close()
       cpu_temp = round(float(cpu_temp)/1000)
       bot.send_message(cid, "  [i]   CPU: %s" % cpu_temp)
       # gpu temp
       gpu_temp = os.popen('/opt/vc/bin/vcgencmd measure_temp').read().split("=")[1][:-3]
       bot.send_message(cid, "  [i]   GPU: %s" % gpu_temp)
    else:
        bot.send_message(cid, " ¡¡PERMISO DENEGADO!!")

@bot.message_handler(commands=['hd'])
def command_hd(m):
    cid = m.chat.id
    if cid == ID :
        bot.send_message(cid, "[+] DISCO DURO")
        bot.send_message(cid, "  [i]   Total: %s" % diskSpace()[0])
        bot.send_message(cid, "  [i]   Usado: %s" % diskSpace()[1])
        bot.send_message(cid, "  [i]   Disponible: %s" % diskSpace()[2])
    else:
        bot.send_message(cid, " ¡¡PERMISO DENEGADO!!")
        print(color.RED + " ¡¡PERMISO DENEGADO!! " + color.ENDC)

@bot.message_handler(commands=['mem'])
def command_mem(m):
    cid = m.chat.id
    if cid == ID :
        bot.send_message(cid, "[+] MEMORIA RAM")
        bot.send_message(cid, "  [i]   Total: %s" % ramInfo()[0])
        bot.send_message(cid, "  [i]   Usado: %s" % ramInfo()[1])
        bot.send_message(cid, "  [i]   Disponible: %s" % ramInfo()[2])
    else:
        bot.send_message(cid, " ¡¡PERMISO DENEGADO!!")
        print(color.RED + " ¡¡PERMISO DENEGADO!! " + color.ENDC)

@bot.message_handler(commands=['cpu'])
def command_cpu(m):
    cid = m.chat.id
    if cid == ID :
        bot.send_message(cid, "[+] CPU")
        cpu = os.popen('mpstat | grep -A 5 "%idle" | tail -n 1 | awk -F " " \'{print 100 - $ 12}\'a').read()
        bot.send_message(cid, "  [i]   Usado: %s" % cpu)
    else:
       bot.send_message(cid, " ¡¡PERMISO DENEGADO!!")

@bot.message_handler(commands=['shutdown'])
def command_shutdown(m):
    cid = m.chat.id
    if cid == ID :
	shutdown = os.system('sudo poweroff')
	bot.send_message(cid, shutdown)
    else:
        bot.send_message(cid, " ¡¡PERMISO DENEGADO!!")
        print(color.RED + " ¡¡PERMISO DENEGADO!! " + color.ENDC)

@bot.message_handler(commands=['reboot'])
def command_reboot(m):
    cid = m.chat.id
    if cid == ID :
	reboot = os.system('sudo reboot')
	bot.send_message(cid, reboot)
    else:
        bot.send_message(cid, " ¡¡PERMISO DENEGADO!!")
        print(color.RED + " ¡¡PERMISO DENEGADO!! " + color.ENDC)


@bot.message_handler(commands=['repoup'])
def command_repoup(m):
    cid = m.chat.id
    if cid == ID :
	repoup = os.system('sudo apt-get update')
	bot.send_message(cid, repoup)
    else:
        bot.send_message(cid, " ¡¡PERMISO DENEGADO!!")
        print(color.RED + " ¡¡PERMISO DENEGADO!! " + color.ENDC)

@bot.message_handler(commands=['sysup'])
def command_sysup(m):
    cid = m.chat.id
    if cid == ID :
	sysup = os.system('sudo apt-get upgrade')
	bot.send_message(cid, sysup)
    else:
        bot.send_message(cid, " ¡¡PERMISO DENEGADO!!")
        print(color.RED + " ¡¡PERMISO DENEGADO!! " + color.ENDC)

@bot.message_handler(commands=['distup'])
def command_distup(m):
    cid = m.chat.id
    if cid == ID :
	distup = os.system('sudo apt-get dist-upgrade')
	bot.send_message(cid, distup)
    else:
        bot.send_message(cid, " ¡¡PERMISO DENEGADO!!")
        print(color.RED + " ¡¡PERMISO DENEGADO!! " + color.ENDC)

@bot.message_handler(commands=['osversion'])
def command_osversion(m):
    cid = m.chat.id
    if cid == ID :
    #osversion = os.proper('lsb_release -a')
        tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
	tempFile = open( "/etc/os-release" )
        osversion = tempFile.read()
        tempFile.close()
        bot.send_message(cid, osversion)
    else:
        bot.send_message(cid, " ¡¡PERMISO DENEGADO!!")
        print(color.RED + " ¡¡PERMISO DENEGADO!! " + color.ENDC)



# EXEC COMANDO
@bot.message_handler(commands=['exec'])
def command_exec(m):
    cid = m.chat.id
    if cid == ID :
        bot.send_message(cid, "Ejecutando: " + m.text[len("/exec"):])
        bot.send_chat_action(cid, 'typing')
        time.sleep(4)
        f = os.popen(m.text[len("/exec"):])
        result = f.read()
        bot.send_message(cid, "Resultado: " + result)
    else:
        bot.send_message(cid, " ¡¡PERMISO DENEGADO!!")
        print(color.RED + " ¡¡PERMISO DENEGADO!! " + color.ENDC)


# INFO HD
def diskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i += 1
        line = p.readline()
        if i == 2:
            return(line.split()[1:5])


# INFO RAM
def ramInfo():
    p = os.popen('free -o -h')
    i = 0
    while 1:
        i += 1
        line = p.readline()
        if i == 2:
            return(line.split()[1:4])


# FILTRAR MENSAJES
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_text(m):
    cid = m.chat.id
    if (m.text.lower() in ['hola', 'hi', 'buenas', 'buenos dias']):
        bot.send_message(cid, 'Muy buenas, ' + str(m.from_user.first_name) + '. Me alegra verte de nuevo.')
    elif (m.text.lower() in ['adios', 'aios', 'adeu', 'ciao']):
        bot.send_message(cid, 'Hasta luego, ' + str(m.from_user.first_name) + '. Te echaré de menos.')


print 'Corriendo...'
bot.polling(none_stop=True)
