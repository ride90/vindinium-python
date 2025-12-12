# Local Vindinium Server

Run your own Vindinium server locally using Docker.

## Quick Start

### Option 1: Use the Quick Start Script (Easiest)

```bash
./quickstart.sh
```

This will start the server and show you next steps.

### Option 2: Manual Start

```bash
# Start the server
docker-compose up -d

# Access at http://localhost
# Create a bot and get your API key

# Stop the server
docker-compose down
```

## What's Included

- **Vindinium Server** - Full game server on port 80
- **MongoDB** - Database for users, bots, and games
- **Backup/Restore** - Scripts to save and restore database state

## Detailed Documentation

See [docs/LOCAL_SERVER.md](../docs/LOCAL_SERVER.md) for complete guide including:
- Installation and setup
- Creating bots
- Testing multiple bots
- Database management
- Troubleshooting

## Server Management

### Start Server
```bash
docker-compose up -d
```

### Stop Server
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f vindinium
```

### Check Status
```bash
docker-compose ps
```

## Database Backup/Restore

### Backup
```bash
./backup-db.sh
```
Creates backups in `db-backup/latest/` and timestamped copies.

### Restore
```bash
./restore-db.sh
```
Restores from `db-backup/latest/`.

### Reset
```bash
docker-compose down
rm -rf mongodb-data
docker-compose up -d
```

## Configuration

Edit `docker-compose.yml` to change ports or settings.

Default configuration:
- **Server**: http://localhost (port 80)
- **MongoDB**: localhost:27017
- **Data**: Stored in `mongodb-data/` (gitignored)

## Troubleshooting

**Port 80 in use?** Edit `docker-compose.yml`:
```yaml
ports:
  - "8080:9000"  # Change to port 8080
```

**Server won't start?** Check Docker is running:
```bash
docker ps
docker-compose logs
```

**Need fresh start?** Reset the database (see above).

## Next Steps

1. Start the server: `docker-compose up -d`
2. Open http://localhost in your browser
3. Register and create a bot
4. Copy your API key to `../.env`
5. Run your bot: `cd .. && python main.py`

For complete documentation, see [docs/LOCAL_SERVER.md](../docs/LOCAL_SERVER.md).

