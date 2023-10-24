# -*- coding: utf-8 -*-
"""
====
Custom networking functions
====

Mostly customized http request for now
"""

import platform
import socket
from bs4 import BeautifulSoup
import requests
import shutil

# set timeout to 10 seconds
socket.setdefaulttimeout(10)

# Create our own User-Agent string. We may need to fake this if a server tryes
# to mess with us.
user_agent = f'Mozilla/5.0 compatible ({platform.system()} {platform.machine()}; Novel-Indexer-Bot)'

#Start building our session
session = requests.session()
session.headers.update({'user-agent': user_agent})

# Provide a function to replace the default User-Agent:
def set_user_agent(agent: str):
    """Function to replace the default User-Agent"""
    session.headers.update({"user-agent": agent})


def quote(url):
    """ Quote a URL to ensure compatibility with unusual caracters in them.

    Added for Wattpad2Epub"""
    parts = url.rsplit('/', 1)
    url = f"{parts[0]}/{requests.utils.quote(parts[1])}"
    return url


def get_url(url):
    tryes = 5
    with session as s:
        while tryes > 0:
            try:
                response = s.get(quote(url))
                break
            except socket.timeout:
                tryes -= 1
            else:
                raise SystemExit("An URL error happened: --")
        html = response.text
        # with open('htmllog.txt', 'w') as file:
        #     file.write(html)
    return html

def get_binary(url, file):
    tryes = 5
    while tryes > 0:
        try:
            response = requests.get(quote(url), stream=True, timeout=500)
            if response.status_code == 200:
                response.raw.decode_content = True
                with open(file, 'wb') as f:
                    shutil.copyfileobj(response.raw, f)
            return True
        except socket.timeout:
            tryes -= 1
        else:
            raise SystemExit('Something went really wrong')
            return False


def get_soup(url):
    html = get_url(url)
    soup = BeautifulSoup(html, 'lxml')
    return soup
