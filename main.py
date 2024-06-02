import os
import ai_generate
import tweeter
import sys
from configs.system_messages import character_twitter_handles

def main():
    #change directory to the current file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # get character name from the env args
    character = sys.argv[1].lower()

    if character == 'jim':
        character = 'Jim Halpert from The Office'
        characterfirstname = 'jim'
    elif character == 'michael':
        character = 'Michael Scott from The Office'
        characterfirstname = 'michael'
    elif character == 'pam':
        character = 'Pam Beasley from The Office'
        characterfirstname = 'pam'
    elif character == 'stanley':
        character = 'Stanley Hudson from The Office'
        characterfirstname = 'stanley'
    elif character == 'dwight':
        character = 'Dwight Schrute from The Office'
        characterfirstname = 'dwight'
    else:
        print('Invalid character')
        return

    # generate a response
    tweet = ai_generate.generate_response(character, characterfirstname)
    # send the tweet
    print()
    print(characterfirstname)
    print(tweet)
    print()

    response = tweeter.send_tweet(characterfirstname, tweet)

    tweetid = response[0]['id']
    # if the text if the tweet montions another character, then generate a response for that character
    for value in character_twitter_handles:
        if value.lower() in tweet.lower() or character_twitter_handles[value].lower() in tweet.lower():
            tweet = ai_generate.generate_response(value+' from The Office', value.lower(),original_tweet=tweet,original_tweet_from=characterfirstname)
            print()
            print(value)
            print('Responding to:',characterfirstname)
            print(tweet)
            print()
            response = tweeter.send_tweet(value.lower(), tweet,responding_to=tweetid)
            break

if __name__ == '__main__':
    main()