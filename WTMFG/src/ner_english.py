# coding: utf-8

import nltk
from nltk.tag.stanford import StanfordNERTagger

jar = './src/stanford-ner-tagger/stanford-ner.jar'
model = './src/stanford-ner-tagger/ner-model-english.ser.gz'
# model = '/Users/amir/hodaProject/code/src/stanford-ner-tagger/english.all.3class.distsim.crf.ser.gz'

class NamedEntityRecognizer:

    @staticmethod
    def find_named_entities(text):
        ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')
        words = nltk.word_tokenize(text)
        result = set()
        o_tokens = set()
        tokens = ner_tagger.tag(words)
        for token in tokens:
            if token[1] == 'O':
                o_tokens.add(token[0])
        for token in tokens:
            if token[0] not in o_tokens:
                result.add(token[0])
        return result


# text = "Tehran is the capital of Iran. Cristian Ronaldo "
# NamedEntityRecognizer.find_named_entities(text)
