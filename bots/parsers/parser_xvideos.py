import re

from BeautifulSoup import BeautifulSoup

class XvideosParser():
    "A xvideos simple parser class."

    def __init__(self, output):
        soup = BeautifulSoup(output)
        self.soup = soup

    def get_keywords(self):
        return self.soup.findAll(attrs={"name":"KEYWORDS"})

    def get_title_on_homepage(self, output):
        for tag in output.findAll('span'):
            return tag

    def get_title_on_videopage(self):
        results = []
        for tag in self.soup.findAll('strong'):
            results.append(tag)
        return results[4]

    def split_title(self, output):
        auxOutput = output.lstrip('<span class="red" style="text-decoration:underline;">').split('<')
        return auxOutput[0]

    def get_video_td(self):
        results = []
        for tag in self.soup.findAll("td", { "width":"183" }):
            results.append(tag)
        return results

    def get_tags(self, output):
        global auxResults
        auxResults = []
        for tag in output.findAll("table", { "width":"930" }):
            auxResults.append(tag)
        return auxResults

    def get_video_td_from_categories(self, output):
        results = []
        for tag in output.findAll("td", { "width":"183" }):
            results.append(tag)
        return results

    def get_thumbnail(self, output):
        global auxThumbnail, thumbnailStruct
        auxThumbnail = []
        thumbnailStruct = []
        for tag in output.findAll('img'):
            auxThumbnail = tag
        thumbnailStruct = str(auxThumbnail).split('"')
        if thumbnailStruct != None:
            return thumbnailStruct[1]
        else:
            return None

    def get_video_duration(self, output):
        for tag in output.findAll('b'):
            return tag

    def get_video_duration_on_categories(self, output):
        for tag in output.findAll('strong'):
            return tag

    def split_video_duration(self, output):
        auxOutput = output.lstrip('<b>(').split(')')
        return auxOutput[0]

    def split_video_duration_on_categories(self, output):
        auxOutput = output.lstrip('<strong>(').split(')')
        return auxOutput[0]

    def parse_videos(self):
        results = []
        match = re.compile('(xvideos\.com\/video)([-a-zA-Z0-9_]+)')
        for link in self.soup.findAll('a'):
            try:
                href = link['href']
                if re.search(match, href):
                    results.append(href)
            except KeyError:
                pass
        return results

    def parse_tags(self, output):
        global resultsTags
        resultsTags = []
        for m in output:
            if re.match('(\/tags\/)', m):
                auxTag = str(m).split('/')
                resultsTags.append(auxTag[2])
        return resultsTags


    def parse_categories(self, output):
        global resultsForCategories
        resultsForCategories = []
        match = re.compile('(xvideos\.com\/c\/)([-a-zA-Z0-9_]+)')
        for link in self.soup.findAll('a'):
            try:
                href = link['href']
                if re.search(match, href):
                    resultsForCategories.append(href)
            except KeyError:
                pass
        return resultsForCategories

    def parse_video_id(self, output):
        global auxOutput
        match = re.compile('(?<=xvideos\.com\/video)([-a-zA-Z0-9_]+)')
        for link in output.findAll('a'):
            try:
                href = link['href']
                if re.search(match, href):
                    auxOutput = href.lstrip('http://www.xvideos.com/video').split('/')
            except KeyError:
                pass
        return auxOutput

    def create_video_iframe(self, output):
        return "<iframe src=\"http://flashservice.xvideos.com/embedframe/" + output + "\" frameborder=0 width=510 height=400 scrolling=no></iframe>"

