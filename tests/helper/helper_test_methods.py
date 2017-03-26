from elasticsearch import Elasticsearch


class HelperTestMethods(object):
    @classmethod
    def create_custom_issue(cls, issue={}, articles=[]):
        default = {'name': 'CusomIssue', 'content': 'CustomContent',
                   'publisher': 'CustomPublisher', 'release_from': 'CustomRelease',
                   'release_date': 'CustomRelease', 'number': 'CustomNumber',
                   'source_dirname': 'tests/elastic_filler/slovak/1940', 'page_height': 4000,
                   'page_width': 6000}
        args = {**default, **issue}

        es = Elasticsearch()

        # create issue
        issue = es.index(index='deep_search_test_python', doc_type='issue', body=args)

        # create articles
        ars = []

        if bool(articles):
            for article in articles:
                article['issue'] = {"id": issue['_id']}
                ars.append(
                    es.index(index='deep_search_test_python', doc_type='article',
                             body=article)
                )
        else:
            for i in range(5):
                article = {
                    'groups': [
                        {'page': i, 'type': 'headings', 'text': 'Some Heading number 1', 'l': 45, 'r': 100, 't': 10, 'b': 100},
                        {'page': i, 'type': 'fulltexts', 'text': 'Some Fulltext number 2', 'l': 45, 'r': 100, 't': 120, 'b': 200}
                    ],
                    "authors": ['Miro', 'Jano', 'Prdo'],
                    "keywords": [],
                    "issue": {
                        "id": issue['_id']
                    }
                }
                ars.append(
                    es.index(index='deep_search_test_python', doc_type='article',
                             body=article)
                )

        es.indices.refresh(index='deep_search_test_python')

        #search newly created issue and articles
        issue = es.get(index='deep_search_test_python', doc_type='issue', id=issue['_id'])
        articles = es.search(index='deep_search_test_python', doc_type="article",
                             body={'query': {'bool': {'must': {
                                 'nested': {'path': 'issue', 'query': {'match': {'issue.id': issue['_id']}}}}}},
                                   'size': 1000})['hits']['hits']

        # return created issue and array of articles
        return issue, articles
