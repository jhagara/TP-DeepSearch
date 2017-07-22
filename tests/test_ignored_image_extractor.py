import unittest
import os
from helper.image_processor import ImageProcessor
from PIL import Image
import glob


class TestImageExport(unittest.TestCase):

    def test_create_images(self):
        articles = [
                      {
                        "_index": "deep_search_test_python",
                        "_type": "article",
                        "_id": "AVtpuETlLK4gTCUnA1O-",
                        "_score": 1,
                        "_source": {
                          "source_dirname": "/",
                          "groups": [
                            {
                              "l": "990",
                              "b": "1051",
                              "t": "966",
                              "type": "headings",
                              "text": "HD",
                              "r": "2506",
                              "page": 2
                            },
                            {
                              "l": "984",
                              "b": "1737",
                              "t": "1074",
                              "type": "fulltexts",
                              "text": "FT",
                              "r": "2514",
                              "page": 2
                            }
                          ],
                            "is_ignored": True,
                          "issue": {
                            "id": "AVtpuENYLK4gTCUnA1O0"
                          }
                        }
                      },
                      {
                        "_index": "deep_search_test_python",
                        "_type": "article",
                        "_id": "AVtpuEX0LK4gTCUnA1PN",
                        "_score": 1,
                        "_source": {
                          "source_dirname": "/",
                          "groups": [
                            {
                              "l": "2544",
                              "b": "4804",
                              "t": "2068",
                              "type": "fulltexts",
                              "text": "FT",
                              "r": "3290",
                              "page": 5
                            },
                            {
                              "l": "1058",
                              "b": "2658",
                              "t": "2388",
                              "type": "headings",
                              "text": "HD ",
                              "r": "1591",
                              "page": 5
                            },
                            {
                              "l": "964",
                              "b": "3948",
                              "t": "2689",
                              "type": "fulltexts",
                              "text": "FT",
                              "r": "1712",
                              "page": 5
                            },
                            {
                              "l": "1756",
                              "b": "4802",
                              "t": "3264",
                              "type": "fulltexts",
                              "text": "FT",
                              "r": "2503",
                              "page": 5
                            }
                          ],
                            "is_ignored": False,
                          "issue": {
                            "id": "AVtpuENYLK4gTCUnA1O0"
                          }
                        }
                      },
                      {
                        "_index": "deep_search_test_python",
                        "_type": "article",
                        "_id": "AVtpuEZiLK4gTCUnA1PU",
                        "_score": 1,
                        "_source": {
                          "source_dirname": "/",
                          "groups": [
                            {
                              "l": "1988",
                              "b": "3855",
                              "t": "3803",
                              "type": "headings",
                              "text": "HD",
                              "r": "2251",
                              "page": 6
                            },
                            {
                              "l": "1844",
                              "b": "4087",
                              "t": "3900",
                              "type": "fulltexts",
                              "text": "FT",
                              "r": "2455",
                              "page": 7
                            }
                          ],
                            "is_ignored": False,
                          "issue": {
                            "id": "AVtpuENYLK4gTCUnA1O0"
                          }
                        }
                      }
                    ]
        
        pics_dirname = os.path.dirname(os.path.abspath(__file__)) + "/19430526/STR"
        print(os.path.dirname(os.path.abspath(__file__)))
        pages_paths = glob.glob(pics_dirname + '/*.jpg')
        pages_paths.sort()
        # print(len(pages_paths))

        remove_paths = []
        try:
            for i, article in enumerate(articles):
                abs_path = os.path.dirname(os.path.abspath(__file__)) + "/19430526/article" + str(i + 1)
                article['_source']['source_dirname'] = abs_path
                name = ImageProcessor.export_article_image(article, pages_paths)

                # check if 1st article is really ignored
                if i == 0:
                    self.assertIsNone(name)

                else:
                    remove_paths.append(name)
                    test_path = str(name[:-4] + '_true.jpg')

                    test = Image.open(test_path)
                    created = Image.open(name)

                    test_hist = test.histogram()
                    created_hist = created.histogram()

                    self.assertEqual(created_hist, test_hist)

        finally:
            for path in remove_paths:
                os.remove(path)

