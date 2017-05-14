#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Author: Ting
Tweet grabber'''
import logging
import traceback
from pprint import pprint
from subprocess import call
import re
from collections import defaultdict
from os.path import join, abspath, dirname, isfile
import csv
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
from argparse import ArgumentParser
# from tweet_config import CONFIG
import imp
from time import sleep
from wordict import define_word
import psycopg2


log = logging.getLogger(name=__file__)

def main(CONFIG):
	try:
		OAUTH_TOKEN = CONFIG.get('OAUTH_TOKEN')
		OAUTH_SECRET = CONFIG.get('OAUTH_SECRET')
		CONSUMER_KEY = CONFIG.get('CONSUMER_KEY')
		CONSUMER_SECRET = CONFIG.get('CONSUMER_SECRET')
		TWITTER_HANDLE = CONFIG.get('TWITTER_HANDLE')
		
		auth = OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

		# twitter_userstream = TwitterStream(auth=auth, domain='userstream.twitter.com')

		t = Twitter(auth=auth)

		# Initialize the tweet
		tweets = None
		# db_info = CONFIG.get('db_info')
		# conn = psycopg2.connect(db_info)
		# cur = conn.cursor()
		while True:
			old_tweets = tweets
			tweets = t.users.search(q='realDonaldTrump', count=1)[0]
			print 'Latest tweet: ' + tweets.get('status').get('text')
			if tweets.get('status').get('text') != old_tweets:
				polarity = process_text(tweets, conn, cur) 
				print polarity
			tweets = tweets.get('status').get('text')
			# To prevent abuse of the twitter API and usage limit, calling it only once a minute.
			sleep(60)

		# cur.close()
		# conn.close()

	except Exception as e:
		print(e)


def process_text(statement, conn, cur): 
	text = str(statement['status']['text'].encode("utf-8"))

	# Examine the meaning of the tweet 
	# Split the tweet into list of words separeted by space 
	try: 
		updated_text = text.split('....cont')[0]
		text_ls = updated_text.split()

		# log_id = log_content(conn, cur, statement)
		# return analyze_text(log_id)
		return analyze_text(text_ls)

	except Exception as e: 
		print e
		return

	return updated_text 


def log_content(conn, cur, statement): 
	text = str(statement['status']['text'].encode("utf-8"))
	tweet_timestamp = str(statement['status']['created_at'])
	handle = str(statement['screen_name'])

	log_id = md5(handle+tweet_timestamp) 

	query = """INSERT {log_id}, {tweet_timestamp}, {handle}, {text}
			   INTO {table}""".format(log_id, text, tweet_timestamp, handle)

	try: 
		cur.execute(query)
		conn.commit()
	except Exception as e: 
		log.warning(e)

	return log_id


def analyze_text(text_ls):
	# For each word and its respective position in the tweet 
	for word in text_ls: 
		# if 'adjective' in word_lookup.define_word(word).pos:
		# 	text.replace(word, word_lookup.define_word(word).atns[0])

		if define_word(word): 
			word_polarity = define_word(word).polarity


if __name__ == '__main__':
	parser = ArgumentParser()
	parser.add_argument('--filepath', required=True, help="Config file path.")
	args, trash = parser.parse_known_args()

	try: 
		tweet_config = imp.load_source('CONFIG', args.filepath)
	except Exception as e: 
		print 'No CONFIG file found'

	main(tweet_config.CONFIG)
