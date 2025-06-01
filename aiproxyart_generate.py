import requests
import json
import os
from configs import system_messages, general_config
from datetime import datetime

#ollama requests api
def generate_response(characterfirstname):

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
    system_context = [
        {
            "role": "system",
            "content": "Maintain a friendly and enthusiastic tone, suitable for engaging with the Magic the Gathering community."
        },
        {
            "role": "system",
            "content": "Do not try and format your tweets with markup"
        }     
    ]
    user_message = [
        {
            "role": "system",
            "content": "You are tweeting about AIProxyArt, an online shop that makes and sells custom Magic the Gathering proxies on MTGEtsy. Your goal is to generate engaging and promotional tweets for your followers."
        },
                {
            "role": "system",
            "content": "AIProxyArt currently sells the following products: {}".format(general_config.products)
        },
        {
            "role": "system",
            "content": "The shop url is: {}".format(general_config.etsy_shop_url)
        },
        {
            "role": "user",
            "content": """Imagine you are your character and sending a tweet. 
            Generate a new short tweet in charactrer. 
            Only use provided examples as a guide, do not copy them!
            Dont tell people who you are, they already know that from your profile. 
            Incorporate relevant hashtags such as #MTG, #MagicTheGathering or #CustomProxiesto increase visibility."""
        }
    ]   

    messages = system_context 
    messages = system_context + system_messages.general_context + system_messages.character_context[characterfirstname] + memories + user_message
    messages = system_context + system_messages.general_context + system_messages.character_context[characterfirstname] + user_message
    for message in messages:
        #print(message['content'])
        pass

    url = general_config.ollama_host

    headers = {
        'Content-Type': "application/json",
    }

    modeldata = {
        "model": "dolphin-llama3:8b",
        "messages": messages,
        "stream": False,
        "keep_alive": "5m",
        "temperature": 0.8,
        "max_tokens": 60,
        "top_p": 0.9,
        "frequency_penalty": 0.8,
        "presence_penalty": 0.3
    }
    tweetlen = 281
    while tweetlen > 280:

        response = requests.post(url, headers=headers, data=json.dumps(modeldata))

        if response.status_code == 200:
            response_text = response.text
            data = json.loads(response_text)
            actual_response = data['message']['content']
            #if actual_response starts with a " and ends with a " remove them
            if actual_response.startswith('"') and actual_response.endswith('"'):
                actual_response = actual_response[1:-1]
            tweetlen = len(actual_response)
            if tweetlen > 280:
                print( len(actual_response))
                continue
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
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
if __name__ == "__main__":
    clear_screen()
    message = generate_response('megan')
    print(message)
    print('Message Length',len(message))