# send tweets
import tweepy
import requests
import json
import os
from configs import twitter_details
from requests_oauthlib import OAuth1

def send_tweet(character, tweet,responding_to=None):
    # get the twitter auth details for the character
    consumer_key = twitter_details.twitter_auth[character]['api_key']
    consumer_secret = twitter_details.twitter_auth[character]['api_key_secret']
    access_token = twitter_details.twitter_auth[character]['access_token']
    access_token_secret = twitter_details.twitter_auth[character]['access_token_secret']
    bearer_token = twitter_details.twitter_auth[character]['bearer_token']


    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(
        access_token,
        access_token_secret,
    )
    # this is the syntax for twitter API 2.0. It uses the client credentials that we created
    newapi = tweepy.Client(
        bearer_token=bearer_token,
        access_token=access_token,
        access_token_secret=access_token_secret,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
    )

    # Create API object using the old twitter APIv1.1
    api = tweepy.API(auth)

    # send the tweet
    if responding_to is not None:
        response = newapi.create_tweet(text=tweet, in_reply_to_tweet_id=responding_to)
    else:
        response = newapi.create_tweet(text=tweet)
    return response

if __name__ == '__main__':    
    # test the function
    tweet = 'This is a test reply tweet'
    character = 'jim'
    #response = send_tweet(character, tweet, responding_to=1797374729852240304)


    