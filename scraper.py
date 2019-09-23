#!/usr/bin/env python

__author__ = "astephens91"

import argparse
import requests
import re
from bs4 import BeautifulSoup
from urlparse import urljoin


def url_content_parse(url):
    response = requests.get(url)

    results = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', response.content)

    soup = BeautifulSoup(response.content, features="html.parser")

    href = soup.find_all('a')
    href_abs = []

    for link in href:
        absolute_path = urljoin(url, link.get('href'))
        if absolute_path not in href_abs:
            href_abs.append(urljoin(url, str(link.get('href'))))

    img = soup.find_all('img')
    img_abs = []

    for link in img:
        absolute_path = urljoin(url, link.get('src'))
        if absolute_path not in img_abs:
            img_abs.append(urljoin(url, str(link.get('src'))))

    url_dict = {'urls': results, 'relative urls': href_abs + img_abs}

    return url_dict


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='Url to parse')

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    dictionary = url_content_parse(args.url)

    print("Urls scraped: {}, Relative Urls constructed: {}".format
          ("\n".join(dictionary['urls']), "\n".join
           (dictionary['relative urls'])))


if __name__ == '__main__':
    main()
