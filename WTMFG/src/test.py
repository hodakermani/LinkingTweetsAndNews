from src.corpora import Corpora
from os import environ, path
import logging

from src.test_runner import configure, print_configuration, save_lists

configure()
print_configuration()

logging.getLogger().setLevel(logging.ERROR)

corpora = Corpora(environ['TEXTS_FILE_PATH'])

corpora.load_tweet_collection(environ['TWEETS_FILE_PATH'])

# corpora.load_news_collection_for_tweets(environ['ALL_NEWS_FILE_PATH'])
corpora.load_news_collection(environ['NEWS_FILE_PATH'])
corpora.link_all_tweets_by_hashtag()
corpora.link_all_news_by_network()
corpora.link_all_tweets_by_named_entities()

corpora.link_all_tweets_by_author()

corpora.generate_latent_model()
corpora.load_latent_model()
corpora.link_all_tweets_by_temporal_relation()
# corpora.link_all_news_by_temporal_relation()

corpora.link_all_news_by_new_feature()

corpora.generate_latent_model()
corpora.load_latent_model()
corpora.find_relevant_news_index()

print_configuration()
print('Mean ATOP: ', corpora.calculate_mean_atop() * 100)

Corpora.set_top_k = 1
print('Mean TOP1: ', corpora.calculate_mean_top10() * 100)

Corpora.set_top_k = 2
print('Mean TOP2: ', corpora.calculate_mean_top10() * 100)

Corpora.set_top_k = 3
print('Mean TOP3: ', corpora.calculate_mean_top10() * 100)

Corpora.set_top_k = 5
print('Mean TOP5: ', corpora.calculate_mean_top10() * 100)

Corpora.set_top_k = 10
print('Mean TOP10: ', corpora.calculate_mean_top10() * 100)

Corpora.set_top_k = 20
print('Mean TOP20: ', corpora.calculate_mean_top10() * 100)

Corpora.set_top_k = 30
print('Mean TOP30: ', corpora.calculate_mean_top10() * 100)

Corpora.set_top_k = 40
print('Mean TOP40: ', corpora.calculate_mean_top10() * 100)

print('Mean RR: ', corpora.calculate_mean_reciprocal_rank() * 100)
