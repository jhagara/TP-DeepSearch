from PIL import Image
from elasticsearch import Elasticsearch
import config
import os
import glob


class ImageExtractor(object):
    #  export image per article
    @classmethod
    def export_article_image(cls, article, pages_paths):

        path = str(article['_source']['source_dirname']) + '/pictures'

        if not os.path.exists(path):
            os.makedirs(path)

        pages = []

        for group in article['_source']['groups']:
            page = int(group['page']) - 1
            if page not in pages:
                pages.append(page)

        crop_groups = [[] for _ in range(len(pages))]
        gps_groups = [[] for _ in range(len(pages))]

        for group in article['_source']['groups']:
            page = int(group['page']) - 1
            page_path = pages_paths[page]
            original = Image.open(page_path)
            left = int(group['l'])
            right = int(group['r'])
            top = int(group['t'])
            bottom = int(group['b'])
            ltrb = (left, top, right, bottom)
            gps_groups[pages.index(page)].append(ltrb)
            crop_groups[pages.index(page)].append(original.crop(ltrb))

        for i, page in enumerate(pages):
            width, height = Image.open(pages_paths[int(page)]).size
            black = Image.new('L', (width, height), 'black')
            for cropped_block, gps in zip(crop_groups[i], gps_groups[i]):
                black.paste(cropped_block, gps)

        image_path = path + '/article_extract_page' + str(pages[i]+1) + '.jpg'
        black.save(image_path)
        return image_path

    def export_image_for_issue(self, issue_id):

        elastic_index = config.elastic_index()

        #  get issue and article from elastic
        es = Elasticsearch()
        issue = es.get(index=elastic_index, doc_type='issue', id=issue_id)
        articles = es.search(index=elastic_index, doc_type="article",
                             body={'query': {'bool': {'must': {
                                 'nested': {'path': 'issue', 'query': {'match': {'issue.id': issue_id}}}}}},
                                 'size': 1000})['hits']['hits']

        pics_dirname = issue['_source']['source_dirname'] + '/STR'
        pages_paths = glob.glob(pics_dirname + '/*.jpg')
        pages_paths.sort()

        for article in articles:
            self.export_article_image(article, pages_paths)