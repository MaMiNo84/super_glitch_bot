# super_glitch_bot

Skeleton implementation for a Solana token monitoring service.
The service fetches token data from RugCheck and DexScreener, listens for new
token mints via Helius WebSockets, and announces promising tokens via a Telegram
bot while tracking performance.

## Installation
```bash
python3.9 -m venv venv  # tested with Python 3.9.23
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
Run the project with:
```bash
python main.py
```

## Shutdown
The service listens for `Ctrl+C`/SIGINT and the `/stop` command from Telegram.
On shutdown, background tasks are cancelled, the Telegram bot is stopped, and
the MongoDB connection is closed.

## Project Structure
- `super_glitch_bot/` - core package containing all modules
- `database/` - MongoDB connection and models
- `datasources/` - integrations with external APIs
- `services/` - monitoring, assessment and tracking logic
- `telegram_bot/` - telegram bot implementation
- `utils/` - helper utilities

## Message Templates
The bot uses predefined message templates from
`services/message_templates.py` for Telegram notifications:

- `NEW_GEM` - announces a newly listed token.
- `PERFORMANCE_UPDATE` - notifies about token performance milestones.
- `STARTED` - sent when the monitoring service starts.
- `STOPPED` - sent when the service stops.
- `ERROR` - generic error message template.
- `TOKEN_DELISTED` - indicates a tracked token was delisted.
