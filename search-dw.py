import os
import argparse
import requests
from googlesearch import search
from urllib.parse import unquote
from time import time


# Check arguments from command line
s_desc = "What to search (keyword)"
e_desc = "Filetype of searched file (pdf or ppt or ...)"
p_desc = "Number of google page to consider (10 or 20 or ...)"
r_desc = "Result limit (10 or 30 or ...)"

p = argparse.ArgumentParser()

p.add_argument('-s', '--search', type=str, help=s_desc, required=True)
p.add_argument('-e', '--ext', type=str, help=e_desc,  required=True)
p.add_argument('-p', '--page', type=int, default=10, help=p_desc)
p.add_argument('-r', '--result', type=int, default=20,     help=r_desc)

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

print("[n]", "[Downloading file from...]")
print("-"*100)

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
print("-"*100)
print(f"Time to download: {time() - start}")
