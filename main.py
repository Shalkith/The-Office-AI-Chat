import os
import aiproxyart_generate
import tweeter
import sys
from configs.system_messages import character_twitter_handles
import random

def main():
    #change directory to the current file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # get character name from the env args
    character = sys.argv[1].lower()

    # generate a response
    tweet = aiproxyart_generate.generate_response(character)
    # send the tweet
    print()
    print(character)
    print(tweet)
    print()

    response = tweeter.send_tweet(character, tweet)




if __name__ == '__main__':
    main()