
# The Office Twitter Bot

This project is a Twitter bot that generates and posts tweets as characters from the TV show "The Office". It uses an AI model to generate the tweets and posts them using the Twitter API.

### Usage

The main script is `main.py`. It takes one argument, which is the name of the character you want to generate a tweet for. The options are `jim`, `michael`, `pam`, `stanley`, and `dwight`.

Example usage:
```bash
python main.py jim
```
This will generate a tweet as Jim Halpert from The Office.

### Files

- `main.py`: The main script that handles the generation and posting of tweets.
- `ai_generate.py`: Custom library for generating responses.
- `tweeter.py`: Custom library for interacting with the Twitter API.
- `general_config.py`: Configuration file containing general settings.
- `system_messages.py`: Script for handling system messages.
- `{character}_memory.json`: Memory file for the characters, containing stored messages. These will be generated by the script as its used.

### Character Memory

Memories from your characters will be stored in specific JSON files. For example, `pam_memory.json` stores Pam's memories. These files help the bot remember past interactions and generate more contextually accurate tweets.

Example content from `pam_memory.json`:
```json
{
  "messages": [
    {
      "role": "assistant",
      "content": "Just another day of doing some light gardening around the house. 🌱🏠 Couldn't help but think about my old Dunder Mifflin days though... remember when Jim and I had that super hilarious paper war with Dwight? Those were the days! 😂 @JmHalp #OfficeMemories"
    },
    {
      "role": "assistant",
      "content": "Cooking with Jim (@JmHalp) today! Making our famous chicken dance stir fry for dinner. It's becoming our Sunday tradition. 🍝🌶️ I love spending time in the kitchen with my favorite person! #Foodie #CoupleGoals"
    }
  ]
}
```

## Built With

- Python

## Authors

- Paul Giles


## Acknowledgments

- The creators of The Office for the inspiration
