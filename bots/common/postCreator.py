import sys
import os
import urllib2
from wordpress_xmlrpc.base import Client
import xmlrpclib
import time
from wordpress_xmlrpc.wordpress import WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost, GetRecentPosts
import datetime
from Crypto.Random.random import randrange
import dataHandler
import random
from random import randint
import calendar

class PostCreator():

    def __init__(self):
        homeDirectory = os.getenv("HOME")
        sys.path.append(r"" + homeDirectory + "/ScraperBot" + "")
        #self.wp_site = "http://localhost/wordpress/xmlrpc.php"
        self.wp_site = "http://www.hottestporn4u.com/xmlrpc.php"
        self.login = "pornmaster"
        self.password = "pornmasterpiece"
        self.dataHandler = dataHandler.DataHandler()
        self.categoriesList = self.dataHandler.read_categories()

    def connect_the_client(self):
        wp = Client(self.wp_site, self.login, self.password)
        return wp

    def get_url_content(self, url):
        try:
            content = urllib2.urlopen(url)
            return content.read()
        except:
            print 'error! NOOOOOO!!!'

    def enter_WP_user(self):
        user = raw_input ("WP user >> ")
        return user

    def enter_WP_password(self):
        password = raw_input ("WP password >> ")
        return password

    def uploadFileToWp(self, thumbnail):
        print "Client connected ..."
        # set to the path to your file
        file_url = thumbnail
        extension = file_url.split(".")
        leng = extension.__len__()
        extension = extension[leng - 1]
        if (extension == 'jpg'):
            xfileType = 'image/jpeg'
        elif(extension == 'png'):
            xfileType = 'image/png'
        elif(extension == 'bmp'):
            xfileType = 'image/bmp'

        file = self.get_url_content(file_url)
        file = xmlrpclib.Binary(file)
        server = xmlrpclib.Server(self.wp_site)
        filename = str(time.strftime('%H:%M:%S'))
        mediarray = {'name':filename + '.' + extension,
                     'type':xfileType,
                     'bits':file,
                     'overwrite':'false'}
        xarr = ['1', self.login, self.password, mediarray]
        result = server.wp.uploadFile(xarr)
        print result

    def createPost(self, title, thumbnail, iframe, videoduration, snippets_Duration, categories, url):
        #user_from_keyboard = enter_WP_user()
        #password_from_keyboard = enter_WP_password()
        print "WP creating post ..."

        wp = self.connect_the_client()

        post0 = WordPressPost()
        post0.title = title
        print "WP title: " + post0.title
        #post0.description = iframe + "Duration <img src=" + thumbnail + " alt=" + title + "><br>" + videoduration
        average = str(round(self.prepare_rating_for_post(), 2))
        print "Average: " + average + "/10"
        number_of_votes = str(self.prepare_number_of_votes())
        print "Votes: " + number_of_votes
        print "url " + url
        print "iframe " + iframe
        print "title " + title
        print "videoduration " + videoduration
        print "thumbnail " + thumbnail
        print "average " + average
        print "number_of_votes " + number_of_votes
        print "categories " + str(categories)
        print "tags " + str(self.dataHandler.prepare_tags_for_post(title))
        post0.description = '<div class="hreview-aggregate"><div class="item vcard"><div itemscope itemtype="http://schema.org/VideoObject"><h2 class="fn"><meta itemprop="embedURL" content="' + url + '" />' + iframe + '<p><span itemprop="name">' + title + '</span></h2><meta itemprop="duration" content="' + snippets_Duration + '" /><h3>(' + videoduration + ')</h3><meta itemprop="thumbnailUrl" content="' + thumbnail + '" /><p><span itemprop="description">This video is called ' + title + '</span></div></div><span class="rating"><span class="average">' + average + '</span> out of <span class="best"> 10 </span>based on <span class="votes">' + number_of_votes + ' </span>votes</span><p><img src="' + thumbnail + '" alt="' + title + '"><br></div>'
        print "WP description: " + post0.description
        #Categories and tags correct
        #post0.categories = ['latest updates', 'new', 'amateur', 'american', 'anal', 'blonde', 'sex', 'fuck', 'girls', 'porn', 'pornstar']
        #post0.tags = ['latest updates', 'new', 'amateur', 'american', 'anal', 'blonde', 'sex', 'fuck', 'girls', 'porn', 'pornstar']
        post0.categories = self.dataHandler.prepare_categories_for_post(categories, self.categoriesList)
        post0.tags = self.dataHandler.prepare_tags_for_post(title)
        dateFormat = self.prepare_post_date()
        post0.date_created = str(dateFormat)
        #post0.date_created = '20120507T12:11:59'
        print "WP Date: " + post0.date_created
        print "before wp.call "
        wp.call(NewPost(post0, True))

    def prepare_rating_for_post(self):
        var = random.uniform(7.5, 10)
        return var

    def prepare_number_of_votes(self):
        var = random.randrange(0, 10100, 2)
        return var

    def prepare_post_date(self):
        print "prepare post date"
        now = datetime.datetime.now()
        lastDay = self.get_last_day_of_the_month(now)
        if now.day == lastDay.day:
            day = randint(1, lastDay.day)
            month = now.month + 1
        elif (calendar.isleap(now.year) and now.day == 29):
            day = randint(1, lastDay.day)
            month = now.month + 1
        elif (not(calendar.isleap(now.year)) and now.day == 28):
            day = randint(1, lastDay.day)
            month = now.month + 1
        else:
            dayRange = now.day + 1
            day = randint(now.day, dayRange)
            month = now.month

        minute = randint(now.minute, 59)
        hour = randint(0, 23)

        if month < 10:
            month = "0" + str(month)
        else:
            month = str(month)

        if day < 10:
            day = "0" + str(day)
        else:
            day = str(day)

        if hour < 10:
            hour = "0" + str(hour)
        else:
            hour = str(hour)

        if minute < 10:
            minute = "0" + str(minute)
        else:
            minute = str(minute)

        if now.second < 10:
            second = "0" + str(now.second)
        else:
            second = str(now.second)

        date = str(now.year) + "" + month + "" + day + "T" + hour + ":" + minute + ":" + second
        print str(date)
        return str(date)

    def get_posts(self, number_of_posts):
        wp = self.connect_the_client()
        post0 = WordPressPost()
        post0 = wp.call(GetRecentPosts(number_of_posts))
        return post0

    def get_last_day_of_the_month(self, date):
        if date.month == 12:
            return date.replace(day=31)
        return date.replace(month=date.month + 1, day=1) - datetime.timedelta(days=1)

