# super_glitch_bot

Skeleton implementation for a Solana token monitoring service.

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

## Project Structure
- `super_glitch_bot/` - core package containing all modules
- `database/` - MongoDB connection and models
- `datasources/` - integrations with external APIs
- `services/` - monitoring, assessment and tracking logic
- `telegram_bot/` - telegram bot implementation
- `utils/` - helper utilities
