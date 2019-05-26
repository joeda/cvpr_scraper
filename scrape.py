#!/usr/bin/env python3

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import argparse

def get_pdf_list(baseurl):
    response = requests.get(baseurl)
    soup = BeautifulSoup(response.text, "html.parser")
    return [l["href"] for l in soup.find_all("a", text="pdf")]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url")
    args = parser.parse_args()
    pdf_list = get_pdf_list(args.base_url)
    print(pdf_list)