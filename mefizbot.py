#!/usr/bin/env python

import requests
from textwrap import fill
import zephyr
from time import sleep
from bs4 import BeautifulSoup
URL = "http://www.metafilter.com/161293/100-days"
CLASS = "mefi-auto"
INSTANCE = "100-days"
SENDER = "mefibot"

res = None
comment_count = 2469

zephyr.init()

while True:
    sleep(1)
    try:
        res = requests.get(URL)
        parsed = BeautifulSoup(res.content, 'html.parser')
        comments = parsed.findAll("div", "comments")[:-1]

        print "Got %d/%d comments" % (comment_count, len(comments))

        if comment_count == len(comments):
            continue

        new_comments = comments[comment_count:]
        for comment in new_comments:
            print "****"
            ct = comment.text
            commentmsg = fill(ct[:ct.rfind("posted by")])
            commenter = ct[ct.rfind("posted by")+9:ct.rfind(' at')]
            message = "%s\n --%s" % (commentmsg, commenter)
            m = zephyr.ZNotice(message=message, cls=CLASS, sender=SENDER, \
                               instance=INSTANCE)
            m.send()
        comment_count = len(comments)
    except Exception as e:
        print e, e.message

