# hidden.message.bot

- With the `/addtext` command, you send a message to the bot which will be stored in the postgreSQL database.
- With the `/text` command, you get a random message from the postgreSQL database.  

Is there any goal..? Not really! It's just fun to send some hidden notes to your friends and hope they will receive one of them one day!  

This bot aims at reamaining private with your friends. Feel free to use the code and create your own bot!  

Technologies used:  
- **Python3**
- **postgreSQL**
- **Heroku**, to deploy the service and get the bot up and running 24/7

# Repository structure

- `bot.py` is the core code
- `Procfile` it set to let Heroku know what will run the code
- `hidden.message.env` is the virtual environment to set up
- `requirements.txt` is gathering the required packages

# To properly set up a similar code

I gathered some notes and a process guide to set up a **Telegram Bot** with a PostgreSQL DB.  
[You can find the guide here]().  

 
