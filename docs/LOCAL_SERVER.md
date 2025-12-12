# Running a Local Vindinium Server

This guide shows you how to run your own local Vindinium server using Docker.

## Why Run a Local Server?

- **Test bots offline** - No internet connection required
- **Faster development** - No network latency
- **Private testing** - Your bots and games stay local
- **Multiple bots** - Test your bots against each other
- **Full control** - Customize game settings

## Prerequisites

- **Docker** and **Docker Compose** installed
- **Docker Desktop** running (on macOS/Windows)

### Install Docker

- **macOS**: Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
- **Linux**: Install via package manager: `sudo apt-get install docker.io docker-compose`
- **Windows**: Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)

## Quick Start

### 1. Start the Server

```bash
cd docker
docker-compose up -d
```

This starts:
- **MongoDB** database on port 27017
- **Vindinium server** on port 80 (http://localhost)

### 2. Verify Server is Running

Open your browser and go to: **http://localhost**

You should see the Vindinium web interface.

### 3. Create a Bot

1. Go to http://localhost
2. Click **"Register"** or **"Sign in"**
3. Create an account (local only, any email works)
4. Click **"Create a bot"**
5. Enter a bot name
6. Copy your **API key**

### 4. Configure Your Bot

Edit your `.env` file:

```bash
VINDINIUM_SERVER=http://localhost
VINDINIUM_KEY=<your-api-key-from-step-3>
VINDINIUM_HERO_NAME=MyBot
```

### 5. Run Your Bot

```bash
cd ..  # Back to project root
python main.py
```

Your bot will connect to your local server and start playing!

## Server Management

### View Server Logs

```bash
cd docker
docker-compose logs -f vindinium
```

Press `Ctrl+C` to stop viewing logs.

### Stop the Server

```bash
cd docker
docker-compose down
```

### Restart the Server

```bash
cd docker
docker-compose restart
```

### Check Server Status

```bash
cd docker
docker-compose ps
```

## Database Management

### Backup Database

Save your current database state (bots, games, users):

```bash
cd docker
./backup-db.sh
```

This creates backups in `docker/db-backup/`.

### Restore Database

Restore from a previous backup:

```bash
cd docker
./restore-db.sh
```

### Reset Database

Completely wipe and start fresh:

```bash
cd docker
docker-compose down
rm -rf mongodb-data
docker-compose up -d
```

## Testing Multiple Bots

You can run multiple bots against your local server:

### Option 1: Multiple Terminal Windows

1. Create multiple `.env` files (`.env.bot1`, `.env.bot2`, etc.)
2. In each terminal, load different env and run:
   ```bash
   # Terminal 1
   export $(cat .env.bot1 | xargs)
   python main.py
   
   # Terminal 2
   export $(cat .env.bot2 | xargs)
   python main.py
   ```

### Option 2: Arena Mode

Configure both bots for arena mode and they'll compete when 4 players join.

## Troubleshooting

### Port 80 Already in Use

If port 80 is taken, edit `docker/docker-compose.yml`:

```yaml
ports:
  - "8080:9000"  # Change 80 to 8080
```

Then use `VINDINIUM_SERVER=http://localhost:8080` in your `.env`.

### Server Won't Start

```bash
# Check Docker is running
docker ps

# View error logs
cd docker
docker-compose logs
```

### Can't Connect to Server

1. Verify server is running: `docker-compose ps`
2. Check URL in `.env` is `http://localhost` (not https)
3. Try accessing http://localhost in your browser

### Database Issues

Reset the database:
```bash
cd docker
docker-compose down
rm -rf mongodb-data
docker-compose up -d
```

## Advanced Configuration

### Change Server Port

Edit `docker/docker-compose.yml`:

```yaml
vindinium:
  ports:
    - "9000:9000"  # Use port 9000 instead of 80
```

Then update your `.env`:
```bash
VINDINIUM_SERVER=http://localhost:9000
```

### Persistent Data Location

Database files are stored in `docker/mongodb-data/` (excluded from Git).

## Next Steps

- Read the [Configuration Guide](CONFIGURATION.md) for more settings
- Check out [Getting Started](GETTING_STARTED.md) to build your first bot
- See [Code Snippets](SNIPPETS.md) for common patterns

## Summary

```bash
# Start server
cd docker && docker-compose up -d

# Create bot at http://localhost
# Copy API key to .env

# Run your bot
cd .. && python main.py

# Stop server when done
cd docker && docker-compose down
```

That's it! You now have a complete local Vindinium environment. 🎉

