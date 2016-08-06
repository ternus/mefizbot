#!/usr/bin/env python

import requests
from textwrap import fill
import zephyr
from time import sleep
from bs4 import BeautifulSoup
URL = "http://www.metafilter.com/161394/Here-at-our-sea-washed-sunset-gates-shall-stand-A-mighty-woman"
CLASS = "mefi-auto"
INSTANCE = "live-thread"
SENDER = "mefibot"
SAFETY_FACTOR = 10

res = None
comment_count = 0

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
        if len(new_comments) > SAFETY_FACTOR:
            print "Skipping ahead %d" % (len(new_comments))
            comment_count = len(comments)
            continue

        for comment in new_comments:
            ct = comment.text
            commentmsg = fill(ct[:ct.rfind("posted by")])
            commenter = ct[ct.rfind("posted by") + 9:ct.rfind(' at')].strip()
            print "**** %s: %s..." % (commenter, commentmsg[:60])
            m = zephyr.ZNotice(
                fields=[URL, commentmsg], cls=CLASS, sender=commenter,
                               instance=INSTANCE)
            m.send()
        comment_count = len(comments)
    except Exception as e:
        print repr(e)
        comment_count += 1
