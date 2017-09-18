import unittest
import os
import shutil
from copy import deepcopy
from helper.image_processor import ImageProcessor
from PIL import Image
import glob


class TestImageCompress(unittest.TestCase):

    def test_compress_images(self):
        source_dirname = os.path.dirname(os.path.abspath(__file__)) + "/19430526"

        rem_dir = source_dirname + "/STR_small"
        try:
            num_pics = ImageProcessor.compress_images(source_dirname)

            pics_dirname_small = source_dirname + "/STR_small"
            pages_paths_small = glob.glob(pics_dirname_small + '/*.jpg')
            pages_paths_small.sort()

            self.assertEqual(len(pages_paths_small), num_pics)

            for test_path in pages_paths_small:
                new_path = deepcopy(test_path)
                new_path = new_path.replace('STR_small', 'STR')

                test_path_info = os.stat(test_path)
                test_path_size = test_path_info.st_size

                new_path_info = os.stat(new_path)
                new_path_size = new_path_info.st_size
                
                self.assertGreater(new_path_size, test_path_size)
                # print(test_path, new_path)

        finally:
            shutil.rmtree(rem_dir)
