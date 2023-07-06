## Prerequisites

[![Code](https://img.shields.io/badge/Code-Python-1B9D73?style=flat&logo=python)](https://python.org)
[![Framework](https://img.shields.io/badge/Framework-Flask-1B9D73?style=flat&logo=flask)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Database-supabase-brightgreen?logo=supabase)](https://supabase.com/)
[![PyhtonAnywhere](https://img.shields.io/badge/Server-PythonAnywhere-green?logo=amazonaws)](https://www.pythonanywhere.com/)
[![Chatbot](https://img.shields.io/badge/Chatbot-OpenAI-lime?logo=openai)](https://openai.com/product)

## Very Initial Steps
1. Install Telegram :)
2. Create a telegram bot by talking to [Bot Father](https://t.me/botfather)
3. Create ChatGPT API Token in [Open AI](https://openai.com/blog/openai-api)
4. Install python in your computer, if you are on windows follow [this](https://www.python.org/downloads/windows/)
5. Install git, follow [this](https://git-scm.com/download/win)
6. Install editor of your choice, I preffer [VSCode]([https://atom.io](https://code.visualstudio.com/))

### Step 0:

- Just git clone this repository and start working by editing the code
   ```shell
   git clone https://github.com/Elizraa/bot-telegram.git
   cd bot-telegram
   ```
### Step 1:
1. Create your virutalenv from terminal `python3 -m venv venv`
2. Activate with `venv\Scripts\activate`
3. Install library `pip install -rrequirements.txt`

### Step 2:
1. Change API Token and Other Variable: 
   ```shell
    url = "YOUR_SUPABASE_URL"
    key = "YOUR_SUPABASE_KEY"
    secret = "YOUR_SECRET_TOKEN"
    bot = telepot.Bot("YOUR_TELEGRAM_BOT_TOKEN")
    bot.setWebhook("YOUR_WEBHOOK".format(secret), max_connections=1)
    openai.api_key = "YOUR_OPENAI_API_KEY"
   ```
