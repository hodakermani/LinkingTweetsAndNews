from logging import Logger

from src.multi_process import Parallel
from src.utilites import time_absolute_diff

logger = Logger(name='TweetsFileReader', level='INFO')

parallel = Parallel()


class TweetCollection:
    hashtags_tweets_k = 3
    NE_tweets_k = 3

    def __init__(self):
        self.tweets = []
        self.words = set()
        self.hash_tags = set()

    def add_tweet(self, tweet):
        self.tweets.append(tweet)
        for hash_tag in tweet.hash_tags:
            self.hash_tags.add(hash_tag)

    # def reassign_hash_tags(self):
    #     self.tweets = self.__reassign_hash_tags(self.tweets)
    #
    # @parallel.parallelize_method
    # def __reassign_hash_tags(self, tweets):
    #     new_tweets = []
    #     for tweet in tweets:
    #         words = tweet.text.split(' ')
    #         for word in words:
    #             if word in self.hash_tags:
    #                 tweet.hash_tags.add(word)
    #         new_tweets.append(tweet)
    #     return new_tweets

    def assign_named_entities(self, named_entities):
        for tweet in self.tweets:
            words = tweet.text.split(' ')
            for word in words:
                if word in named_entities:
                    tweet.named_entities.add(word)

    def __get_topk_tweets_with_same_hashtag(self, reference_tweet, hashtag):
        result = []
        for tweet in self.tweets:
            if hashtag in tweet.hash_tags:
                result.append(tweet)
        result.sort(key=lambda t: time_absolute_diff(reference_tweet.published_time, t.published_time).total_seconds())
        return result[: TweetCollection.hashtags_tweets_k]

    def __get_topk_tweets_with_same_named_entity(self, reference_tweet, named_entity):
        result = []
        for tweet in self.tweets:
            if named_entity in tweet.named_entities:
                result.append(tweet)
        result.sort(key=lambda t: time_absolute_diff(reference_tweet.published_time, t.published_time).total_seconds())
        return result[: TweetCollection.NE_tweets_k]

    def link_tweets_by_hashtag(self):
        self.tweets = self.__link_tweets_by_hashtag(self.tweets)

    @parallel.parallelize_method
    def __link_tweets_by_hashtag(self, tweets):
        new_tweets = []
        for tweet in tweets:
            for hash_tag in tweet.hash_tags:
                tweet.add_neighbours(self.__get_topk_tweets_with_same_hashtag(tweet, hash_tag))
            new_tweets.append(tweet)
        return new_tweets

    def link_tweets_by_named_entities(self):
        self.tweets = self.__link_tweets_by_named_entities(self.tweets)

    @parallel.parallelize_method
    def __link_tweets_by_named_entities(self, tweets):
        new_tweets = []
        for tweet in tweets:
            for named_entity in tweet.named_entities:
                tweet.add_neighbours(self.__get_topk_tweets_with_same_named_entity(tweet, named_entity))
            new_tweets.append(tweet)
        return new_tweets
