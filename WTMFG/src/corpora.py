import codecs
import logging
from src.latent_model import LatentModel
from src.multi_process import Parallel
from src.news_collection import NewsCollection
from src.text import Text
from src.text_collection import TextCollection
from src.tweet_collection import TweetCollection
from src.utilites import load_tweets_from_file, load_news_from_file, time_absolute_diff, execution_time_keeper, \
    load_news_for_tweets, intersection
import subprocess
from os import path, environ
from src.matrix import SparseAdjacencyMatrix

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tmp_dir = './tmp'

parallel = Parallel()


class Corpora:
    time_tweets_k = 3
    time_news_k = 3
    num_of_iterations = 3
    news_new_feature = 3
    tweet_author_k = 2
    set_top_k = 10

    def __init__(self, texts_file_path):
        self.__text_collection = TextCollection()
        self.news_collection = NewsCollection()
        self.tweet_collection = TweetCollection()
        self.__texts_file_path = texts_file_path
        self.latent_model = None

    @execution_time_keeper
    def load_tweet_collection(self, file_path):
        tweets = load_tweets_from_file(file_path)
        for tweet in tweets:
            self.tweet_collection.add_tweet(tweet)
        print('Tweets loaded from: %s' % file_path)
        print('Num of tweets %d' % len(self.tweet_collection.tweets))

    def link_all_tweets_by_hashtag(self):
        # self.tweet_collection.reassign_hash_tags()
        # print('Hashtags reassigned')
        self.tweet_collection.link_tweets_by_hashtag()
        print('Tweets linked by hashtags')

    @execution_time_keeper
    def load_news_collection(self, news_path):
        news_list = load_news_from_file(news_path)
        for news in news_list:
            self.news_collection.add_news(news)
        print('News loaded from: %s' % news_path)
        print('Num of news %d' % len(self.news_collection.news_list))

    @execution_time_keeper
    def load_news_collection_for_tweets(self, all_news_path):
        news_list = load_news_for_tweets(self.tweet_collection.tweets, all_news_path)
        for news in news_list:
            self.news_collection.add_news(news)
        print('News loaded from: %s' % all_news_path)
        print('Num of news %d' % len(self.news_collection.news_list))

    @execution_time_keeper
    def link_all_news_by_network(self):
        self.news_collection.link_by_network()
        print('News linked by network')

    @execution_time_keeper
    def link_all_tweets_by_named_entities(self):
        named_entities = self.news_collection.find_named_entities()
        self.tweet_collection.assign_named_entities(named_entities)
        print('Named entities assigned to tweets')
        self.tweet_collection.link_tweets_by_named_entities()
        print('Tweets linked by named entities')

    @execution_time_keeper
    def generate_latent_model(self):
        # construct tmp/texts.txt
        self.__join_with_other_texts_and_export()
        print('Texts file exported')
        subprocess.call('./scripts/bash/generate_tf_idf.sh')
        # give sparse matrix format to TF-IDF
        self.__save_matrices()
        print('Matrices saved')
        subprocess.call(['./scripts/bash/run_wtmf.sh', str(Corpora.num_of_iterations)])

    def load_latent_model(self):
        self.latent_model = LatentModel(path.join(tmp_dir, 'model.q'))
        print('Latent model loaded')
        num_of_tweets = len(self.tweet_collection.tweets)
        num_of_news = len(self.news_collection.news_list)
        num_of_texts = self.__text_collection.num_of_text - num_of_tweets - num_of_news
        self.num_of_texts = num_of_texts
        self.latent_model.calculate_cosine_matrix(num_of_texts, num_of_tweets, num_of_news)

    @execution_time_keeper
    def link_all_news_by_temporal_relation(self):
        self.news_collection.news_list = self.__link_all_news_by_temporal_relation(self.news_collection.news_list)
        print('News linked by temporal relation')

    @parallel.parallelize_method
    def __link_all_news_by_temporal_relation(self, news_list):
        new_news_list = []
        for news in news_list:
            similar_news = self.__get_topk_news_by_temporal_relation_for_news(news)
            news.add_neighbours(similar_news)
            new_news_list.append(news)
        return new_news_list

    @execution_time_keeper
    def link_all_tweets_by_temporal_relation(self):
        self.tweet_collection.tweets = self.__link_all_tweets_by_temporal_relation(self.tweet_collection.tweets)
        print('Tweets linked by temporal relation')

    @parallel.parallelize_method
    def __link_all_tweets_by_temporal_relation(self, tweets):
        new_tweets = []
        for tweet in tweets:
            similar_tweets = self.__get_topk_tweets_by_temporal_relation_for_tweet(tweet)
            tweet.add_neighbours(similar_tweets)
            new_tweets.append(tweet)
        return new_tweets

    @execution_time_keeper
    def calculate_mean_reciprocal_rank(self):
        reciprocal_rank_sum = 0
        reciprocal_rank_values = self.__calculate_reciprocal_rank_values(self.tweet_collection.tweets)
        for reciprocal_rank_value in reciprocal_rank_values:
            reciprocal_rank_sum += reciprocal_rank_value
        return reciprocal_rank_sum / len(self.tweet_collection.tweets)

    @parallel.parallelize_method
    def __calculate_reciprocal_rank_values(self, tweets):
        reciprocal_rank_values = []
        for tweet in tweets:
            if tweet.referred_news_rank == -1:
                reciprocal_rank_values.append(0)
            else:
                reciprocal_rank_values.append(1 / tweet.referred_news_rank)
        return reciprocal_rank_values

    @execution_time_keeper
    def calculate_mean_top10(self):
        top10_values = self.__calculate_top10_values(self.tweet_collection.tweets)
        top10_sum = 0
        for top10_value in top10_values:
            top10_sum += top10_value
        return top10_sum / len(self.tweet_collection.tweets)

    @parallel.parallelize_method
    def __calculate_top10_values(self, tweets):
        top10_values = []
        for tweet in tweets:
            if tweet.referred_news_rank <= Corpora.set_top_k and tweet.referred_news_rank != -1:
                top10_values.append(1)
            else:
                top10_values.append(0)
        return top10_values

    @execution_time_keeper
    def calculate_mean_atop(self):
        atop_sums = self.__calculate_atop_values(self.tweet_collection.tweets)
        atop_sum = 0
        for atop in atop_sums:
            atop_sum += atop
        return atop_sum / len(self.tweet_collection.tweets)

    @parallel.parallelize_method
    def __calculate_atop_values(self, tweets):
        atops = []
        N = len(self.news_collection.news_list)
        for tweet in tweets:
            if tweet.referred_news_id in self.news_collection.id_index_map:
                rank = tweet.referred_news_rank
                rank = N - rank
                atops.append((rank - 1) / (N - 1))
            else:
                atops.append(0)
                logger.info('News with id=%s not exists in corpora' % tweet.referred_news_id)
        return atops

    def __get_topk_ranked_news_to_tweet(self, tweet_index, k=None):
        news = self.news_collection.news_list.copy()
        for text in news:
            text.sim = self.latent_model.cosine_similarity(text.index, tweet_index)
        news.sort(key=lambda i: i.sim, reverse=True)
        if k is None:
            return news
        else:
            return news[:k]

    @execution_time_keeper
    def __save_matrices(self):
        self.__text_collection.load_text(path.join(tmp_dir, 'train.clean'),
                                         path.join(tmp_dir, 'vocab'), path.join(tmp_dir, 'train.ind'))
        self.__text_collection.save_tf_idf_matrix(path.join(tmp_dir, 'train.tfidf.sm'))
        self.__text_collection.save_weight_matrix(path.join(tmp_dir, 'train.weight.sm'))
        self.__generate_adjacency_matrix().store_in_file(path.join(tmp_dir, 'train.adjacency.sm'))

    @execution_time_keeper
    def __generate_adjacency_matrix(self):
        adjacency_matrix = SparseAdjacencyMatrix(self.__text_collection.num_of_text,
                                                 self.__text_collection.num_of_text)
        tweets_and_news = self.__get_all_tweet_and_news_texts()
        for i in range(0, len(tweets_and_news)):
            text = tweets_and_news[i]
            adjacency_matrix.add_row(sorted([index for index in text.neighbours]))
        num_of_texts = self.__text_collection.num_of_text - len(tweets_and_news)
        for i in range(0, num_of_texts):
            adjacency_matrix.add_row([])
        return adjacency_matrix

    @execution_time_keeper
    def __join_with_other_texts_and_export(self):
        open(path.join(tmp_dir, 'texts.txt'), 'w').close()
        output_file = codecs.open(path.join(tmp_dir, 'texts.txt'), mode='a', encoding='utf-8')
        for text in self.__get_all_tweet_and_news_texts():
            output_file.write(text.text)
            output_file.write('\n')
        texts_file = codecs.open(self.__texts_file_path, mode='r', encoding='utf-8')
        output_file.write(texts_file.read())
        output_file.close()

    def __get_topk_tweets_by_temporal_relation_for_tweet(self, tweet):
        tweets_in_same_interval = []
        for t in self.tweet_collection.tweets:
            if time_absolute_diff(tweet.published_time, t.published_time).days < 1:
                tweets_in_same_interval.append(t)
        tweets_in_same_interval.sort(
            key=lambda k: self.latent_model.cosine_similarity(tweet.index, k.index),
            reverse=True)
        return tweets_in_same_interval[:Corpora.time_tweets_k]

    def __get_topk_news_by_temporal_relation_for_news(self, news):
        news_in_same_interval = []
        for n in self.news_collection.news_list:
            if time_absolute_diff(n.published_time, news.published_time).days < 1:
                news_in_same_interval.append(n)
        news_in_same_interval.sort(
            key=lambda k: self.latent_model.cosine_similarity(news.index, k.index),
            reverse=True)
        return news_in_same_interval[:Corpora.time_news_k]

    def __get_all_tweet_and_news_texts(self):
        texts = []
        for tweet in self.tweet_collection.tweets:
            texts.append(tweet)
        for news in self.news_collection.news_list:
            texts.append(news)
        texts = sorted(texts, key=lambda t: t.index)
        return texts

    def __find_news_rank(self, tweet):
        news = self.news_collection.news_list.copy()
        for text in news:
            text.sim = self.latent_model.cosine_similarity(
                text.index, tweet.index)
        news.sort(key=lambda i: i.sim, reverse=True)
        for i, n in enumerate(news):
            if tweet.referred_news_id == n.news_id:
                return i + 1
        logger.info('News with id=%s not exists in corpora' % tweet.referred_news_id)
        return -1

    @execution_time_keeper
    def find_relevant_news_index(self):
        self.tweet_collection.tweets = self.__find_relevant_news_index(self.tweet_collection.tweets)
        file = codecs.open(path.join(tmp_dir, 'ranks.txt'), mode='w+', encoding='utf-8')
        for tweet in self.tweet_collection.tweets:
            file.write('%d %s %d\n' % (tweet.index, tweet.referred_news_id, tweet.referred_news_rank))

    @parallel.parallelize_method
    def __find_relevant_news_index(self, tweets):
        new_tweets = []
        for tweet in tweets:
            tweet.referred_news_rank = self.__find_news_rank(tweet)
            new_tweets.append(tweet)
        return new_tweets

    def test(self):
        for t in self.tweet_collection.tweets:
            referred_news = self.news_collection.news_map[t.referred_news_id]
            t.add_neighbour(referred_news)
            referred_news.add_neighbour(t)

    def link_all_news_by_new_feature(self):
        self.news_collection.news_list = self.__link_all_news_by_new_feature(self.news_collection.news_list)
        print('News linked by published time, network name and similarity')
        print('k in new feature', Corpora.news_new_feature)

    @parallel.parallelize_method
    def __link_all_news_by_new_feature(self, news_list):
        new_news_list = []
        for news in news_list:
            collection1 = self.news_collection.filter_by_network(news)
            collection2 = self.news_collection.filter_by_temporal(news)
            collection1 = intersection(collection1, collection2)
            collection1.sort(key=lambda n: self.latent_model.cosine_similarity(n.index, news.index), reverse=True)

            news.add_neighbours(collection1[:Corpora.news_new_feature])
            new_news_list.append(news)
        return new_news_list

    def link_all_tweets_by_author(self):
        self.__link_all_tweets_by_author(self.tweet_collection.tweets)
        print('linked tweets with author name')

    @parallel.parallelize_method
    def __link_all_tweets_by_author(self, tweet_list):
        new_tweet_list = []
        for curr_tweet in tweet_list:
            k = 0
            for tweet in self.tweet_collection.tweets:
                if k < Corpora.tweet_author_k and curr_tweet.index != tweet.index and \
                        curr_tweet.author == tweet.author:
                    curr_tweet.add_neighbour(tweet)
                    new_tweet_list.append(curr_tweet)
        return new_tweet_list

