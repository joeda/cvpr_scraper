#!/usr/bin/env python3

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import argparse
import urllib.parse
import os

def dl_pdf(base_url, pdf_path, target_dir):
    full_path = urllib.parse.urljoin(base_url, pdf_path)
    target_file = os.path.join(target_dir, pdf_path)
    abs_dir = os.path.dirname(target_file)
    if not os.path.exists(abs_dir):
        os.makedirs(abs_dir)
    urllib.request.urlretrieve(full_path, target_file)

def get_pdf_list(baseurl):
    response = requests.get(baseurl)
    soup = BeautifulSoup(response.text, "html.parser")
    return [l["href"] for l in soup.find_all("a", text="pdf")]

def range_with_status(total):
    """ iterate from 0 to total and show progress in console """
    n = 0
    while n <= total:
        s = '[{0}]'.format(str(n)+ "/" + str(total))
        if n == total:
            s += '\n'
        if n > 0:
            s = '\r' + s
        print(s, end='')
        yield n
        n += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Download papers from CVPR open access")
    parser.add_argument("base_url", type=str, help="Website to scrape, i. e. http://openaccess.thecvf.com/CVPR2018_workshops/CVPR2018_W9.py")
    parser.add_argument("--target-dir", type=str, help="Directory where the files are written into", required=True)
    parser.add_argument("--delay", type=float, metavar="n", help="Wait n seconds after finishing a download to start a new one")
    args = parser.parse_args()
    pdf_list = get_pdf_list(args.base_url)
    for i in range_with_status(len(pdf_list)):
        time.sleep(0.5)
        dl_pdf(args.base_url, pdf_list[i], args.target_dir)
