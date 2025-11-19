# discord-chat-exporter |EDUCATIONAL PURPOSES ONLY|

This is a small tool that exports any Discord chat you choose.  
It saves all messages, usernames, timestamps, and every attachment in the channel.

pick a channel ID, export everything, and keep a clean backup of the conversation.

( you get channel id by right clicking someones chat or a channel and pressing copy. )

## What it does

- exports all messages in order  
- saves them into `chat.txt`  
- downloads all attachments into a folder called `attachments`  
- creates a separate folder for each chat you export  
- works on DMs and server channels  
- simple and clean console output

Everything gets saved inside the `text/` folder.

## Requirements

- Python 3  
- `pip install discord aiohttp python-dotenv`

You’ll need a Discord `USER` token Not Bot token in a `.env` file: TOKEN=<urtoken>

## Usage

Run the script: python exporter.py

Enter a channel ID when it asks.



