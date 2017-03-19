import math
from elasticsearch import Elasticsearch
from textblob import TextBlob as tB


class Analyzer(object):
    def __tf(self, word, blob):
        return blob.words.count(word) / len(blob.words)

    def __n_containing(self, word, bloblist):
        return sum(1 for blob in bloblist if word in blob)

    def __idf(self, word, bloblist):
        return math.log(len(bloblist) / (1 + self.__n_containing(word, bloblist)))

    def __tfidf(self, word, blob, bloblist):
        return self.__tf(word, blob) * self.__idf(word, bloblist)

    # generate key words from bloblist
    def key_words(self, bloblist):

        key_words_art = []

        for i, blob in enumerate(bloblist):
            scores = {word: self.__tfidf(word, blob, bloblist) for word in blob.words}
            sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            key_words = []
            for word, score in sorted_words[:10]:
                key_words.append(word)
            key_words_art.append(key_words)

        return key_words_art

    # generate key words from json
    def key_words_from_json(self, jlist):

        bloblist = []

        for article in jlist:
            all_text = ''
            for group in article['groups']:
                all_text += group['text']
            bloblist.append(tB(all_text))

        key_words_art = self.key_words(bloblist)
        for i, article in enumerate(jlist):
            article['keywords'] = key_words_art[i]

        return

    # generate key words and insert then in to elastic
    def insert_key_words(self, id):

        # establishment of connection
        es = Elasticsearch()

        result = es.search(index="elastic_index", doc_type="article", body={"query": {"match": {"id": id}}})

        article_ids = []
        article_bodies = []

        for hit in result['hits']['hits']:
            article_bodies.append(hit['_source'])
            article_ids.append(hit['_id'])

        self.key_words_from_json(article_bodies)

        for i, article in enumerate(article_bodies):
            updated = es.index(index='elastic_index', doc_type='article', body=article, id=article_ids[i])
            if updated['_id'] != article_ids[i]:
                print("hlaska")  #TODO doplnit
                return 1

        es.indices.refresh(index="issues")
