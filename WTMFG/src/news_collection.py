from src.multi_process import Parallel
from src.ner_english import NamedEntityRecognizer
from src.utilites import time_absolute_diff

parallel = Parallel()


class NewsCollection:
    network_k = 10

    def __init__(self):
        self.named_entities = set()
        self.news_list = []
        self.news_map = {}
        self.id_index_map = {}
        self.texts = ''

    def add_news(self, news):
        self.news_list.append(news)
        self.news_map[news.news_id] = news
        self.id_index_map[news.news_id] = news.index
        self.texts += news.text + '\n'

    def find_named_entities(self):
        named_entities = NamedEntityRecognizer.find_named_entities(self.texts)
        self.named_entities.update(named_entities)
        return self.named_entities

    def link_by_network(self):
        self.news_list = self.__link_by_network(self.news_list)

    @parallel.parallelize_method
    def __link_by_network(self, news_list):
        new_news_list = []
        for news in news_list:
            new_news = self.__link_topk_news_with_same_network(news)
            new_news_list.append(new_news)
        return new_news_list

    def __link_topk_news_with_same_network(self, reference_news):
        self.news_list.sort(key=lambda news: time_absolute_diff(reference_news.published_time,
                                                                news.published_time).total_seconds())
        num_of_linked = 0
        for news in self.news_list:
            if news.news_id != reference_news.news_id and news.get_network_name() == reference_news.get_network_name() \
                    and num_of_linked < NewsCollection.network_k:
                reference_news.add_neighbour(news)
                num_of_linked += 1
        return reference_news

    def filter_by_network(self, curr_news):
        new_news_list = []
        for news in self.news_list:
            if news.get_network_name() == curr_news.get_network_name():
                new_news_list.append(news)
        return new_news_list

    def filter_by_temporal(self, curr_news):
        new_news_list = []
        for news in self.news_list:
            if time_absolute_diff(news.published_time, curr_news.published_time).days < 1:
                new_news_list.append(news)
        return new_news_list
