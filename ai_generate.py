import requests
import json
import os
from configs import system_messages, general_config
from datetime import datetime

#ollama requests api
def generate_response(character,characterfirstname,original_tweet=None,original_tweet_from=None):

    


    system_context = [
    {
        "role": "system",
        "content": "Your character is: {}. Stay true to this character's personality, including speech patterns and mannerisms.".format(character)
    },
    {
        "role": "system",
        "content": "Stay true to {}'s personality, including speech patterns, mannerisms, and typical content. Do not break character.".format(characterfirstname)
    }
    ]

    twitter_handles = ''
    for key in system_messages.character_twitter_handles:
        twitter_handles += key + ' is ' + system_messages.character_twitter_handles[key] + ', '
    if original_tweet is not None:
        user_message = [
            {
                "role": "user",
                "content": """You just received a tweet from {}. Respond to this tweet as {}. 
                Keep it to 280 characters or less. If you mention any other character in this list use their twitter handle: {}. 
                The tweet you are responding to is: {}""".format(original_tweet_from,character,system_messages.character_twitter_handles,original_tweet)
            }
        ]
        
    else:
        user_message = [
            {
                "role": "user",
                "content": """Generate a new short tweet as {}. Focus your tweets on the day-to-day happenings and routine activities of {}. 
                Share small, everyday moments and thoughts that reflect their typical day. Keep it to 280 characters or less.
                Today is {} {}
                if you mention any other character in this list use their twitter handle: {}.
                """.format(character,characterfirstname,datetime.now().strftime("%A"),str(datetime.now()),system_messages.character_twitter_handles)
            }
        ]

    print(user_message)
    

    

    chatid = characterfirstname+'_memory'


    # for each unique chatid we will create a json file with the chat history
    # if it already exists we will append to it
    # if it doesn't exist we will create it
    #each message will have a new line


    if os.path.exists('memories/'+chatid + '.json'):
        with open('memories/'+chatid + '.json', 'r') as f:
            data = json.load(f)
        with open('memories/'+chatid + '.json', 'w') as f:
            json.dump(data, f)
    else:
        data = {'messages': []}
        with open('memories/'+chatid + '.json', 'w') as f:
            json.dump(data, f)


    
    # read  the json file messages to a list
    with open('memories/'+chatid + '.json', 'r') as f:
        data = json.load(f)
        memories = data['messages']

    # add the system context to the messages

    messages = system_context + system_messages.general_context + system_messages.character_context[characterfirstname] + memories + user_message

    for message in messages:
        #print(message['content'])
        pass

    url = general_config.ollama_host

    headers = {
        'Content-Type': "application/json",
    }

    data = {
        "model": "command-r:latest",
        "messages": messages,
        "stream": False
    }
    tweetlen = 281
    while tweetlen > 280:
        print('tweet is too long...retrying')

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            response_text = response.text
            data = json.loads(response_text)
            actual_response = data['message']['content']
            tweetlen = len(actual_response)
            if tweetlen > 280:
                continue
            # replace  character names in the response with the twitter handles
            for key in system_messages.character_twitter_handles:
                if characterfirstname == key.lower():
                    pass
                else:
                    pass
                    #actual_response = actual_response.replace(key, system_messages.character_twitter_handles[key])
            # write the response to the json file
            with open('memories/'+chatid + '.json', 'r') as f:
                chatdata = json.load(f)
                if len(actual_response) < 30 or len(actual_response) > 280:
                    pass
                else:
                    chatdata['messages'].append(data['message'])
            with open('memories/'+chatid + '.json', 'w') as f:
                json.dump(chatdata, f)
            return actual_response
        else:
            print("Error: ", response.status_code)
            print(response.text)
            return "Error"

if __name__ == "__main__":
    message = generate_response('Pam Beasley from The Office','pam')
    print(message)
    print('Message Length',len(message))