# general import needed
import time
import requests
import time

# api for use NYT APi
from pynytimes import NYTAPI

# for telegram bot
# telebotAPI are the best one i tested so far !!
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

if __name__=='__main__':

    # init telegram bot
    TELEGRAM_TOKEN = 'YOUR TOKEN HERE'
    bot = telebot.TeleBot(TELEGRAM_TOKEN)

    # NYT api settings
    nyt = NYTAPI("YOUR NEW YORK TIMES APIs HERE", parse_dates=True)

    'top stories from the NYT'
    # top_stories = nyt.top_stories()
    # a=1

    'Get all the top stories from a specific category'
    # top_science_stories = nyt.top_stories(section = "science")
    # b=1

    'get most viewd articles of last day'
    # most_viewed = nyt.most_viewed()

    'most shared article'
    # most_shared = nyt.most_shared()

    # to get the latest articles published by NYT by category
    sections = ['science','automobiles', 'business', 'climate',  'fashion','food','health', 'home page', 'new york','real estate', 'smarter living', 'sports','style','technology','the learning network','the upshot','today’s paper', 'travel','world','your money']

    # save the last artcile time per each session, 
    # if the new latest article is newer than we send it to the telegram bot (for now)
    latest_per_sections = []

    # when the bot is started it just get all latest articles per category 
    # and keep their unix timestamp
    # (then when new articles come out it send them...)
    flag_first = True

    # loop cycle (not best choice, still ALPHA version...)
    while True:

        # for the session choosen (by me ahaha)
        for i in range(len(sections)):
            try: # in case of exception/s...
                #first scan
                if flag_first:
                    latest = nyt.latest_articles(
                        source = "all",
                        section = sections[i]
                    ) # this function return the latest 20 articles for the category
                    # we just check the last one, but actually may happen that more article are new
                    # is not rare to see more than onespawn at the same time

                    # we base analysis on published date, possible also to check creation_date or updateed_date
                    date = latest[0]['published_date']
                    # convert datetime to timestamp
                    date_unix_timestamp =  int((time.mktime(date.timetuple())))
                    latest_per_sections.append(date_unix_timestamp)

                    # to know when we have scanned all categories at least once
                    if len(latest_per_sections) == len(sections):
                        flag_first = False

                # else we have to check if the last article is new or not
                # new means "we haven't seen it yet"
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
                        # new article for the category!!
                        # print(sections[i], ' --> new article !!')
                        article = latest[0]

                        ## for debug
                        # print('\t Title: ', article['title'])
                        # print('\t Abstract: ', article['abstract'])
                        # print('\t\t source --> ', article['source'])

                        # send message to telegram bot for testing
                        # this is the message body (not used now)
                        message_title = '*'+article['title']+'*'
                        message_abstract = article['abstract']
                        message_image = requests.get(article['multimedia'][3]['url']).content
                        message_source = article['source']
                        # bot.send_message(203287688, message_title, parse_mode= 'Markdown')

                        latest_per_sections[i] = date_unix_timestamp

                        

                        'to send message with image of article and text in caption'
                        'actually useless for this bot since telegram preview handle everything for us...'
                        # message_text = message_title + ' \n\n ' + message_abstract
                        # try:
                        #     message_image = requests.get(article['multimedia'][3]['url']).content
                        # except:
                        #     message_image = requests.get(article['thumbnail_standard']).content
                        # bot.send_photo(203287688,message_image, caption=message_text, parse_mode= 'Markdown')

                        'to send message with just text and link to have preview on telegram'
                        'preview should be unlimited using telegram....testiong this theory'
                        chat_id = 'YOUR CHAT ID AS INTEGER'
                        try:
                            article_url = 'section: *'+sections[i].upper()+'*' +'\n\n'+article['url']
                            bot.send_message(chat_id, article_url, parse_mode='Markdown')
                        except:
                            text='*ERROR SENDING NEW ARTICLE !! *'
                            bot.send_message(chat_id, text, parse_mode='Markdown')

                       

                        

                if (i+1)%10 == 0:
                    # at most 10 resuqest per minute
                    # since the categories are 20 we do a break every 10
                    # each 1 minutes we check for new articles in all the categories
                    time.sleep(60)
                    # actually the sleep has to be increased since is not enough (i reached daily limit with this conif...)
            
            # if exception thorwn print why
            except Exception as  e:

                print('Eccezzione --> ', e)
                if e.args[0] == 'Error 400: Invalid input':
                    # quanti-=1
                    a=1
                    sections.remove(sections[i])

            
    breakpoint() # never reached now dueto while loop