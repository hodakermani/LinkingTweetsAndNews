from dateutil.parser import *
from src.text import Text


class InvalidNewsLine(BaseException):
    def __init__(self):
        pass


class News(Text):
    def __init__(self, news_line):
        news_line_words = news_line.split("\t")
        if len(news_line_words) != 6:
            raise InvalidNewsLine()
        self.news_id = news_line_words[0]
        self.published_time = parse(news_line_words[1], tzinfos={"EST": "UTC-5", "EDT": "UTC-4"})
        self.title = news_line_words[2]
        self.url = news_line_words[3]
        self.summary = news_line_words[4]
        self.timestamp = news_line_words[5]
        super().__init__(self.title + ' ' + self.summary)

    def get_network_name(self):
        network_name = self.url.replace("http://", "")
        network_name = network_name.replace("www.", "")
        return network_name.split("/")[0]
