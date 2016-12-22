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
from wordict import define_word


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
				if updated_text is not None: 
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
		try:
			my_last_tweet = t.users.search(q='reelDonaldDump', count=1)[0].get('status').get('text')
			if my_last_tweet == text:
				print('Content has been tweeted previously, tweet passed.')
				return
		except Exception as e: 
			print e

		text = text.replace('amp;', '')

		t.statuses.update(status=text)
	else:
		print('140 characters crossed')


def process_text(statement): 
	text = str(statement['status']['text'].encode("utf-8"))
	tweet_time = str(statement['status']['created_at'])
	print('Tweet Content: ' + text + ' at ' + tweet_time)
	handle = 'realDonaldTrump'  # str(statement['screen_name'])

	# Examine the meaning of the tweet 
	# Split the tweet into list of words separeted by space 
	try: 
		updated_text = text.split('....cont')[0]
		text_ls = updated_text.split()

		# For each word and its respective position in the tweet 
		for word in text_ls: 
			# if 'adjective' in word_lookup.define_word(word).pos:
			# 	text.replace(word, word_lookup.define_word(word).atns[0])
			specific_word = False 	
			for letter in list(word): 
				if letter.isupper(): 
					specific_word = True 

			if define_word(word) and not specific_word: 
				print word, define_word(word)
				updated_text = updated_text.replace(word, define_word(word))

	except Exception as e: 
		print e
		return

	print('Proposed Tweet Content: ' + updated_text)
	print('Proposed Tweet Length: ' + str(len(updated_text)))

	if len(updated_text) + len(handle) + 1 < 140: 
		updated_text = '@' + handle + ' ' + updated_text
		print('Tagged original handler.')
	elif len(updated_text) < 140: 
		pass
	else:
		return
		# updated_text = text

	return updated_text 


if __name__ == '__main__':
	main()


# Reference: 
# https://github.com/sixohsix/twitter/
# https://github.com/ckoepp/TwitterSearch/blob/master/TwitterSearch/TwitterUserOrder.py
# https://github.com/ideoforms/python-twitter-examples/blob/master/twitter-user-search.py
# http://stackoverflow.com/questions/4698493/can-i-add-custom-methods-attributes-to-built-in-python-types
# http://stackoverflow.com/questions/17140408/if-statement-to-check-whether-a-string-has-a-capital-letter-a-lower-case-letter