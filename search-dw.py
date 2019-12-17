import os
import argparse
import requests
from googlesearch import search
from urllib.parse import unquote
from urllib.error import HTTPError
from time import time

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
    # set file name and check ext
    fileNameRetrieved = j.split("/")
    fileName = unquote(fileNameRetrieved[len(fileNameRetrieved)-1])
    testExt = fileName[len(fileName)-4:len(fileName)]

    if testExt.lower() != "." + args.ext.lower():
        fileName += "." + args.ext.lower()

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
i = 0
start = time()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

print()
print("Downloading file...")
print()

try:
    for j in search(query, tld="com", num=args.page, stop=args.result, pause=10.0):
        # Ignore bad request and move on
        try:
            r = requests.get(j, timeout=5, headers=headers)
            # Get file size of file retrieved
            size = int(r.headers['Content-length'])/1000000
            # Download only file > 0.5 MB
            if (size > 0.5):
                i += 1
                fileN = setFileName(j)
                print(i, fileN, str(round(size, 1)) + " MB")
                with open(fileN, "wb") as f:
                    f.write(r.content)
        except:
            pass
except HTTPError as e:
    print("Houston we've got a problem!!!")
    print(e.headers)
print()
print(f"Time to download: {time() - start}")
