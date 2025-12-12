# Installation

This project is designed to run directly from source code - no package installation required!

## Prerequisites

- **Python 3.13 or higher**
- **pip** (Python package manager)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/ride90/vindinium-python.git
cd vindinium-python
```

### 2. Verify Python Version

Make sure you have Python 3.13 or higher:

```bash
python --version
```

If you need to install Python 3.13, visit [python.org](https://www.python.org/downloads/).

### 3. Create a Virtual Environment (Optional but Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `requests` - For HTTP communication with the Vindinium server
- `black` - Code formatter (development tool)
- Other supporting libraries

### 5. Get Your API Key

1. Visit [<https://your-vindinium-server-url>/](<https://your-vindinium-server-url>/)
2. Register for an account or log in
3. Copy your API key from your profile

### 6. Configure Your Bot

Edit `main.py` and update the configuration:

```python
client = vindinium.Client(
    server='<https://your-vindinium-server-url>',
    key='YOUR_API_KEY_HERE',  # Replace with your actual API key
    mode='training',           # 'training' or 'arena'
    n_turns=300,              # Number of turns (training mode only)
    open_browser=True         # Open browser to watch the game
)
```

## Testing Your Installation

### Test Module Import

```bash
python -c "import vindinium; print('✓ Vindinium imported successfully!')"
```

### List Available Bots

```bash
python -c "import vindinium; print('Available bots:', [b for b in dir(vindinium.bots) if 'Bot' in b])"
```

Expected output:
```
Available bots: ['AggressiveBot', 'BaseBot', 'MinerBot', 'MinimaxBot', 'RandomBot', 'RawBot']
```

### Run the Example Bot

```bash
python main.py
```

If everything is configured correctly, this will:
1. Connect to the Vindinium server
2. Start a training game
3. Run the MinerBot
4. Print the replay URL when finished

## Troubleshooting

### "ModuleNotFoundError: No module named 'requests'"

Install dependencies:
```bash
pip install -r requirements.txt
```

### "Connection refused" or "Connection error"

Check that:
1. You're using the correct server URL: `<https://your-vindinium-server-url>`
2. You have internet connectivity
3. The Vindinium server is online

### "Invalid API key"

Make sure:
1. You've registered at [<https://your-vindinium-server-url>/](<https://your-vindinium-server-url>/)
2. You've copied your API key correctly (no extra spaces)
3. You've replaced `<my key>` in `main.py` with your actual key

### Python version issues

This project requires Python 3.13+. Check your version:
```bash
python --version
```

If you have multiple Python versions, you may need to use `python3.13` explicitly:
```bash
python3.13 -m venv venv
```

## Next Steps

Once installation is complete:

1. Read [GETTING_STARTED.md](GETTING_STARTED.md) to learn how to create your first bot
2. Check [SNIPPETS.md](SNIPPETS.md) for common bot patterns
3. Explore the built-in bots in `vindinium/bots/` for examples
4. Start coding your own bot strategy!

## Updating Dependencies

To update all dependencies to their latest versions:

```bash
pip install --upgrade -r requirements.txt
```

## Uninstalling

Since this project runs from source, simply delete the project directory:

```bash
cd ..
rm -rf vindinium-python
```

If you created a virtual environment, it will be deleted along with the project directory.

