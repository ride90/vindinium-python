# Vindinium Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites

- Python 3.13+
- Docker Desktop (for local server)

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Start Local Server

```bash
cd docker
./quickstart.sh
```

Or manually:
```bash
cd docker
docker-compose up -d
```

## Step 3: Create Your Bot

1. Open http://localhost in your browser
2. Register an account (any email works locally)
3. Click "Create a bot"
4. Enter a bot name
5. Copy your API key

## Step 4: Configure

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env`:
```bash
VINDINIUM_SERVER=http://localhost
VINDINIUM_KEY=<paste-your-api-key-here>
VINDINIUM_HERO_NAME=MyBot
```

## Step 5: Run Your Bot

```bash
python main.py
```

Watch your bot play at http://localhost!

## What's Next?

### Test Different Bots

Edit `main.py` to try different bots:

```python
# Try the miner bot
url = client.run(vindinium.bots.MinerBot())

# Try the aggressive bot
url = client.run(vindinium.bots.AggressiveBot())

# Try the minimax bot
url = client.run(vindinium.bots.MinimaxBot())
```

### Create Your Own Bot

See [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) for a tutorial.

### Run Multiple Bots

Create multiple `.env` files and run them in different terminals to compete against yourself!

## Common Commands

```bash
# Start server
cd docker && docker-compose up -d

# Stop server
cd docker && docker-compose down

# View server logs
cd docker && docker-compose logs -f vindinium

# Run your bot
python main.py

# Backup database
cd docker && ./backup-db.sh

# Restore database
cd docker && ./restore-db.sh
```

## Troubleshooting

**Port 80 in use?**
Edit `docker/docker-compose.yml` and change port 80 to 8080, then use `VINDINIUM_SERVER=http://localhost:8080`

**Server won't start?**
Make sure Docker Desktop is running: `docker ps`

**Can't connect?**
Check server is running: `cd docker && docker-compose ps`

## Documentation

- **[Local Server Guide](docs/LOCAL_SERVER.md)** - Complete server documentation
- **[Configuration](docs/CONFIGURATION.md)** - All settings explained
- **[Getting Started](docs/GETTING_STARTED.md)** - Build your first bot
- **[Code Snippets](docs/SNIPPETS.md)** - Common patterns

## Summary

```bash
# 1. Install
pip install -r requirements.txt

# 2. Start server
cd docker && ./quickstart.sh

# 3. Create bot at http://localhost and get API key

# 4. Configure
cp .env.example .env
# Edit .env with your API key

# 5. Run
python main.py
```

That's it! Happy bot building! 🤖

