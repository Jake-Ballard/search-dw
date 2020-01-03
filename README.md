# What is
**search-dw** is a Python utility to automate "search and download" via google search.
	
## Getting Started
To run this script, you need to have **Python3 installed** on your system. 

### Prerequisite
The following pip are needed.
```
$ pip3 install bs4

$ pip3 install requests

$ pip3 install urllib3

```
### Download
Download project from GitHub.
```
git clone https://github.com/Jake-Ballard/search-dw.git && cd search-dw
```

### Usage 
```
$ python3 search-dw.py 
usage: search-dw.py
          -s or --search,               What to search...
          -e or --ext,                  Filetype of searched file
          -d or --dw        [optional], Download directory
          -l or --log       [optional], Log directory
          -r or --result    [optional], Result limit
         Example:
            1. python3 search-dw.py -s "Ruby doc" -e pdf
            2. python3 search-dw.py -s "Security Workshop" -e ppt -r 5
```

**Note:** The following [extensions](https://support.google.com/webmasters/answer/35287?hl=en) are available

### Examples
Here you are some examples that shows you how to search and download somenthing based on one or more keywords.

#### Nr. 1
In this example we are looking for some file with the keywords **debian official** and file extension **pdf** and we want to limit result to **3**.
```
$ python3 search-dw.py -s "debian official" -e pdf -r 3

```

#### Nr. 2
In this example we are looking for some file with the keywords **vim tutorial** and file extension **pdf** and we want to limit result to **5**.
```
$ python3 search-dw.py -s "vim tutorial" -e pdf -r 5

```

## Feedback

Your suggestions are kindly [welcome](https://github.com/Jake-Ballard/search-dw/issues)!

## Warning

Use the **search-dw.py** script at your own risk.  

