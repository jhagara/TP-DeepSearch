from helper.downloader import Downloader
import unittest
import os
import shutil


class TestDownloader(unittest.TestCase):
    TEST_URL = "https://kramerius.mzk.cz"  # change if needed
    TEST_UUID = "uuid:06a34a20-7042-11dd-b8d0-000d606f5dc6"  # change if needed

    def test_downloader(self):
        path = os.path.dirname(os.path.abspath(__file__)) + "/.."
        downloader = Downloader()
        downloader.download_item(self.TEST_URL, self.TEST_UUID, path)
        expected_files = ["/kramerius/Lidové noviny/51/32***/XML/1_uuid:f3dee9b0-6ada-11dd-9c52-000d606f5dc6.xml",
                          "/kramerius/Lidové noviny/51/32***/XML/2_uuid:a7aaec20-6ae3-11dd-9a90-000d606f5dc6.xml",
                          "/kramerius/Lidové noviny/51/32***/XML/3_uuid:f3e5ee90-6ada-11dd-96e5-000d606f5dc6.xml",
                          "/kramerius/Lidové noviny/51/32***/XML/4_uuid:a7ad8430-6ae3-11dd-8a3a-000d606f5dc6.xml",
                          "/kramerius/Lidové noviny/51/32***/XML/5_uuid:f3eb1eb0-6ada-11dd-9093-000d606f5dc6.xml",
                          "/kramerius/Lidové noviny/51/32***/XML/6_uuid:a7b21810-6ae3-11dd-b5a7-000d606f5dc6.xml",
                          "/kramerius/Lidové noviny/51/32***/XML/7_uuid:f3f1ae60-6ada-11dd-99f9-000d606f5dc6.xml",
                          "/kramerius/Lidové noviny/51/32***/XML/8_uuid:a7b6abf0-6ae3-11dd-b261-000d606f5dc6.xml",
                          "/kramerius/Lidové noviny/51/32***/STR/1_uuid:f3dee9b0-6ada-11dd-9c52-000d606f5dc6.jpeg",
                          "/kramerius/Lidové noviny/51/32***/STR/2_uuid:a7aaec20-6ae3-11dd-9a90-000d606f5dc6.jpeg",
                          "/kramerius/Lidové noviny/51/32***/STR/3_uuid:f3e5ee90-6ada-11dd-96e5-000d606f5dc6.jpeg",
                          "/kramerius/Lidové noviny/51/32***/STR/4_uuid:a7ad8430-6ae3-11dd-8a3a-000d606f5dc6.jpeg",
                          "/kramerius/Lidové noviny/51/32***/STR/5_uuid:f3eb1eb0-6ada-11dd-9093-000d606f5dc6.jpeg",
                          "/kramerius/Lidové noviny/51/32***/STR/6_uuid:a7b21810-6ae3-11dd-b5a7-000d606f5dc6.jpeg",
                          "/kramerius/Lidové noviny/51/32***/STR/7_uuid:f3f1ae60-6ada-11dd-99f9-000d606f5dc6.jpeg",
                          "/kramerius/Lidové noviny/51/32***/STR/8_uuid:a7b6abf0-6ae3-11dd-b261-000d606f5dc6.jpeg"]
        for file in expected_files:
            self.assertTrue(os.path.exists(path + file), file + " is missing")

        shutil.rmtree(path + "/kramerius")
