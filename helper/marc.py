from elasticsearch import Elasticsearch
import config
import os
from pymarc import MARCReader, Record, Field
from time import gmtime, strftime

#  pymarc cheat sheets at :
# https://github.com/ThursdayPythonCodeClub/Code-Examples/blob/master/ex-tab-delim-2-marc/pymarc-cheat-sheet.py


class Marc(object):
    #  export issue into marc
    def __export_issue(self, issue, journal_marc, source_dirname, es, index):
        issue_record = Record(leader='     nas  22     uic4500', force_utf8=True)

        # 001
        issue_record.add_field(Field(tag='001', data=issue['_id']))

        # 003 VRT = organization code for UKB
        issue_record.add_field(Field(tag='003', data='VRT'))

        # 005
        time = self.__get_time()
        issue_record.add_field(Field(tag='005', data=time))

        # 008
        issue_record.add_field(self.__get_008_issue(issue, journal_marc, time))

        # 007
        issue_record.add_field(Field(tag='007', data="ta"))

        # 022
        if journal_marc['022']['a'] is not None:
            issue_record.add_field(Field(tag='022',
                                         indicators=[' ', ' '],
                                         subfields=['a', journal_marc['022']['a']]))

        # 245
        n_245 = issue['_source']['release_date'][0:3] + ", "
        if issue['_source']['year'] is not None:
            n_245 += issue['_source']['year'] + ", "
        else:
            n_245 += " , "

        if issue['_source']['number'] is not None:
            n_245 += issue['_source']['number']
        else:
            n_245 += " "

        issue_record.add_field(
            Field(
                tag='245',
                indicators=[' ', ' '],
                subfields=['a', issue['_source']['name'],
                           'n', n_245]
            )
        )

        # 264
        place_of_release = ""
        if journal_marc['264']['a'] is not None:
            place_of_release = journal_marc['264']['a']

        publisher = ""
        if issue['_source']['publisher'] is not None and len(issue['_source']['publisher']) > 0:
            publisher = issue['_source']['publisher']
        elif journal_marc['264']['b'] is not None:
            publisher = journal_marc['264']['b']

        issue_record.add_field(
            Field(
                tag='264',
                indicators=[' ', ' '],
                subfields=['a', place_of_release,
                           'b', publisher,
                           'c', issue['_source']['release_date'][0:3]]
            )
        )

        # 300
        issue_record.add_field(Field(tag='300', indicators=[' ', ' '], subfields=['a',
                                                                                  str(issue['_source']['page_count'])]))

        # 336
        issue_record.add_field(
            Field(
                tag='336',
                indicators=[' ', ' '],
                subfields=['a', 'text',
                           'b', 'txt',
                           '2', 'rdacontent']
            )
        )

        # 337
        issue_record.add_field(
            Field(
                tag='337',
                indicators=[' ', ' '],
                subfields=['a', 'bez média',
                           'b', 'n',
                           '2', 'rdamedia']
            )
        )

        # 338
        issue_record.add_field(
            Field(
                tag='338',
                indicators=[' ', ' '],
                subfields=['a', 'zväzok',
                           'b', 'nc',
                           '2', 'rdacarrier']
            )
        )

        # 773
        issue_record.add_field(
            Field(
                tag='773',
                indicators=[' ', ' '],
                subfields=['w', journal_marc['001'].value(),
                           't', journal_marc['245']['a'],
                           '7', 'nnas']
            )
        )

        path = source_dirname + "/issue_marc21.txt"
        self.__save_marc(issue_record, path)

        es.update(index=index,
                  doc_type='issue',
                  id=issue['_id'],
                  body={
                      "script": {
                          "inline": "ctx._source.issue_marc21_path = params.path",
                          "lang": "painless",
                          "params": {
                              "path": path
                          }
                      }
                  })
        return issue_record

    #  export article into marc
    def __export_article(self, article, issue_marc, source_dirname, order, es, index):
        article_record = Record(leader='     nas  22     uic4500', force_utf8=True)

        # 001
        article_record.add_field(Field(tag='001', data=article['_id']))

        # 003
        article_record.add_field(Field(tag='003', data='VRT'))

        # 005
        time = self.__get_time()
        article_record.add_field(Field(tag='005', data=time))

        # 008
        article_record.add_field(issue_marc['008'])

        # 007
        article_record.add_field(Field(tag='007', data="ta"))

        # 245
        heading, subheading = self.__heading_subheadings(article)
        article_record.add_field(
            Field(
                tag='245',
                indicators=[' ', ' '],
                subfields=['a', heading,
                           'b', subheading]
            )
        )

        # 264
        article_record.add_field(issue_marc['264'])

        # 336
        article_record.add_field(issue_marc['336'])

        # 337
        article_record.add_field(issue_marc['337'])

        # 338
        article_record.add_field(issue_marc['338'])

        # 100
        if len(article['_source']['authors']) > 0:
            article_record.add_ordered_field(
                Field(
                    tag='100',
                    indicators=['1', ' '],
                    subfields=['a', article['_source']['authors'][0]]
                )
            )
            article_record['245'].add_subfield('c', article['_source']['authors'][0])

        # 653
        for word in article['_source']['keywords']:
            article_record.add_field(
                Field(
                    tag='653',
                    indicators=[' ', ' '],
                    subfields=['a', word]
                )
            )

        # 700
        if len(article['_source']['authors']) > 1:
            for author in article['_source']['authors'][1:]:
                article_record.add_field(
                    Field(
                        tag='700',
                        indicators=['1', ' '],
                        subfields=['a', author]
                    )
                )

        # 773
        article_record.add_field(
            Field(
                tag='773',
                indicators=[' ', ' '],
                subfields=['w', issue_marc['001'].value(),
                           't', issue_marc['245']['a'],
                           '7', 'nnas']
            )
        )

        path = source_dirname + "/articles/" + str(order)
        if not os.path.exists(path):
            os.makedirs(path)
        path += "/" + str(order) + "_marc21.txt"
        self.__save_marc(article_record, path)

        es.update(index=index,
                  doc_type='article',
                  id=article['_id'],
                  body={
                      "script": {
                          "inline": "ctx._source.article_marc21_path = params.path",
                          "lang": "painless",
                          "params": {
                              "path": path
                          }
                      }
                  })

    # get time in format  yyyymmddhhmmss.f
    def __get_time(self):
        time = strftime("%Y%m%d%H%M%S", gmtime())
        return time + ".0"

    def __get_008_issue(self, issue, journal_marc, time):
        data_008 = time[2:8]
        data_008 += 'e'
        data_008 += issue['_source']['release_date']
        data_008 += journal_marc['008'].value()[15:17]
        data_008 += "                 "
        data_008 += journal_marc['008'].value()[35:37]
        data_008 += " "
        data_008 += "d"

        return Field(tag='008', data=data_008)

    def __heading_subheadings(self, article):
        heading = ""
        subheading = ""

        for group in article['_source']['groups']:
            if group['type'] == 'headings' and heading == "":
                heading = group['text']
            elif group['type'] == 'headings' and heading != "":
                heading += " " + group['text']
            elif group['type'] == 'subheadings' and subheading == "":
                subheading = group['text']
            elif group['type'] == 'subheadings' and subheading != "":
                subheading += " " + group['text']

        return heading, subheading

    #  save marc on path
    def __save_marc(self, marc, path):
        with open(path, 'wb') as f:
            f.write(marc.as_marc())

    def export_marc_for_issue(self, issue_id):

        elastic_index = config.elastic_index()

        #  get issue and article from elastic
        es = Elasticsearch()
        issue = es.get(index=elastic_index, doc_type='issue', id=issue_id)
        articles = es.search(index=elastic_index, doc_type="article",
                             body={'query': {'bool': {'must': {
                                 'nested': {'path': 'issue', 'query': {'match': {'issue.id': issue_id}}}}}},
                                 'size': 1000})['hits']['hits']

        journal_path = issue['_source']['journal_marc21_path']
        source_dirname = issue['_source']['source_dirname']

        #  get marc21 for jurnal
        with open(journal_path, 'rb') as fh:
            reader = MARCReader(fh)
            journal_marc = next(reader)

        issue_marc = self.__export_issue(issue, journal_marc, source_dirname, es, elastic_index)

        for i, article in enumerate(articles):
            self.__export_article(article, issue_marc, source_dirname, i+1, es, elastic_index)

        es.indices.refresh(index=elastic_index)

