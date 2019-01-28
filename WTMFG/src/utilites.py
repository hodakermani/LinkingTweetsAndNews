from src.tweet import InvalidTweetLine, Tweet
from src.news import InvalidNewsLine, News

import time
import logging
import codecs

logger = logging.getLogger(__name__)


def get_all_texts_from_short_text(corpus):
    texts = []
    for short_text in corpus:
        texts.append(short_text.text)
    return texts


def load_news_from_file(news_file_name):
    file = codecs.open(news_file_name, mode='r', encoding='utf-8')
    content = file.readlines()
    content = [x.strip() for x in content]
    current_line_count = 0
    news = []
    for line in content:
        current_line_count += 1
        try:
            news.append(News(line))
        except InvalidNewsLine as error:
            logger.error('Invalid news at line %d' % current_line_count)
    return news


def load_tweets_from_file(tweets_file_name):
    file = codecs.open(tweets_file_name, mode='r', encoding='utf-8')
    content = file.readlines()
    content = [x.strip() for x in content]
    current_line_count = 0
    tweets = []
    for line in content:
        current_line_count += 1
        try:
            tweets.append(Tweet(line))
        except InvalidTweetLine as error:
            logger.error('Invalid tweet at line %d' % current_line_count)
    return tweets


def load_news_for_tweets(tweets, all_news):
    referred_news_ids = set()
    for tweet in tweets:
        referred_news_ids.add(tweet.referred_news_id)
    news_list = []
    file = codecs.open(all_news, mode='r', encoding='utf-8')
    content = file.readlines()
    content = [x.strip() for x in content]
    current_line_count = 0
    for line in content:
        current_line_count += 1
        news_id = line.split('\t')[0]
        if news_id in referred_news_ids:
            try:
                news_list.append(News(line))
            except InvalidNewsLine as error:
                logger.error('Invalid news at line %d' % current_line_count)
    return news_list


def time_absolute_diff(t1, t2):
    return max(t1 - t2, t2 - t1)


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def execution_time_keeper(method):
    def decorated(*args, **kwargs):
        start_time = time.perf_counter()
        output = method(*args, **kwargs)
        end_time = time.perf_counter()
        logger.info('%s Execution Time: %f' % (method.__name__, (end_time - start_time)))
        return output

    return decorated


def cached(method):
    cache = {}

    def decorated(*args):
        cache_key = tuple([*args][1:])
        if cache_key not in cache:
            cache[cache_key] = method(*args)
        return cache[cache_key]

    return decorated
