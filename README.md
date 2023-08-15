# django-telegram-bot

<p align="center">
    <img src="https://github.com/kartikmalhotra/telegram_ai_chat_bot/docs/photo-1690683790356-c1edb75e3df7.jpeg" align="center" height="350px" weight="350px">

    <img src="https://play-lh.googleusercontent.com/ZU9cSsyIJZo6Oy7HTHiEPwZg0m2Crep-d5ZrfajqtsH-qgUXSqKpNA2FpPDTn-7qA5Q=w480-h960" align="center" height="350px" weight="350px">

</p>

### Check the example bot that uses the code from Main branch: [BotMother](https://t.me/randombum_bot)

## Features

- Database: Postgres, Sqlite3, MySQL - you decide!
- Admin panel (thanks to [Django](<Domian>/admin)
- Telegram API usage webhook mode](https://core.telegram.org/bots/api#setwebhook)
- Create multiple avatars and connect them to Telegram Bot accounts
- User will receive messages from each avatar upto thrice a day. Same message to all users and at the same fixed time hardcoded using cron job
- User can control the frequencey of these stories by sending Telegram commands - /once-a-day /twice-a-day /thrice-a-day /no-updates
- Using ChatGPT API to respond based on the prompt controlled from Admin dashboard and the user messages
- Include the last few messages in the context to ChatGPT
- User should purchase credits for the Bot to respond to their messages
- Each user message will consume 1 credit and the credits will be per user-bot combo. User cannot share their credits across bots
- Credits will be purchased as packages using Stripe. For example, $5 - 1000 credits, $10 - 2200 credits, $20 - 5000 credits. /buy-credit /my-credits
- Listening to these set of commands

## Telegram bot commands:

- help - Learn how to interact with me
- balance - Check how many credits you have
- buy - Buy more credits to interact with me
- restart - Restart the conversation
- threestory - Receive three stories per day
- twostory - Receive two stories per day
- onestory - Receive one story per day
- nostory - Disable story updatess

## Content

- [How to run locally](https://github.com/kartikmalhotra/telegram_ai_chat_bot/#how-to-run)
- [Telegram webhook](https://github.com/ohld/django-telegram-bot/#setup_telegram_bot_api_webhook_url)

# How to run

## Quickstart: Webhook & PostgreSQL

The fastest way to run the bot is to run it in webhook mode using SQLite database :

```bash
git clone https://github.com/kartikmalhotra/telegram_ai_chat_bot
cd telegram_ai_chat_bot
```

Create virtual environment (optional)

```bash
python3 -m venv venv
source venv/bin/activate
```

Install all requirements:

```
pip install -r requirements.txt
```

Create `django.env` file in root directory and add environment=local for local/ environment=production for production,
Change setting.py file in root directory and add your OpenAi, stripe keys in settings.py

Run migrations to setup SQLite database:

```bash
python manage.py migrate
```

Create superuser to get access to admin panel:

```bash
python manage.py createsuperuser
```

````
If you want to open Django admin panel which will be located on http://localhost:8000/tgadmin/:

```bash
python manage.py runserver
````

### Create superuser for Django admin panel

```bash
python manage.py createsuperuser
```

### Setup Telegram Bot API webhook URL

You need to tell Telegram servers where to send events of your Telegram bot. Just open in the browser:

```
https://api.telegram.org/bot<BotToken>/setWebhook?url=<DOMAIN_URL>/webhook/telegram?botid=<bot_id>

```

### Create Django super user

Being inside a container:

```bash
python manage.py createsuperuser
```

After that you can open admin panel of your deployed app which is located at https://<YOURDOMAIN.COM>/tgadmin.
