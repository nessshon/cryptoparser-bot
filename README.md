<h1 align="center">🤖 CryptoParser bot</h1>

#### This bot parses cryptocurrency sites and sends the results for moderation to the bot for distribution to channels.

## Requirements

* Python 3.10 and above.
* Docker and docker-compose.

## Usage

Go to the project folder

```bash
cd cryptoparser-bot
```

Create environment variables file

```bash
cp .env.example .env
```

Edit [environment variables](#environment-variables-reference) in `.env`

```bash
nano .env
```

### Launch using Docker

1. Install [docker](https://docs.docker.com/get-docker) and [docker compose](https://docs.docker.com/compose/install/)

2. Build and run your container
   ```bash
   docker-compose up -d
   ```

### Environment variables reference

| Variable   | Type | Description                                             |
|------------|------|---------------------------------------------------------|
| REDIS_HOST | str  | Set "redis" if you will be using docker                 |
| BOT_TOKEN  | str  | Token, get it from [@BotFather](https://t.me/BotFather) |
| ADMIN_ID   | int  | Telegram Administrator ID                               |
| DEV_ID     | int  | Developer's Telegram ID                                 |
