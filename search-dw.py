import os
import argparse
import requests
from googlesearch import search
from urllib.parse import unquote
from time import time

# Check arguments from command line customizing msg


def msg(name=None):
    return '''search-dw.py
          -s or --search,             What to search...
          -e or --ext,                Filetype of searched file
          -p or --page   [optional],  Number of google page to consider
          -r or --result [optional],  Result limit
         
         Example:
            1. python3 search-dw.py -s "Ruby doc" -e pdf
            2. puthon3 search-dw.py -s forking -e ppt -p 10 -r 5 
         '''


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

# move in download dir
os.chdir(dirName)

# Set counter & monitor time exec
start = time()

print()
print("Downloading file from...")

for i, j in enumerate(search(query, tld="com", num=args.page, stop=args.result, pause=10.0,), 1):
    print(i, unquote(j))
    # ignore bad request
    try:
        r = requests.get(j, timeout=5)
    except:
        pass
    # set file name and check ext
    fileNameRetrieved = j.split("/")
    fileName = unquote(fileNameRetrieved[len(fileNameRetrieved)-1])
    testExt = fileName[len(fileName)-4:len(fileName)]

    # download file and ignore errors
    try:
        if testExt.lower() != "." + args.ext.lower():
            fileName += "." + args.ext.lower()
        with open(fileName, "wb") as f:
            f.write(r.content)
    except:
        pass
print()
print(f"Time to download: {time() - start}")
