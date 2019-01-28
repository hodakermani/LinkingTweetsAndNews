import codecs
from os import environ, path

from src.corpora import Corpora
from src.news_collection import NewsCollection
from src.tweet_collection import TweetCollection


def configure():
    hashtags_tweets_k = 3
    if 'HASHTAGS_TWEETS_K' in environ:
        hashtags_tweets_k = int(environ['HASHTAGS_TWEETS_K'])
    NE_tweets_k = 3
    if 'NE_TWEETS_K' in environ:
        NE_tweets_k = int(environ['NE_TWEETS_K'])
    time_tweets_k = 3
    if 'TIME_TWEETS_K' in environ:
        time_tweets_k = int(environ['TIME_TWEETS_K'])
    time_news_k = 3
    if 'TIME_NEWS_K' in environ:
        time_news_k = int(environ['TIME_NEWS_K'])
    network_news_k = 3
    if 'NETWORK_NEWS_K' in environ:
        network_news_k = int(environ['NETWORK_NEWS_K'])
    num_of_iterations = 20
    if 'NUM_OF_ITERATIONS' in environ:
        num_of_iterations = int(environ['NUM_OF_ITERATIONS'])
    news_new_feature = 3
    if 'NEW_FEATURE_K' in environ:
        news_new_feature = int(environ['NEW_FEATURE_K'])
    tweet_author_k = 2
    if 'TWEET_AUTHOR_K' in environ:
        tweet_author_k = int(environ['TWEET_AUTHOR_K'])
    Corpora.tweet_author_k = tweet_author_k
    TweetCollection.hashtags_tweets_k = hashtags_tweets_k
    TweetCollection.NE_tweets_k = NE_tweets_k
    Corpora.time_tweets_k = time_tweets_k
    Corpora.time_news_k = time_news_k
    NewsCollection.network_k = network_news_k
    Corpora.num_of_iterations = num_of_iterations
    Corpora.news_new_feature = news_new_feature


def print_configuration():
    print('<<<<<<<<<<<<<<<<<<<< Configuration >>>>>>>>>>>>>>>>>>>>')
    print('Hashtags_tweets_k:', TweetCollection.hashtags_tweets_k)
    print('NE_tweets_k: ', TweetCollection.NE_tweets_k)
    print('Time_tweets_k', Corpora.time_tweets_k)
    print('Time_news_k', Corpora.time_news_k)
    print('Network_news_k', NewsCollection.network_k)
    print('Num_of_iterations', Corpora.num_of_iterations)
    print('Texts_file_path', environ['TEXTS_FILE_PATH'])
    print('Tweets_file_path:', environ['TWEETS_FILE_PATH'])
    print('News_file_path:', environ['NEWS_FILE_PATH'])
    print('Num_of_processors', environ['NUM_OF_PROCESSORS'])
    print('NEW_FEATURE_K', Corpora.news_new_feature)
    print('Tweet_author_k', Corpora.tweet_author_k)
    print('<<<<<<<<<<<<<<<<<<<< Configuration >>>>>>>>>>>>>>>>>>>>')


def save_lists(corpora):
    total_num_of_neighbours = 0
    file = codecs.open(path.join('./tmp', 'tl.txt'), mode='w+', encoding='utf-8')
    corpora.tweet_collection.tweets.sort(key=lambda t: t.index)
    for tweet in corpora.tweet_collection.tweets:
        total_num_of_neighbours += len(tweet.neighbours)
        file.write('%d %d %d %s: ' % (
            tweet.index, corpora.news_collection.id_index_map[tweet.referred_news_id],
            tweet.referred_news_rank, tweet.published_time))
        # for t in tweet.hash_tags:
        #     file.write('%s, ' % t)
        for t in tweet.named_entities:
            file.write('%s, ' % t)
        file.write(' -- ')
        for i in tweet.neighbours:
            file.write('(%d:%s), ' % (i, corpora.tweet_collection.tweets[i].published_time))
        file.write('\n')
    file.close()
    file = codecs.open(path.join('./tmp', 'nl.txt'), mode='w+', encoding='utf-8')
    for news in corpora.news_collection.news_list:
        total_num_of_neighbours += len(news.neighbours)
        file.write('%d' % (news.index))
        for i in news.neighbours:
            file.write('%d, ' % i)
        file.write('\n')
    file.close()
    print('Total Num Of Neighbours: %d' % (total_num_of_neighbours / 2))
