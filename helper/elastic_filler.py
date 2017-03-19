import copy
import json
from elasticsearch import Elasticsearch


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
