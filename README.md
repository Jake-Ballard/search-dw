# What is
**search-dw** is a Python utility to automate "search and download" via google search.
	
## Getting Started
To run this script, you need to have **Python3 installed** on your system. 

### Prerequisite
The following pip are needed.
```
$ pip3 install requests
$ pip3 install google
$ pip3 install urllib3

```
### Download
Download project from GitHub.
```
git clone https://github.com/Jake-Ballard/search-dw.git && cd search-dw
```

### Examples
Here you are some examples that shows you how to search and download somenthing based on one or more keywords.

#### Nr. 1
In this example we are looking for some file with the keywords **debian official** and file extension **pdf** and we want to limit result to **3** (leaving page parameter to default value, 10). We've got exactly 3 valid result. 
```
$ python3 search-dw.py -s "debian official" -e pdf -r 3

```
[![search-dw - example 1](https://github.com/Jake-Ballard/search-dw/blob/master/ex_1.PNG)](#features)

#### Nr. 2
In this example we are looking for some file with the keywords **vim tutorial** and file extension **pdf** and we want to limit result to **5** (leaving page parameter to default value, 10). Differently to the example nr. 1 we've got just 2 valid result. 
```
$ python3 search-dw.py -s "vim tutorial" -e pdf -r 5

```

[![search-dw - example 2](https://github.com/Jake-Ballard/search-dw/blob/master/ex_2.PNG)](#features)

## Feedback

Your suggestions are kindly [welcome](https://github.com/Jake-Ballard/search-dw/issues)!

## Warning

Use the **search-dw.py** script at your own risk.  


