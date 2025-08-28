# Telegram Chat Parser and Aggregator

This project was (that was originally planned for using in my telegram channel) parses and aggregates messages from Telegram chats.

It reads message texts, media, etc. and provides aggregated information using AI.

## Roadmap

- [x] Parse Telegram chats
- [x] Save messages to a database
- [ ] Aggregate messages using AI
- [ ] Generate reports

## Usage

Fill .env file via .env.example

On first run:
```bash
uv sync --locked --all-groups
docker compose up --build -d migrations
```

Then run the userbot:
```bash
uv run -m src.userbot.main
```

And enter phone number and code. Then you can stop it and run via docker compose:
```bash
docker compose up -d --build
```

For the future runs just:
```bash
docker compose up -d --build
```