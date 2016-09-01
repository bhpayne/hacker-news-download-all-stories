# https://github.com/minimaxir/hacker-news-download-all-stories/blob/master/hacker_news_getallstories.py

import urllib2
import json
import datetime
import time
import pytz
import pandas as pd
from pandas import DataFrame

ts = str(int(time.time()))
df = DataFrame()
hitsPerPage = 1000
num_comments_threshold=3

# https://hn.algolia.com/api
requested_keys = ["title","url","points","num_comments","author","created_at_i","objectID"]

count=0
#while True:
while (count<10):
	try:
#		url = 'https://hn.algolia.com/api/v1/search_by_date?tags=story&hitsPerPage=%s&numericFilters=created_at_i<%s' % (hitsPerPage, ts)
		url = 'https://hn.algolia.com/api/v1/search_by_date?tags=story&hitsPerPage=%s&numericFilters=created_at_i<%s&numericFilters=num_comments<%s' % (hitsPerPage, ts, num_comments_threshold)
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		data = json.loads(response.read())
		last = data["nbHits"] < hitsPerPage
		data = DataFrame(data["hits"])[requested_keys]
		df = df.append(data,ignore_index=True)
		ts = data.created_at_i.min()
		print count
		if (last):
			break
		time.sleep(3.6)
		count += 1
		

	except Exception, e:
		print e

df["title"] = df["title"].map(lambda x: x.translate(dict.fromkeys([0x201c, 0x201d, 0x2011, 0x2013, 0x2014, 0x2018, 0x2019, 0x2026, 0x2032])).encode('utf-8').replace(',',''))
df["created_at"] = df["created_at_i"].map(lambda x: datetime.datetime.fromtimestamp(int(x), tz=pytz.timezone('America/New_York')).strftime('%Y-%m-%d %H:%M:%S'))

ordered_df = df[["title","url","points","num_comments","author","created_at","objectID"]]

ordered_df.to_csv("hacker_news_stories.csv",encoding='utf-8', index=False)
