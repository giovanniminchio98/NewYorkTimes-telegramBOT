# import os
# import json
import time
import requests
# import datetime
# import dateutil
# import pandas as pd
# from dateutil.relativedelta import relativedelta
import time

# api for use NYT APi
from pynytimes import NYTAPI

# for telegram bot
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# markup gen for telegram bot example
def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
                               InlineKeyboardButton("No", callback_data="cb_no"))
    return markup

if __name__=='__main__':

    # bot init Telegram
    TELEGRAM_TOKEN = 'YOUR TELEGRAM BOT API'
    bot = telebot.TeleBot(TELEGRAM_TOKEN)

    # NYT api settings
    nyt = NYTAPI("YOUR NYT API", parse_dates=True)

    # # top stories from the NYT
    # top_stories = nyt.top_stories()
    # a=1

    # # Get all the top stories from a specific category
    # top_science_stories = nyt.top_stories(section = "science")
    # b=1

    # get most viewd articles of last day
    most_viewed = nyt.most_viewed()
    c=1

    # # most shared article
    # most_shared = nyt.most_shared()
    # d=1

    # to get the latest articvle published by NYT
    sections = ['science','automobiles', 'business', 'climate',  'fashion','food','health', 'home page', 'new york','real estate', 'smarter living', 'sports','style','technology','the learning network','the upshot','today’s paper', 'travel','world','your money']

    latest_per_sections = []

    flag_first = True

    while True:

        for i in range(len(sections)):
            try: 
                if flag_first:
                    latest = nyt.latest_articles(
                        source = "all",
                        section = sections[i]
                    )
                    date = latest[0]['published_date']
                    date_unix_timestamp =  int((time.mktime(date.timetuple())))
                    latest_per_sections.append(date_unix_timestamp)

                    if len(latest_per_sections) == len(sections):
                        flag_first = False

                else:
                    latest = nyt.latest_articles(
                        source = "all",
                        section = sections[i]
                    )

                    # check if article new, then keep it and notice about it
                    # date can be "updated_date" or "created_date" or "published_date""
                    date = latest[0]['published_date']
                    date_unix_timestamp =  int((time.mktime(date.timetuple())))

                    if date_unix_timestamp > latest_per_sections[i]:
                        article = latest[0]
                        message_title = article['title']
                        message_abstract = article['abstract']
                        flag_image = True
                        try:
                            message_image = requests.get(article['multimedia'][2]['url']).content
                        except:
                            flag_image = False

                        message_source = article['source']
                        latest_per_sections[i] = date_unix_timestamp

                        'to send message with just text and link to have preview on telegram'
                        'preview should be unlimited using telegram....testiong this theory'

                        if article['url'].split('/')[3] == 'live':
                            a=1
                        else:
                            try:
                                #section
                                mini_title = '<b>('+sections[i].upper()+') </b>' + ' \n\n'

                                # title
                                message_title = '<b>' + message_title + '</b>' 
                                title_finale = "<a href='"+str(article['url'])+"'>"+ message_title +"</a>"+ '\n\n'

                                # abstract
                                message_abstract = '<b>Abstract: </b>'+ message_abstract +  ' \n'

                                final_text = mini_title + title_finale + message_abstract + text #+ preview

                                article_link = " <a href='"+str(article['url'])+"'> - </a> "

                                section_link = "<a href='"+str("https://www.nytimes.com/section/"+sections[i].lower())+"'><b>"+ sections[i].upper() +"</b></a>"

                                title_finale = 'New article'+article_link+section_link + "\n\n <a href='"+str(article['url'])+"'><b>Read More</b></a>"+ '\n\n'

                                bot.send_message('CHANNEL NAME OR CHAT ID', title_finale, parse_mode='HTML', disable_notification=True)
                            except:
                                text='*ERROR SENDING NEW ARTICLE !! *'
                                bot.send_message('CHANNEL NAME OR CHAT ID', text, parse_mode='Markdown')
                                continue

                if i%2 ==0 and i != 0:
                    # at most 10 resuqest per minute AND 4000 PER DAY
                    # since the categories are 50 we do a break every 10
                    # each 5 minutes we check for new articles in all the categories
                    time.sleep(60)
            except Exception as  e:
                print('Eccezzione --> ', e)
                bot.send_message('CHANNEL NAME OR CHAT ID', "<b>Errorebot...</b>controllare server !!! \n\n" + str(e), parse_mode='HTML')
                if e.args[0] == 'Error 400: Invalid input':
                    # quanti-=1
                    a=1
                    sections.remove(sections[i])
