import unittest
import os
import shutil
from helper.image_processor import ImageProcessor
from PIL import Image
import glob


class TestImageExport(unittest.TestCase):

    def test_create_images(self):
        source_dirname = os.path.dirname(os.path.abspath(__file__)) + "/19430526"

        # rem_dir = source_dirname + "/STR_small"

        pics_dirname_small = os.path.dirname(os.path.abspath(__file__)) + "/19430526/STR_small_true"
        pages_paths_small = glob.glob(pics_dirname_small + '/*.jpg')
        pages_paths_small.sort()
        
        try:
            num_pics = ImageProcessor.compress_images(source_dirname)
            self.assertEqual(len(pages_paths_small), num_pics)

            for test_path in pages_paths_small:
                new_path = page.replace('STR_small_true','STR_small')
                # print(test_path, name)
                test = Image.open(test_path)
                created = Image.open(new_path)
                self.assertEqual(created, test)

                test_hist = test.histogram()
                created_hist = created.histogram()
                self.assertEqual(created_hist, test_hist)

        finally:
            print('done')
