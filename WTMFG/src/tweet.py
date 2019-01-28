from src.text import Text
from dateutil.parser import *


class InvalidTweetLine(BaseException):
    def __init__(self):
        pass


class Tweet(Text):
    def __init__(self, tweet_line):
        self.hash_tags = set()
        tweet_line_words = tweet_line.split("\t")
        if len(tweet_line_words) != 7:
            raise InvalidTweetLine()
        self.tweet_id = tweet_line_words[0]
        self.published_time = parse(tweet_line_words[1], tzinfos={"EST": "UTC-4"})
        self.author = tweet_line_words[2]
        self.set_text(tweet_line_words[3])
        super().__init__(self.text)
        self.referred_news_url = tweet_line_words[4]
        self.referred_news_id = tweet_line_words[5]
        self.referred_news_rank = -1
        self.timestamp = tweet_line_words[6]
        self.named_entities = set()

    def __str__(self):
        return super(Tweet, self).__str__()

    def set_text(self, text):
        words = text.split(' ')
        refined_words = []
        for word in words:
            if '#' in word:
                word = word.replace('#', '')
                self.hash_tags.add(word)
            refined_words.append(word)
        self.text = ' '.join(refined_words)
