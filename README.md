# Roastmate
![image](https://github.com/sherifnada/roastmate/assets/6246757/a2e17fd3-bc42-428d-bb51-d67f65e73e5f)

_what are you looking at?_

## 1) What?
Roastmate is an iMessage chatbot that roasts you, your friends, and anyone who happened to be within line of sight of your phone screen. 

Stack: 
* Python
* Heroku for hosting
* Sendblue.co (for programmatically sending iMessage)
* ChatGPT

It was retired in October 2023 after a rapid decline in number of friends. 


## How did Roastmate work? 
The full flow is [here](https://github.com/sherifnada/roastmate/blob/master/ux-workflow.png) but the TL;DR is: 

1. When a new message is sent in a chat it's in, Roastmate had an N% chance of responding (best N we found was 10%)
2. If it's responding, it generates the response via [prompting ChatGPT](https://github.com/sherifnada/roastmate/blob/master/roastmate/prompts.py), including the last few messages from the text thread (this was created before the Assistants API came out so we had to manually hold on to chat history)

There are other details but that's pretty much the gist of it. 
