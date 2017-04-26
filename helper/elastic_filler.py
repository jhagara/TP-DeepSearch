import copy
import json
import logging
from elasticsearch import Elasticsearch, ElasticsearchException
from helper.infohandler import InfoHandler
import config
import re
import datetime
import os
from time import gmtime, strftime


class Elastic(object):
    def save_to_elastic(self, issue_name, dirname, paths):
        elastic_index = config.elastic_index()

        # loading of json templates from empty_jsons
        empty_issue = {}

        empty_article = {}
        groups = []
        empty_group = {}
        empty_issue_art = {}

        articles = []

        # establishment of connection
        es = Elasticsearch()

        # explicitly creating index to be sure
        # es.indices.create(index=elastic_index, ignore=400)

        # SETUP OF ISSUE DOCUMENT
        empty_issue['name'] = issue_name
        # empty_issue_art['name'] = issue_name

        empty_issue['pages_count'] = len(self.articles)
        empty_issue['created_at'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        empty_issue['source_dirname'] = dirname
        empty_issue['journal_marc21_path'] = paths['journal_marc21']

        page_zero = self.xml.xpath("//page")[0]
        empty_issue['page_height'] = int(page_zero.attrib['height'])
        # empty_issue_art['page_height'] = int(page_zero.attrib['height'])
        empty_issue['page_width'] = int(page_zero.attrib['width'])
        # empty_issue_art['page_width'] = int(page_zero.attrib['width'])

        for marcs in self.header['marc21']:
            """
            if marcs['key'] == 'Annual_set':
                empty_issue['release_from'] = marcs['value']
            elif marcs['key'] == 'Date_Location':
                empty_issue['release_date'] = marcs['value']
            elif marcs['key'] == 'Founder':
                empty_issue['publisher'] = marcs['value']
            """
            if marcs['key'] == 'Number':
                empty_issue['number'] = marcs['value']
            elif marcs['key'] == 'Volume':
                empty_issue['year'] = marcs['value']
            elif marcs['key'] == 'Subscription':
                empty_issue['content'] = marcs['value']

            xml_name = paths['xml'].split('/')[-1]
            empty_issue['release_date'] = re.search('[0-9]{8}', xml_name).group(0)
            """
            elif marcs['key'] == 'Cost':
                # neviem

            elif marcs['key'] == 'Address':
                # neviem
            """

        # index | PUT into ES
        # just print new index
        some = es.index(index=elastic_index,  doc_type='issue', body=empty_issue)
        issue_id = some['_id']

        print("Issue created, index: " + elastic_index +
              ", type: issue, id: ", some['_id'])
        empty_issue_art['id'] = some['_id']

        # SETUP OF ARTICLE DOCUMENT
        for page in self.articles:
            for article in page:
                new_article = copy.deepcopy(empty_article)
                groups = []
                article.sort(key= lambda group: int(group.attrib['t']))
                # GETTING MAX FONT SIZE
                heading_sizes = [] 
                for group in article:
                    if group.attrib['type'] == 'headings':
                        for par in group.xpath('par'):
                            for line in par.xpath('line'):
                                for formatting in line.xpath('formatting'):
                                    heading_sizes.append(formatting.get("fs"))
                max_font = max([int(head.split('.', 1)[0]) for head in heading_sizes] or [0])

                # MAIN PART
                for group in article:
                    if group.attrib['type'] == 'headings':
                        new_heading = copy.deepcopy(empty_group)
                        # print(new_heading)
                        new_heading['type'] = 'subheadings'
                        new_heading['l'] = group.attrib['l']
                        new_heading['r'] = group.attrib['r']
                        new_heading['t'] = group.attrib['t']
                        new_heading['b'] = group.attrib['b']
                        new_heading['page'] = group.attrib['page']
                        all_text = ''
                        pars = group.xpath('par')
                        pars.sort(key=lambda x: x.attrib['t'])
                        for par in pars:
                            for line in par.xpath('line'):
                                for formatting in line.xpath('formatting'):
                                    if int(formatting.get("fs").split('.', 1)[0]) == max_font:
                                        new_heading['type'] = 'headings'
                                    all_text += formatting.text + '\n'
                        new_heading['text'] = all_text
                        # print(new_heading)
                        groups.append(new_heading)
                    elif group.attrib['type'] == 'fulltexts':
                        new_fulltext = copy.deepcopy(empty_group)
                        new_fulltext['type'] = 'fulltexts'
                        new_fulltext['l'] = group.attrib['l']
                        new_fulltext['r'] = group.attrib['r']
                        new_fulltext['t'] = group.attrib['t']
                        new_fulltext['b'] = group.attrib['b']
                        new_fulltext['page'] = group.attrib['page']
                        all_text = ''
                        pars = group.xpath('par')
                        pars.sort(key=lambda x: x.attrib['t'])
                        for par in pars:
                            for line in par.xpath('line'):
                                for formatting in line.xpath('formatting'):
                                    all_text += formatting.text + '\n'
                        new_fulltext['text'] = all_text
                        # print(new_fulltext)
                        groups.append(new_fulltext)
                new_article['groups'] = groups
                # print(groups)
                new_article['issue'] = empty_issue_art
                articles.append(new_article)

        ar_count = 0

        error_name = config.get_full_path('logs', 'error.log')
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        error_logger = logging.getLogger()
        error_logger.setLevel(logging.ERROR)

        if not os.path.exists(error_name):
            e_file = open(error_name, 'w')

        error_handler = logging.FileHandler(error_name)
        error_handler.setFormatter(formatter)
        error_logger.addHandler(error_handler)

        info_logger = logging.getLogger()
        info_name = config.get_full_path('logs', 'info.log')

        if not os.path.exists(info_name):
            i_file = open(info_name, 'w')

        info_handler = InfoHandler(info_name)
        info_handler.setFormatter(formatter)
        info_logger.addHandler(info_handler)

        for art in articles:
            # index | PUT into ES
            try:
                some = es.index(index=elastic_index, doc_type='article', body=art)
                ar_count += 1
            except ElasticsearchException:
                pass

        number = str(xml_name)

        info_logger.info(str(datetime.date.today()) + "Journal " + issue_name + ", issue num. " +
                         number + " was parsed.")
        info_logger.info(str(datetime.date.today()) + "Articles created: " + str(ar_count) +
                         "/" + str(len(articles)) + ".")

        es.indices.refresh(index=elastic_index)

        return issue_id

