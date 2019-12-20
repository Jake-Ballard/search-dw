# What is: search-dw is a Python utility to automate "search and download" via google search.
#
# Keep UP2Date here: https://github.com/Jake-Ballard/search-dw.git

import os
import re
import argparse
import requests
from time import time
from clint.textui import progress
from googlesearch import search
from urllib.parse import unquote
from urllib.error import HTTPError


# Custom message from argparse

def msg(name=None):
    return '''search-dw.py
          -s or --search,             What to search...
          -e or --ext,                Filetype of searched file
          -p or --page   [optional],  Number of google page to consider
          -r or --result [optional],  Result limit
         Example:
            1. python3 search-dw.py -s "Ruby doc" -e pdf
            2. python3 search-dw.py -s "Security Workshop" -e ppt -p 10 -r 5
         '''

# Set file name based on url retrived


def setFileName(j):
    # set file name and prepare ext
    t_fileName = j.split("/")
    t_fileName = unquote(t_fileName[-1])
    ext = t_fileName[-4:]

    # clean file name
    fileName = "".join(re.findall("[a-zA-Z]+", t_fileName[:-4]))
    fileName += args.ext.lower()

    return fileName


# Manage argument from command line
p = argparse.ArgumentParser(usage=msg())

p.add_argument('-s', '--search', type=str, required=True)
p.add_argument('-e', '--ext', type=str, required=True)
p.add_argument('-p', '--page', type=int, default=10)
p.add_argument('-r', '--result', type=int, default=20)

args = p.parse_args()

# Set Google Query
query = args.search + " filetype:" + args.ext

# Set downlod directory
dirName = "dw"

# Skip if exist
try:
    os.mkdir(dirName)
except:
    pass

# Move in download dir
os.chdir(dirName)

# Set counter & monitor time exec & prepare header
i, t = 0, time()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

sdsc = "\nDownloading of << " + args.search + " >> is started. Be patient :-)\n"

print(sdsc)

try:
    for j in search(query, tld="com", num=args.page, stop=args.result, pause=20.0,  user_agent=headers['User-Agent']):
        # Ignore bad request and move on
        try:
            r = requests.get(j, timeout=5, headers=headers)
            # Get file size of file retrieved
            size = int(r.headers['Content-length'])
            # Download only file > 100 KB
            if (size > 100000):
                fileN = setFileName(j)
                with open(fileN, "wb") as f:
                    for bar in progress.bar(r.iter_content(chunk_size=1024), expected_size=(size/1024) + 1, label=fileN + " - "):
                        if bar:
                            f.write(bar)
                            f.flush()
                i += 1
        except:
            pass

    # Prepare statistics
    f_dw = "file" if i == 1 else "files"
    print(f"\nDownloaded {i} {f_dw} in {time() - t} seconds\n")

except HTTPError as e:
    print("Houston, we've got a problem!!!\n")
    if (e.getcode() == 429):
        print("Stop now!!!\nToo many requests, wait and retry later!\n")
    else:
        print(e)
