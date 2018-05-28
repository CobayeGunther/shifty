# -*- coding: utf-8 -*-
from tokens import *
import telepot
import sqlite3
import datetime
import time


db = sqlite3.connect('datas',
                    check_same_thread=False,
                    detect_types=sqlite3.PARSE_DECLTYPES)
try:
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE work(ddmm integer PRIMARY KEY, begin timestamp, end timestamp, beginSec timestamp, endSec timestamp)''')
    db.commit()
except sqlite3.OperationalError:
    print("database already exist")


def beatifulize(shift):
    #i don't like the datetime representation,
    #so i made my own showing weekday, shifts and hours of work
    week   = ['Monday',
              'Tuesday',
              'Wednesday',
              'Thursday',
              'Friday',
              'Saturday',
              'Sunday']
    ddmm = shift[0]
    begin = shift[1]
    end = shift[2]
    if shift[3] is not None:
        beginSec = shift[3]
        endSec = shift[4]

    msg =  str(week[begin.weekday()]) + ' ' \
             + str(begin.day) + '/' + str(begin.month) + ' : \n    ' + \
             str(begin.hour) + ':' + str(begin.minute) + '-' + \
             str(end.hour) + ':' + str(end.minute)
    if shift[3] is not None:
        beginSec = shift[3]
        endSec = shift[4]
        msg = msg + "\n    " + str(beginSec.hour) + \
            ':' + str(beginSec.minute) + '-' + \
                 str(endSec.hour) + ':' + str(endSec.minute)
    if shift[3] is not None:
        hours = (end - begin) + (endSec - beginSec)
    else:  # hours of the shift
        hours = end - begin
    msg = msg + "\n    " + str(hours.seconds / 3600) + " hours"
    return msg


def addShift(msg):
    parts = msg[1:].split(" ")
    print(("command = ", msg[:1], " parts = ", parts, " len ", len(parts)))
    #we split day and month from msg
    day, month = parts[0].split("/")
    ddmm = day + month
    date = datetime.date(2018, int(month), int(day))
    #we split begin, end hours and minutes
    #into integer that we arrange in datetime.time
    beginHour, beginMinute = parts[1].split("h")
    if beginMinute != '':
        beginTime = datetime.time(int(beginHour), int(beginMinute), 0)
    else:
        beginTime = datetime.time(int(beginHour), 0, 0)
    endHour, endMinute = parts[2].split("h")
    if endMinute != '':
        endTime = datetime.time(int(endHour), int(endMinute), 0)
    else:
        endTime = datetime.time(int(endHour), 0, 0)
    if len(parts) == 5:
        #we split begin, end hours and minutes
         #into integer that we arrange in datetime.time
        beginHour, beginMinute = parts[3].split("h")
        if beginMinute != '':
            beginTimeSec = datetime.time(int(beginHour), int(beginMinute), 0)
        else:
            beginTimeSec = datetime.time(int(beginHour), 0, 0)
        endHour, endMinute = parts[4].split("h")
        if endMinute != '':
            endTimeSec = datetime.time(int(endHour), int(endMinute), 0)
        else:
            endTimeSec = datetime.time(int(endHour), 0, 0)
        beginSec = datetime.datetime.combine(date, beginTimeSec)
        if endTimeSec < beginTimeSec:
            endSec = datetime.datetime.combine(date + datetime.timedelta(days=1), endTimeSec)
        else:
            endSec = datetime.datetime.combine(date, endTimeSec)
    else:
        beginSec = None
        endSec = None
    #then we combine day month hours and minutes
     #in datetime, and if end h < begin h, we add a day
    begin = datetime.datetime.combine(date, beginTime)
    if endTime < beginTime:
        end = datetime.datetime.combine(date + datetime.timedelta(days=1), endTime)
    else:
        end = datetime.datetime.combine(date, endTime)

    if len(parts)==5:
        print(("second shift : ", beginSec, " - ", endSec))
        hours = (end - begin) + (endSec - beginSec)
    else: # hours of the shift
        hours = end - begin


    try:
        with db:
            cursor = db.cursor()
            cursor.execute('''INSERT INTO work(ddmm, begin, end, beginSec, endSec)
                  VALUES(?,?,?,?,?)''', (ddmm, begin, end, beginSec, endSec))
            db.commit()
            if len(parts) == 5:
                hours = (end - begin) + (endSec - beginSec)
            else:  # hours of the shift
                hours = end - begin
            return str(hours.seconds / 3600) + " hours"
    except sqlite3.IntegrityError:
        print('Record already exists')


def showShift(msg):
    parts = msg[1:].split(" ")
    print(("command = ", msg[:1], " parts = ", parts, " len ", len(parts)))
    #we split day and month from msg
    day, month = parts[0].split("/")
    ddmm = day + month
    #ddmm = int(ddmm)
    with db:
        cursor = db.cursor()
        cursor.execute('''SELECT ddmm, begin, end, beginSec, endSec FROM work WHERE ddmm = ?''', (ddmm,))
        shift = cursor.fetchone()
        return beatifulize(shift)


def getWeek(dstr):
    return dstr.isocalendar()[1]


def showWeek(msg):
    nothing, week = msg.split()
    print(("using ", week))
    with db:
        sumHours = datetime.timedelta()
        cursor = db.cursor()
        cursor.execute('''
                        SELECT ddmm, begin, end, beginSec, endSec FROM work
                        ''')
        shift = cursor.fetchall()
        for day in shift:
            begin = day[1]
            print(begin)
            if begin.isocalendar()[1] == int(week):
                msg = msg + '\n ' + beatifulize(day)
                if day[3] is not None:
                    hours = (day[2] - day[1]) + (day[4] - day[3])
                else:  # hours of the shift
                    hours = day[2] - day[1]
                sumHours = sumHours + hours


        days, seconds = sumHours.days, sumHours.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        return msg + '\n\n' + str(hours) + ':' + str(minutes) + " hours"



def remShift(msg):
    parts = msg[1:].split(" ")
    print(("command = ", msg[:1], " parts = ", parts, " len ", len(parts)))
    #we split day and month from msg
    day, month = parts[0].split("/")
    ddmm = day + month
    #ddmm = int(ddmm)
    try:
        with db:
            cursor = db.cursor()
            cursor.execute('''DELETE FROM work WHERE ddmm = ?''', (ddmm,))
            db.commit()
            return str(ddmm) + " removed"
    except:
        print('Record already exists')


class YourBot(telepot.Bot):
    def __init__(self, *args, **kwargs):
        super(YourBot, self).__init__(*args, **kwargs)
        self._answerer = telepot.helper.Answerer(self)
        self._message_with_inline_keyboard = None

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        # Do your stuff according to `content_type` ...
        print(("Your chat_id:" + str(chat_id) + "chat_type : "
               + str(chat_type)))  # this will tell you your chat_id
        if chat_id in adminchatid:  # Store adminchatid variable in tokens.py
            #Text messages
            if content_type == 'text':
                command = msg['text'][:1]
                if command == '+':
                    bot.sendMessage(chat_id, addShift(msg['text']))
                elif command == '?':
                    bot.sendMessage(chat_id, showShift(msg['text']))
                elif command == '-':
                    bot.sendMessage(chat_id, remShift(msg['text']))
                elif 'week' in msg['text'] or 'Week' in msg['text']:
                    bot.sendMessage(chat_id, showWeek(msg['text']))

TOKEN = telegrambot
bot = YourBot(TOKEN)
bot.message_loop()


def main():
    test = "+11/06 11h00 12h00"
    test2 = "+11/06 11h00 12h00 19h00 22h00"
    test3 = "?11/06"
    print("enter you work shift")
    #msg = input()
    msg = test3
    print(msg)

    # Keep the program running.
    while 1:
        time.sleep(10)  # 10 seconds
        #tr += 10