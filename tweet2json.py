#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from requests_oauthlib import OAuth1
import json

from datetime import datetime as dt

datetime = dt.now()
datetimestr = datetime.strftime('%Y%m%d%H%M%S')

f = open('tweet_'+datetimestr+'.log', 'w')

api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_secret = "YOUR_ACCESS_SECRET"

url = "https://stream.twitter.com/1.1/statuses/sample.json"
auth = OAuth1(api_key, api_secret, access_token, access_secret)
r = requests.post(url, auth=auth, stream=True)

import sys

j = 0
i = 0
for line in r.iter_lines():
    j = j+1
    # limit 10000 tweet
    if i > 10000:
        sys.exit()
    if line == '':
        continue
    data = json.loads(line)
    lang = data.get('lang')
    # select japanese lang
    if  lang == 'ja':
        print i,"/10000 all:",j
        i=i+1
        tweet = data.get('text')
        tweet = tweet.replace('\n','')
        timestamp = data.get('timestamp_ms')
        user = data.get('user')
        entities = data.get('entities')
        hashtags = []
        for hashtag in entities.get('hashtags'):
            # print hashtag
            hashtags.append(hashtag.get("text"))

        name = user.get("name")
        screen_name = user.get("screen_name")

        line = '{"timestamp":"'+timestamp +'","name":"'+name + '","screen_name":"'+screen_name+'","tweet":"'+tweet
        if len(hashtags) > 0:
            line = line +',"hashtags":'+ json.dumps(hashtags)+'}'
        else:
            line = line + '"}'

        f.write(line.encode('utf-8')+"\n")