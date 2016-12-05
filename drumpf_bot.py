#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Author: Ting'''
import logging
import traceback
from pprint import pprint
from subprocess import call
import re
from collections import defaultdict
from os.path import join, abspath, dirname, isfile
import csv
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
from tweet_config import CONFIG
from time import sleep
import __builtin__


def main():
	try:
		OAUTH_TOKEN = CONFIG.get('OAUTH_TOKEN')
		OAUTH_SECRET = CONFIG.get('OAUTH_SECRET')
		CONSUMER_KEY = CONFIG.get('CONSUMER_KEY')
		CONSUMER_SECRET = CONFIG.get('CONSUMER_SECRET')
		TWITTER_HANDLE = CONFIG.get('TWITTER_HANDLE')
		
		auth = OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

		t = Twitter(auth=auth)

		# twitter_userstream = TwitterStream(auth=auth, domain='userstream.twitter.com')

		# Initialize the tweet
		tweets = None
		while True:
			old_tweets = tweets
			tweets = get_tweet(t)[0]
			if tweets.get('status').get('text') != old_tweets:
				updated_text = process_text(tweets) 
				send_tweet(t, updated_text)
				tweets = tweets.get('status').get('text')
			# To prevent abuse of the twitter API and usage limit, calling it only once a minute.
	 		sleep(60)

	except Exception as e:
		print(e)


def get_tweet(t):
	#Fetch the latest tweet about Donald Trump
	users = t.users.search(q='realDonaldTrump', count=1)
	return users


def send_tweet(t, text):
	#This is the part which actually posts the tweet
	if len(text)<=140:
		#Twitter allows only 140 character tweets
		print('tweetable')

		# Check the lateast tweet to avoid deplicate
		my_last_tweet = t.users.search(q='reelDonaldDump', count=1)[0].get('status').get('text')
		if my_last_tweet == text:
			return

		text = text.replace('amp;', '')

		t.statuses.update(status=text)
	else:
		print('140 characters crossed')


def process_text(statement): 
	text = str(statement['status']['text'].encode("utf-8"))
	tweet_time = str(statement['status']['created_at'])
	print('Tweet Content: ' + text + ' at ' + tweet_time)
	handle = 'realDonaldTrump'  # str(statement['screen_name'])

	# ###
	# text_ls = text.split('')
	# for idx, word in text_ls: 
	# 	# Check word meaning from dictionary

	# 	# Check if phrase/name
	# 	if text_ls(idx).type == text_ls(idx + 1).type: 
	# 		print 'They are the same word type'
	# 	elif text_ls(word_index).type == 'adj':
	# 		text.replace(text_ls(idx), text_ls(word_index).antonym)


	if len(text) + len(handle) + 1 < 140: 
		updated_text = '@' + handle + ' ' + text
	else:
		updated_text = text
	print('Updated Tweet Content: ' + updated_text)

	return updated_text 


if __name__ == '__main__':
	main()


# Reference: 
# https://github.com/sixohsix/twitter/
# https://github.com/ckoepp/TwitterSearch/blob/master/TwitterSearch/TwitterUserOrder.py
# https://github.com/ideoforms/python-twitter-examples/blob/master/twitter-user-search.py
# http://stackoverflow.com/questions/4698493/can-i-add-custom-methods-attributes-to-built-in-python-types