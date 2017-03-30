from elasticsearch import Elasticsearch
import config
from pymarc import MARCReader, Record, Field
from time import gmtime, strftime


class Marc(object):
    #  export issue into marc
    def __export_issue(self, issue, journal_marc, source_dirname):
        issue_record = Record()

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
                                         subfields=['a', journal_marc['022']['a']]))

        # 245
        n_245 = issue['release_date'][0:3] + ", "
        if issue['year'] is not None:  # TODO pozriet ako je year v elasticu
            n_245 += issue['year'] + ", "
        else:
            n_245 += " , "

        if issue['number'] is not None:
            n_245 += issue['number']
        else:
            n_245 += " "

        issue_record.add_field(
            Field(
                tag='245',
                subfields=['a', issue['name'],
                           'n', n_245]
            )
        )

        # 264
        place_of_release = None
        if journal_marc['264']['a'] is not None:
            place_of_release = journal_marc['264']['a']

        publisher = None
        if issue['publisher'] is not None and len(issue['publisher']) > 0:
            publisher = issue['publisher']
        elif journal_marc['264']['b'] is not None:
            publisher = journal_marc['264']['b']

        issue_record.add_field(
            Field(
                tag='264',
                subfields=['a', place_of_release,
                           'b', publisher,
                           'c', issue['release_date'][0:3]]
            )
        )

        # 300 $$a
        # počet
        # strán
        #  TODO doplnit

        # 336
        issue_record.add_field(
            Field(
                tag='336',
                subfields=['a', 'text',
                           'b', 'txt',
                           '2', 'rdacontent']
            )
        )

        # 337
        issue_record.add_field(
            Field(
                tag='337',
                subfields=['a', 'bez média',
                           'b', 'n',
                           '2', 'rdamedia']
            )
        )

        # 338
        issue_record.add_field(
            Field(
                tag='338',
                subfields=['a', 'zväzok',
                           'b', 'nc',
                           '2', 'rdacarrier']
            )
        )
        path = ""  # TODO doplnit
        self.__save_marc(issue_record, path)

    #  export article into marc
    def __export_article(self, article, issue_marc, source_dirname):
        print()

    # get time in format  yyyymmddhhmmss.f
    def __get_time(self):
        time = strftime("%Y%m%d%H%M%S", gmtime())
        return time + ".0"

    def __get_008_issue(self, issue, journal_marc, time):
        data_008 = time[2:8]
        data_008 += 'e'
        data_008 += issue['release_date']
        data_008 += journal_marc['008']['data'][15:17]
        data_008 += "                 "
        data_008 += journal_marc['008']['data'][35:37]
        data_008 += " "
        data_008 += "d"

        return Field(tag='008', data=data_008)

    #  save marc on path
    def __save_marc(self, marc, path):
        print()

    def export_marc_for_issue(self, issue_id):

        elastic_index = config.elastic_index()

        #  get issue and article from elastic
        es = es = Elasticsearch()
        issue = es.get(index=elastic_index, doc_type='issue', id=issue_id)
        articles = es.search(index=elastic_index, doc_type="article",
                             body={'query': {'bool': {'must': {
                                 'nested': {'path': 'issue', 'query': {'match': {'issue.id': issue_id}}}}}},
                                 'size': 1000})['hits']['hits']

        journal_path = issue['journal_marc21']  # TODO skontrolovat v elasticu
        source_dirname = issue['source_dirname']

        #  get marc21 for jurnal

        with open(journal_path, 'rb') as fh:
            reader = MARCReader(fh)
            journal_marc = next(reader)

        issue_marc = self.__export_issue(issue, journal_marc, source_dirname)

        for article in articles:
            self.__export_article(article, issue_marc, source_dirname)


# with open('/home/jakub/git/TP-DeepSeach/helper/marc.txt', 'rb') as fh:
#     reader = MARCReader(fh)
#     journal_marc = next(reader)
#     e = journal_marc['245']
#     print(e)
#     new = Record()
#     new.add_field(e)
#     print(new)

# time = strftime("%Y%m%d%H%M%S", gmtime())
# print(time[2:8])
