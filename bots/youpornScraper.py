import parsers.parser_youporn
import common.startBrowser, common.html_tag_parser
from BeautifulSoup import BeautifulSoup
import common.postCreator
import common.dataHandler
import sys
import os

class YouPornScraper():

    def __init__(self):
        homeDirectory = os.getenv("HOME")
        sys.path.append(r"" + homeDirectory + "/ScraperBot" + "")

    def scrape_videos(self, br, htmlscraper, parser, wpPost, dataHandler, videoUrls, categoriesList):
        postList = wpPost.get_posts(1500)

        for i in range(len(videoUrls)):
            try:
                print "---------------------" + str(i) + " from " + str(len(videoUrls)) + "------------------------"
                soup = BeautifulSoup(br.scrap_website(videoUrls[i]))
                title = htmlscraper.convert_hypen_into_space(parser.split_url(videoUrls[i]))
                print "Video scraping started ..."
                print "title: " + htmlscraper.uppercase_first_letter_from_string(title)
                if (wpPost.is_this_item_on_the_list(title, postList)):
                    print "Content already posted"
                else:

                    title_as_categories = htmlscraper.convert_title_to_categories(str(title))
                    print "categories: " + str(title_as_categories)
                    url = videoUrls[i]
                    print "url: " + url
                    print "url objects: " + htmlscraper.convert_hypen_into_space(parser.split_url(url))
                    strIntoCategories = htmlscraper.convert_hypen_into_space(parser.split_url(url))
                    thumbnail = parser.get_thumbnail(soup)
                    print "thumbnail: " + thumbnail
                    paraVideo = parser.parse_video_id(videoUrls[i])
                    iframe = parser.create_video_iframe(paraVideo[0], paraVideo[1])
                    print "iframe: " + iframe
                    video_duration = parser.get_duration(soup)
                    print "video duration: " + video_duration
                    print "Wordpress post creator starting ..."
                    wpPost.createPost(title, thumbnail, iframe, video_duration, str(title_as_categories), str(title_as_categories))
                    print "Scraped video [OK]"
            except:
                pass

    def scrape_from_category(self, br, htmlscraper, parser, wpPost, categoryUrls, scraper):
        print "scraping videos from categories"
        for i in range(len(categoryUrls)):
            soup = BeautifulSoup(br.scrap_website(categoryUrls[i]))
            totalUrlsVideos = parser.getUrlsFromVideos(soup, htmlscraper)
            totalUrlsVideos = list(set(totalUrlsVideos))
            scraper.scrape_videos(br, htmlscraper, parser, wpPost, totalUrlsVideos)

    """Function not used. Legacy code """
    def scraping_homepage(self, br, htmlscraper, parser, wpPost, output):
        print "scraping homepage"
        reu = parser.get_video_box()
        for i in range(len(reu)):
            try:
                print "---------------------" + str(i) + " from " + str(len(reu)) + "------------------------"

                title = htmlscraper.convert_hypen_into_space(parser.split_url(htmlscraper.parse_href(reu[i])))
                print " Scraping started ..."
                print "title: " + htmlscraper.uppercase_first_letter_from_string(title)

                title_as_categories = htmlscraper.convert_title_to_categories(str(title))
                print "title convert to categories: " + str(title_as_categories)
                url = "http://www.youporn.com" + htmlscraper.parse_href(reu[i])
                print "url: " + url
                print "url objects: " + htmlscraper.convert_hypen_into_space(parser.split_url(url))
                strIntoCategories = htmlscraper.convert_hypen_into_space(parser.split_url(url))
                print htmlscraper.convert_string_into_categories(strIntoCategories)
                thumbnail = parser.get_thumbnail(reu[i])
                print "thumbnail: " + thumbnail
                paraVideo = parser.parse_video_id(url)
                iframe = parser.create_video_iframe(paraVideo[0], paraVideo[1])
                print "iframe: " + iframe
                soup = BeautifulSoup(br.scrap_website(url))
                cat_and_tags = parser.get_tags_and_categories(soup)
                cats = BeautifulSoup(str(cat_and_tags[0]))
                cat = parser.extract_categories(htmlscraper.parse_all_href(cats))
                print "categories: " + cat
                tags = BeautifulSoup(str(cat_and_tags[1]))
                tag = parser.extract_categories(htmlscraper.parse_all_href(tags))
                print "tags: " + tag
                video_duration = parser.get_duration(soup)
                print "video duration: " + video_duration
                print "Wordpress post creator starting ..."
                print "Scraped video [OK]"
                wpPost.createPost(title, thumbnail, iframe, video_duration, cat, tag)
            except:
                pass


    def main(self):
        print "Youporn scraper bot is starting ..."
        br = common.startBrowser.BotBrowser()
        homepage = br.scrap_website('http://www.youporn.com/')
        htmlscraper = common.html_tag_parser.HtmlTagParser(homepage)
        parser = parsers.parser_youporn.YoupornParser(homepage)
        wpPost = common.postCreator.PostCreator()
        dataHandler = common.dataHandler.DataHandler()
        categoriesList = dataHandler.read_categories()
        print categoriesList
        print len(categoriesList)
        categories = dataHandler.prepare_categories_for_post("blonde fuck in the ass", categoriesList)
        print categories
        #scraper = YouPornScraper()
        #soup = BeautifulSoup(homepage)
        #totalUrlsVideos = parser.getUrlsFromVideos(soup, htmlscraper)
        #totalUrlsCategories = parser.getUrlsFromCategories(soup, htmlscraper)
        #totalUrlsVideos = list(set(totalUrlsVideos))
        #totalUrlsCategories = list(set(totalUrlsCategories))
        #scraper.scrape_videos(br, htmlscraper, parser, wpPost, dataHandler, totalUrlsVideos)
        #scraper.scrape_from_category(br, htmlscraper, parser, wpPost, totalUrlsCategories, scraper)
        print "Youporn scraper bot is finishing ..."

YouPornScraper().main()