import copy
import json
import math
from elasticsearch import Elasticsearch
from textblob import TextBlob as tB


class Elastic(object):
    def save_to_elastic(self, issue_name, dirname):
        # loading of json templates from empty_jsons
        with open('helper/empty_jsons/issue.json') as issue_file:
            empty_issue = json.load(issue_file)

        with open('helper/empty_jsons/article.json') as article_file:
            empty_article = json.load(article_file)
            groups = []
            empty_group = empty_article['groups'][0]
            empty_issue_art = empty_article['issue']

        articles = []

        # establishment of connection
        es = Elasticsearch()

        # explicitly creating index to be sure
        es.indices.create(index='issues', ignore=400)

        # SETUP OF ISSUE DOCUMENT
        empty_issue['name'] = issue_name
        empty_issue_art['name'] = issue_name

        empty_issue['source_dirname'] = dirname

        page_zero = self.xml.xpath("//page")[0]
        empty_issue['page_height'] = int(page_zero.attrib['height'])
        empty_issue_art['page_height'] = int(page_zero.attrib['height'])
        empty_issue['page_width'] = int(page_zero.attrib['width'])
        empty_issue_art['page_width'] = int(page_zero.attrib['width'])

        for marcs in self.header['marc21']:
            if marcs['key'] == 'Annual_set':
                empty_issue['release_from'] = marcs['value']
            elif marcs['key'] == 'Number':
                empty_issue['number'] = marcs['value']
                empty_issue_art['number'] = marcs['value']
            elif marcs['key'] == 'Date_Location':
                empty_issue['release_date'] = marcs['value']
            elif marcs['key'] == 'Founder':
                empty_issue['publisher'] = marcs['value']
            elif marcs['key'] == 'Subscription':
                empty_issue['content'] = marcs['value']
            """
            elif marcs['key'] == 'Cost':
                # neviem

            elif marcs['key'] == 'Address':
                # neviem
            """

        # index | PUT into ES
        some = es.index(index='issues',  doc_type='issue', body=empty_issue)

        print("Issue created with id: ", some['_id'])
        empty_issue_art['id'] = some['_id']

        # SETUP OF ARTICLE DOCUMENT
        strana = 0
        for page in self.articles:
            strana = strana + 1
            for article in page:
                new_article = copy.deepcopy(empty_article)
                groups = []
                for group in article:
                    if group.attrib['type'] == 'headings':
                        new_heading = copy.deepcopy(empty_group)
                        # print(new_heading)
                        new_heading['type'] = 'heading'
                        new_heading['l'] = group.attrib['l']
                        new_heading['r'] = group.attrib['r']
                        new_heading['t'] = group.attrib['t']
                        new_heading['b'] = group.attrib['b']
                        new_heading['page'] = strana
                        all_text = ''
                        for par in group.xpath('par'):
                            for line in par.xpath('line'):
                                for formatting in line.xpath('formatting'):
                                    all_text += formatting.text
                        new_heading['text'] = all_text
                        # print(new_heading)
                        groups.append(new_heading)
                    elif group.attrib['type'] == 'fulltexts':
                        new_fulltext = copy.deepcopy(empty_group)
                        new_fulltext['type'] = 'fulltext'
                        new_fulltext['l'] = group.attrib['l']
                        new_fulltext['r'] = group.attrib['r']
                        new_fulltext['t'] = group.attrib['t']
                        new_fulltext['b'] = group.attrib['b']
                        new_fulltext['page'] = strana
                        all_text = ''
                        for par in group.xpath('par'):
                            for line in par.xpath('line'):
                                for formatting in line.xpath('formatting'):
                                    all_text += formatting.text
                        new_fulltext['text'] = all_text
                        # print(new_fulltext)
                        groups.append(new_fulltext)
                new_article['groups'] = groups
                # print(groups)
                new_article['issue'] = empty_issue_art
                articles.append(new_article)

        for art in articles:
            # index | PUT into ES
            some = es.index(index='issues', doc_type='article', body=art)

            print("Article created with id: ", some['_id'])

        es.indices.refresh(index="issues")

    def __tf(self, word, blob):
        return blob.words.count(word) / len(blob.words)

    def __n_containing(self, word, bloblist):
        return sum(1 for blob in bloblist if word in blob)

    def __idf(self, word, bloblist):
        return math.log(len(bloblist) / (1 + self.__n_containing(word, bloblist)))

    def __tfidf(self, word, blob, bloblist):
        return self.__tf(word, blob) * self.__idf(word, bloblist)

    def key_words(self, bloblist):

        key_words_art = []

        for i, blob in enumerate(bloblist):
            scores = {word: self.__tfidf(word, blob, bloblist) for word in blob.words}
            sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            key_words_art.append(sorted_words[:10])

        return key_words_art

    def key_words_from_json(self, jlist):

        bloblist = []

        for article in jlist:
            all_text = ''
            for group in article['groups']:
                all_text += group['text']
            bloblist.append(tB(all_text))

        key_words_art = self.key_words(bloblist)
        for i, article in jlist:
            article['keywords'] = key_words_art[i]

        return

    def insert_key_words(self, id):

        # establishment of connection
        es = Elasticsearch()

        result = es.search(index="issues", doc_type="article", body={"query": {"match": {"id": id}}})

        article_ids = []
        article_bodies = []

        for hit in result['hits']['hits']:
            article_bodies.append(hit['_source'])
            article_ids.append(hit['_id'])

        self.key_words_from_json(article_bodies)

        for i, article in enumerate(article_bodies):
            updated = es.index(index='issues', doc_type='article', body=article, id=article_ids[i])
            if updated['_id'] != article_ids[i]:
                print("hlaska")  #TODO doplnit
                return 1

        es.indices.refresh(index="issues")


