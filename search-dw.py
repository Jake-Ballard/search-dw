# What is: search-dw is a Python utility to automate "search and download" via google search.
#
# Keep UP2Date here: https://github.com/Jake-Ballard/search-dw.git


import os
import re
import requests
import logging
import argparse
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import unquote

l = logging.getLogger()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def msg():
    return '''search-dw.py
          -s or --search,               What to search...
          -e or --ext,                  Filetype of searched file
          -d or --dw        [optional], Download directory
          -l or --log       [optional], Log directory
          -r or --result    [optional], Result limit
         Example:
            1. python3 search-dw.py -s "Ruby doc" -e pdf
            2. python3 search-dw.py -s "Security Workshop" -e ppt -r 5
         '''


def start_log(log_dir):
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s')

    vh = logging.StreamHandler()
    vh.setFormatter(formatter)
    log.addHandler(vh)

    logfile = datetime.now().strftime(log_dir+'/logfile_%H_%M_%d_%m_%Y.log')

    fh = logging.FileHandler(logfile)
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s')
    fh.setFormatter(formatter)

    log.addHandler(fh)

    return log


def setDirectory(dw_dir, log_dir):
    try:
        os.mkdir(dw_dir)
        os.mkdir(log_dir)
    except FileExistsError:
        pass


def setFileName(r, ext):

    tmp_filename = r.split("/")
    tmp_filename = unquote(tmp_filename[-1])

    fileName = "".join(re.findall("[a-zA-Z]+", tmp_filename[:-4]))
    fileName += "." + ext.lower()
    return fileName


def saveRes(list, res, dw, ext):

    path = os.path.abspath(os.curdir) + "/" + dw
    l.info("Trying to get %d file in %s ..." % (res, path))

    os.chdir(dw)

    d_count = 1

    for i in range(res):
        j_master = list[i].get('href').replace('/url?q=', '').split("&")
        j = j_master[0]
        # discarding bad url & bad size (<100Kb)
        if ((j[0:4] == "http") and (j[-3:] == ext)):
            try:
                r = requests.get(j, stream=True, headers=HEADERS)
                size = int(r.headers['Content-length'])
                if (size > 100000):
                    l.info("***** file nr. %d *****" % d_count)
                    l.info("Downloading file: %s " % j)
                    fileN = setFileName(j, ext)
                    with open(fileN, "wb") as f:
                        f.write(r.content)
                        l.info("File %s downloaded correctly" % fileN)
                    d_count += 1
            except Exception as e:
                pass
    l.info("Downloaded %d of %d file searched" % (d_count, res))


def getGoogleRes(query, directory, result, ext):

    l.info("Executing Google query...")
    q = '+'.join(query.split())

    url = 'https://google.com/search?q=' + q

    l.info("Query is: %s", url)
    res = requests.get(url, stream=True)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, 'html.parser')

    l_list = soup.select('div#main > div > div > div > a')
    n_res = min(result, len(l_list))

    return saveRes(l_list, n_res, directory, ext)


def execute(query, directory, ext, result):

    l.info("Program started...")
    n = "&num="+str(result)
    query += "+filetype:" + ext + n

    getGoogleRes(query, directory, result, ext)

    l.info("Finished")


def main():
    p = argparse.ArgumentParser(usage=msg())
    p.add_argument('-s', '--search', type=str, required=True)
    p.add_argument('-e', '--ext', type=str, required=True)
    p.add_argument('-d', '--dw', type=str, default='dw')
    p.add_argument('-l', '--log', type=str, default='log')
    p.add_argument('-r', '--result', type=int,
                   default=20, choices=range(1, 90))
    args = p.parse_args()

    a_s = args.search
    a_e = args.ext
    a_d = args.dw
    a_l = args.log
    a_r = args.result

    setDirectory(a_d, a_l)

    l = start_log(args.log)
    l.info("Reading arguments...")

    execute(a_s, a_d, a_e, a_r)


if __name__ == '__main__':
    main()
