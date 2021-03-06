from BeautifulSoup import BeautifulSoup
import re

class YoupornParser():
    "A youporn simple parser class."

    def __init__(self, output):
        soup = BeautifulSoup(output)
        self.soup = soup

    def get_video_box(self, soup):
        results = []
        for tag in soup.findAll("li", { "class":"videoBox" }):
            results.append(tag)
        return results

    def get_title(self, soup):
        results = []
        for tag in soup.findAll("h1"):
            results.append(tag)
        results.pop(0) #remove the tag <h1 class="title">Videos Being Watched Now</h1>
        return results

    def split_title(self, output):
        auxOutput = output.split('>')
        auxOutput = auxOutput[2].split('<')
        return auxOutput[0]

    def get_thumbnail(self, output):
        global auxThumbnail, thumbnailStruct
        auxThumbnail = []
        thumbnailStruct = []
        for tag in output.findAll('img'):
            auxThumbnail = tag
        thumbnailStruct = str(auxThumbnail).split('"')
        return thumbnailStruct[1]

    def get_tags_and_categories(self, output):
        global auxResults
        for tag in output.findAll("ul", { "class":"listCat" }):
            auxResults.append(tag)
        return auxResults

    def extract_categories(self, output):
        final_categories = []
        for i in output:
            aux = i
            if len(aux) > 2:
                final_categories.append(aux[len(aux) - 2])
        return final_categories

    def split_url(self, output):
        aux = output.split("/")
        return aux[len(aux) - 2]

    def parse_video_id(self, output):
        global auxOutput
        auxOutput = output.lstrip('http://www.youporn.com/watch').split('/')
        return auxOutput

    def get_duration(self, output):
        i = 0
        for ul in output.findAll('ul', attrs={'class': 'spaced'}):
            liSoup = BeautifulSoup(str(ul))
            for li in liSoup.findAll('li'):
                i = i + 1
                if i == 2:
                    line = str(li)
                    lin = line.split('>')
                    duration = lin[3].split('<')
        return str(duration[0])

    def prepare_duration_for_snippets(self, duration):
        #format T30M00S
        min = duration.split('min')
        minute = str(min[0]).strip()
        sec = min[1].split('sec')
        second = str(sec[0]).strip()
        newDuration = "T" + minute + "M" + second + "S"
        return newDuration

    def getUrlsFromVideos(self, soup):
        results = []
        match = re.compile('(?<=\/watch/)([a-zA-Z0-9_-])+')
        for link in soup.findAll('a'):
            try:
                href = link['href']
                if re.search(match, href):
                    final_result = "http://www.youporn.com" + href
                    results.append(final_result)
            except KeyError:
                pass
        return results

    def getUrlsFromCategories(self, soup):
        results = []
        match = re.compile('(?<=\/category/)([a-zA-Z0-9_-])+')
        for link in soup.findAll('a'):
            try:
                href = link['href']
                if re.search(match, href):
                    final_result = "http://www.youporn.com" + href
                    results.append(final_result)
            except KeyError:
                pass
        return results

    def create_video_iframe(self, in1, in2):
        return "<iframe src=\"http://www.youporn.com/embed/" + in1 + "/" + in2 + "/\" frameborder=\'0\' height=\'485\' width=\'615\' scrolling=\'no\' name=\'yp_embed_video\'></iframe>"

    def list_has_duplicate_items(self, L):
        for item in L:
            if L.count(item) > 1:
                return True
        return False

    def get_duplicate_items(self, L):
        new = set()
        for item in L:
            if L.count(item) > 1:
                new.add(item)
        return list(new)
