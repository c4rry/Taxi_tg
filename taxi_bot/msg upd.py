import os
import sys
import time
import re
from datetime import datetime, date, time
from gett import gett, read_f

from telethon import TelegramClient, events, utils

session = os.environ.get('TG_SESSION', 'printer2')
api_id = 00000  # API ID (получается при регистрации приложения на my.telegram.org)
api_hash = "AAaaaaaaaaaaaa"  # API Hash (оттуда же)
proxy = None  # https://github.com/Anorov/PySocks

client = TelegramClient(session, api_id, api_hash, proxy=proxy).start()



@client.on(events.NewMessage(pattern=None))
async def handler(event):
    sender = await event.get_sender()
    name = utils.get_display_name(sender)
    user_id = utils.get_peer(sender).user_id
    director_id = 0000000 # указать id директора в телеграм

    start = str(datetime.now().strftime("%Y-%m-%d") + ' 00:00:01')
    finish = str(datetime.now().strftime("%Y-%m-%d %H:%M:") + '00')
    msg = str(event.text).strip()

    if (user_id == director_id) & (len(re.findall('Гетт', msg))):
        if re.findall('сегодня', msg):  # Гетт сегодня
            if re.findall('до', msg):  # Гетт сегодня с 10 до 11
                start_hour = str(msg).split(' ')[3]
                end_hour = str(int(str(msg).split(' ')[5]) - 1)
                if int(end_hour) < 0:
                    end_hour = '0'

                if len(start_hour) == 1:
                    start_hour = '0' + start_hour
                if len(end_hour) == 1:
                    end_hour = '0' + end_hour

                start = str(datetime.now().strftime("%Y-%m-%d ") + str(start_hour) + ':00:01')
                finish = str(datetime.now().strftime("%Y-%m-%d %H:%M:") + str(end_hour) + ':59:59')
            else:
                start = str(datetime.now().strftime("%Y-%m-%d") + ' 00:00:01')
                finish = str(datetime.now().strftime("%Y-%m-%d %H:%M:") + '59')
        else:
            if not (re.findall('до', msg)):  # Гетт 25.04-25.04
                start = '2019-{}-{} 00:00:01'.format(msg[8:10], msg[5:7])
                if (str(msg[11:16]) == str(datetime.now().strftime("%d.%m"))):
                    finish = str(datetime.now().strftime("%Y-%m-%d %H:%M:") + '59')
                else:
                    finish = '2019-{}-{} 23:59:59'.format(msg[14:16], msg[11:13])
            else:  # Гетт 25.04-25.04 с 10 до 12
                start_hour = str(msg).split(' ')[3]
                end_hour = str(int(str(msg).split(' ')[5]) - 1)
                if int(end_hour) < 0:
                    end_hour = '0'

                if len(start_hour) == 1:
                    start_hour = '0' + start_hour
                if len(end_hour) == 1:
                    end_hour = '0' + end_hour

                start = str('2019-{}-{} '.format(msg[8:10], msg[5:7]) + str(start_hour) + ':00:01')
                finish = str('2019-{}-{} '.format(msg[14:16], msg[11:13]) + str(end_hour) + ':59:59')


        gett(start, finish)
        des = 'Данные за период с ' + start + ' по ' + finish + '\n'

        try:
            await client.send_file(weta_id, 'summary.txt', caption=des)
            await client.send_file(weta_id, 'rides.csv')
        except:
            await client.send_message(weta_id, 'Ты неверно указал запрос или исчерпан лимит на отчеты. '
                                               'Попробуй что-то из этого:\n '
                                               'Гетт сегодня\n'
                                               'Гетт сегодня с 10 до 11\n'
                                               'Гетт 01.04-26.04\n'
                                               'Гетт 01.04-25.04 с 23 до 15\n'
                                               'Обрати внимание, что час начала и час окончания счета указывается для '
                                               'соответсвующей даты')


with client:
    client.run_until_disconnected()
