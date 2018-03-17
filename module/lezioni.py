# -*- coding: utf-8 -*-

from sets import Set

import json, datetime
import requests

import calendar
import locale
import time

locale.setlocale(locale.LC_ALL, 'it_IT.utf8')

def lezioni_output(item):
    daylist = list(calendar.day_name)

    output = "*Nome:* " + item["Nome"]
    output += "\n*Aula:* " + item["Aula"]

    for day in daylist:
        if(day.replace('ì','i') in item and item[day.replace('ì','i')] != ""):
            output += "\n*" + day.title() + ":* " + item[day.replace('ì','i')]

    output += "\n*Anno:* " + item["Anno"] + "\n"

    return output

def lezioni_condition(items, condition, *arg):
    output = Set()
    for item in items:
        if(arg):
            if(arg[0] in item[condition].lower()):
                output.add(lezioni_output(item))
        else:
            if(condition.replace('ì','i') in item and item[condition.replace('ì','i')] != ""):
                output.add(lezioni_output(item))

    return output

def lezioni_condition_mult(items, days, years):
    output = Set()
    for item in items:
        for day in days:
            if( [year for year in years if year in item["Anno"].lower()] ):
                if(day.replace('ì','i') in item and item[day.replace('ì','i')] != ""):
                    output.add(lezioni_output(item))
    return output

def lezioni_cmd(bot, update, args, path):

    output_str = "Poffarbacco, qualcosa non va. Segnalalo ai dev /contributors \n"

    if(args):
        output = Set()
        r = json.load(open(path))

        items = r["materie"]
        daylist = list(calendar.day_name)
        daylist = [x.lower().encode('utf-8').replace('ì', 'i') for x in daylist]
        #Clear arguments - Trasform all to lower case utf-8 (ì) - Remove word 'anno' and len<2
        args = [x.lower().encode('utf-8') for x in args if len(x) > 2]

        try:

            if 'anno' in args: args.remove('anno')

            #Study case
            if(len(args) == 1):

                if(args[0] in daylist):
                    output = lezioni_condition(items, args[0])

                elif(args[0] == "oggi"):
                    output = lezioni_condition(items, time.strftime("%A"))

                elif(args[0] == "domani"):
                    tomorrow_date = datetime.datetime.today() + datetime.timedelta(1)
                    tomorrow_name = datetime.datetime.strftime(tomorrow_date,'%A')
                    output = lezioni_condition(items, tomorrow_name)

                elif(args[0] in ("primo", "secondo", "terzo")):
                    output = lezioni_condition(items, "anno", args[0])

                elif([item["Nome"].lower().find(args[0]) for item in items]):
                    output = lezioni_condition(items, "Nome", args[0])

                if not len(output):
                    output_str = "Nessun risultato trovato :(\n"
            elif(len(args) > 1):

                #Create an array of days and years if in arguments
                days = list(set(args).intersection(daylist))
                years = list(set(args).intersection(("primo", "secondo", "terzo")))

                if(days and years):
                    output = lezioni_condition_mult(items, days, years)

                elif("oggi" in args and years):
                    day = [time.strftime("%A")]
                    output = lezioni_condition_mult(items, day, years)

                elif("domani" in args and years):
                    tomorrow_date = datetime.datetime.today() + datetime.timedelta(1)
                    tomorrow_name = datetime.datetime.strftime(tomorrow_date,'%A')
                    day = [tomorrow_name]
                    output = lezioni_condition_mult(items, day, years)

                else:
                    for arg in args:
                        output = output.union(lezioni_condition(items, "Nome", arg))

                if not len(output):
                    output_str = "Nessun risultato trovato :(\n"

        except Exception as e:
            #debugging
            bot.sendMessage(chat_id=update.message.chat_id, text=str(e))

    else:
        output_str = "Inserisci almeno uno dei seguenti parametri: giorno, materia, anno."

    return output_str
