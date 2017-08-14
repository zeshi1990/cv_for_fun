from utils.logger import Logger

import os
import logging
import urllib

import pandas as pd
from PIL import Image


class ImgDownloader:
    def __init__(self):
        # create logger
        self.logger = Logger(name="Image Downloader", level=logging.DEBUG)
        self.logger.info("Image Downloader Initialize Start")
        self._img_url_db = pd.read_csv("fall11_urls.txt",
                                       delimiter="\t",
                                       header=None,
                                       names=["id", "url"],
                                       error_bad_lines=False)
        self.logger.info("Image Downloader Initialize Complete")

    def get_table_length(self):
        return self._img_url_db.shape[0]

    def get_url(self, idx):
        return self._img_url_db.iloc[idx, 1]

    def print_table(self):
        print self._img_url_db

    def download_img(self, idx):
        url = self._img_url_db.loc[idx, "url"]
        base_fn = self._img_url_db.loc[idx, "id"]
        if not os.path.exists("tmp"):
            os.mkdir("tmp")
        fn = os.path.join("tmp", base_fn)
        try:
            urllib.urlretrieve(url, fn)
        except Exception, e:
            print "a"
            self.logger.warn(e)
        try:
            Image.open(fn)
            self.logger.info("Downloaded image id: {0}; url[{1}]".format(base_fn, url))
        except IOError as e:
            print "b"
            self.logger.warn(e)
            os.remove(fn)
            return 1
        return 0

    def remove_img(self, idx):
        url = self._img_url_db.loc[idx, "url"]
        base_fn = self._img_url_db.loc[idx, "id"]
        fn = os.path.join("tmp", base_fn)
        try:
            os.remove(fn)
            self.logger.info("Removed image id: {0}; url[{1}]".format(base_fn, url))
        except Exception, e:
            print "c"
            self.logger.warn(e)
            return 1
        return 0

    def download_batch(self, idx_start, size):
        for i in range(idx_start, idx_start + size):
            self.download_img(i)
        return 0


def main():
    img_downloader = ImgDownloader()
    img_downloader.download_batch(0, 5)
    img_downloader.remove_img(1)

if __name__=="__main__":
    main()
