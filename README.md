# cloudRobot - Telegram Cloud Storage Bot
This bot provides an interface for a cloud for Telegram messages, such as pictures, videos or text messages from users.

# How to setup:

**First clone the Repo with git**

```git clone https://github.com/typetg/cloudRobot```

**Change the directory to cloudRobot**

```cd cloudRobot```

**Edit the config.ini file with your Variables**

```nano config.ini```

**Install the requirements.txt**

```pip3 install -r requirements.txt```

**Start the Bot**

```python3 cloudbot.py```

# Variables:
- **Telegram Api ID & Hash**: Get it from my.telegram.org
- **Bot-Token**: Create a new Bot at @botfather
- **Database-Channel**: Create a super group you like by making the chat history visible and invite @missrose_bot and your cloudRobot.
Then write /id and remove Rose again afterwards. The channel ID should be in this format: -100xxx
- **Admins**: Users who are allowed to use this cloudRobot. Please write the user IDs separated with spaces in this format: "11272378 2711717 16162662"

# Commands:
- **/start**: send a control Panel
- **/addfolder {FOLDERNAME}**:  create a new folder
- **/rename MSGID;NEW TITLE**: rename a file
