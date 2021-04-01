# -*- coding: utf-8 -*-
"""
====
Custom networking functions
====

Mostly customized http request for now
"""


import urllib.request
import urllib.parse
import urllib.error
import socket
from bs4 import BeautifulSoup
import gzip
import brotli
from io import BytesIO
import platform


# set timeout to 10 seconds
socket.setdefaulttimeout(10)

# Create our own User-Agent string. We may need to fake this if a server tryes
# to mess with us.
USER_AGENT = 'Mozilla/5.0 compatible (' + platform.system() + ' ' + \
    platform.machine() + '; Novel-Indexer-Bot)'


# Provide a function to replace the default User-Agent:
def set_user_agent(agent):
    USERAGENT = agent


def get_url(url):
    tryes = 5
    response = None
    # Build our request
    request = urllib.request.Request(url)
    # Accept compressed content
    request.add_header('Accepting-encoding', 'gzip, br')
    # Use our custom User-Agent
    request.add_header('User-Agent', USER_AGENT)

    while tryes > 0:
        try:
            response = urllib.request.urlopen(url)
            break
        except socket.timeout:
            tryes -= 1
        except urllib.error.URLError as error:
            if isinstance(error.reason, socket.timeout):
                tryes -= 1
            else:
                print("Se produjo un error de url: -%s-" % error.reason)
                quit()

    encoding = response.info().get('Content-Encoding')
    if encoding == 'gzip':
        buffer = BufferIO(response.read())
        html = gzip.GzipFile(fileobj=buffer)
    elif encoding == 'br':
        # html = brotli.decompress(response.content)
        html = request.text
    else:
        html = response.read()
    response.close()
    return html

def get_soup(url):
    html = get_url(url)
    soup = BeautifulSoup(html, 'lxml')
    return soup
