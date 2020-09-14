import os, sys
from signal import signal, SIGPIPE, SIG_DFL

def fetch():

    """This small method first check if json file already exists.
       if so then file will be deleted. Then the method call the spider
       method and generate new json file 
    """

    if os.path.exists("ministers.json"):
        os.remove("ministers.json")
    os.popen('scrapy crawl parlament --set FEED_URI=ministers.json --set FEED_FORMAT=json')
    return "OK"


signal(SIGPIPE,SIG_DFL) 
fetch()