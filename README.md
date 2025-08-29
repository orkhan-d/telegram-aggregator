# Telegram Chat Parser and Aggregator

This project was (that was originally planned for using in my telegram channel) parses and aggregates messages from Telegram chats.

It reads message texts, media, etc. and provides aggregated information using AI.

#### Tech Stack
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=Pydantic&logoColor=white)

## Roadmap

- [x] Parse Telegram chats
- [x] Save messages to a database
- [ ] Aggregate messages using AI
- [ ] Generate reports

## Usage

Fill .env file via .env.example

#### On first run:
```bash
uv sync --locked --all-groups
```

Then run the userbot:
```bash
uv run -m src.userbot.main
```

And enter phone number and code.

---

#### For the future runs just:
```bash
docker compose up -d --build
```