# Social Media Request Cancellation Tool

A unified tool to cancel pending follow/connection/friend requests across **Instagram**, **LinkedIn**, and **Facebook** using browser automation via Playwright.

---

## Features

- **Multi-platform support**: Instagram, LinkedIn, Facebook
- **Instagram**: Uses `data/pending_follow_requests.json` (your Instagram export)
- **LinkedIn**: Automatically navigates to invitation manager
- **Facebook**: Automatically navigates to friend requests page
- **Configurable**: Adjustable delays, headless mode
- **Safe**: Manual login, no credentials stored

---

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
   - [Instagram](#instagram)
   - [LinkedIn](#linkedin)
   - [Facebook](#facebook)
3. [Command-Line Options](#command-line-options)
4. [Makefile Shortcuts](#makefile-shortcuts)
5. [How It Works](#how-it-works)
6. [Notes & Safety](#notes--safety)

---

## Installation

### Prerequisites

- Python 3.8+
- `make` (optional, for convenience)

### Setup

```bash
make all
```

This will:
- Create a virtual environment (`venv/`)
- Install Python dependencies (Playwright)
- Install required browser binaries

Or manually:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install playwright
python -m playwright install
```

---

## Usage

### Instagram

#### Step 1 — Download Your Instagram Data

1. Open **Accounts Center** in Instagram settings
2. Go to **Your information and permissions** → **Export your information**
3. Click **Create Export** → select your account → **Export to device**
4. Choose:
   - **Data to export**: *Choose specific info* → select only **Followers and following**
   - **Date range**: *All time*
   - **Format**: *JSON*
   - **Media quality**: *Medium*
5. Wait for the email, then download the archive

#### Step 2 — Extract the JSON file

After extracting the archive, locate:
```
connections/
└── followers_and_following/
                └── pending_follow_requests.json
```

Copy this file to `data/pending_follow_requests.json` in the project root.

#### Step 3 — Run the tool

```bash
python3 main.py instagram
```

---

### LinkedIn

The tool automatically navigates to LinkedIn's invitation manager page and withdraws all pending connection requests.

```bash
python3 main.py linkedin
```

---

### Facebook

The tool automatically navigates to Facebook's friend requests page and cancels all pending friend requests.

```bash
python3 main.py facebook
```

---

## Command-Line Options

```
usage: main.py [-h] [--headless] [--delay DELAY]
               {instagram,linkedin,facebook}

positional arguments:
  {instagram,linkedin,facebook}
                        Platform to process

optional arguments:
  -h, --help            show this help message and exit
  --headless            Run browser in headless mode (invisible)
  --delay DELAY, -d DELAY
                        Delay in seconds between actions (default: 2.0)
```

### Examples

```bash
# Instagram with custom delay
python3 main.py instagram --delay 3.0

# LinkedIn in headless mode
python3 main.py linkedin --headless

# Facebook with short delay
python3 main.py facebook --delay 1.0
```

---

## Makefile Shortcuts

```bash
# Setup
make all          # Install dependencies and browsers (default)
make install      # Create venv and install Python deps
make browsers     # Install Playwright browsers

# Run platforms (uses venv Python)
make instagram    # Cancel Instagram requests
make linkedin     # Cancel LinkedIn connection requests
make facebook     # Cancel Facebook friend requests
make run          # Run with custom ARGS (e.g., make run ARGS="instagram --headless")

# Help & cleanup
make help         # Show all available commands
make clean        # Remove virtual environment
```

---

## How It Works

1. **Browser Launch**: Opens a Chromium browser window (visible by default)
2. **Manual Login**: You log in manually on the platform's login page
3. **Press ENTER**: After successful login, press ENTER in the terminal
4. **Processing**:
   - **Instagram**: Visits each profile from JSON and cancels requests
   - **LinkedIn**: Navigates to invitation manager and withdraws all pending
   - **Facebook**: Navigates to friend requests page and cancels all pending
5. **Statistics**: Shows a summary of processed targets

---

## Project Structure

```
requests-cleanup/
├── src/
│   ├── __init__.py
│   ├── cli.py              # CLI entry point and argument parsing
│   └── platforms/
│       ├── __init__.py
│       ├── base.py         # Abstract Platform base class
│       ├── instagram.py    # Instagram handler (JSON-based)
│       ├── linkedin.py     # LinkedIn handler (page-based)
│       └── facebook.py     # Facebook handler (page-based)
├── data/
│   └── pending_follow_requests.json.example  # Example Instagram data
├── main.py                 # Entry point
├── Makefile               # Build/run automation
├── README.md              # This file
└── .gitignore             # Git ignore rules
```

---

## Notes & Safety

- **Manual login** ensures your credentials are never stored or automated
- **Rate limiting**: Default 2-second delay between actions; adjust with `--delay`
- **UI changes**: If platforms update their UI, button selectors may need adjustment
- **Non-English interfaces**: Selectors assume English text; modify if needed
- **Headless mode**: Use `--headless` for background operation (requires prior login session or cookies)
- **Already cancelled**: Items without pending requests are automatically skipped
- **Errors**: Failed items are counted but don't stop the entire process

---

## Troubleshooting

### "No module named 'playwright'"
Run `make install` or install manually:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install playwright
python -m playwright install
```

### "Instagram data file not found"
Place your Instagram export at `data/pending_follow_requests.json`:
```bash
cp data/pending_follow_requests.json.example data/pending_follow_requests.json
# Then edit the file with your actual data
```

### "No pending request found" messages
- The request may already be cancelled
- The user may have accepted your request
- UI selectors may need updating for your language/region

### Login issues
- Ensure you're fully logged in before pressing ENTER
- If using headless mode, you may need to handle 2FA or captchas manually first

### Selector problems
If the tool can't find buttons, you may need to update the selectors in `src/platforms/*.py` to match the current platform UI.

---

## License

MIT License — feel free to modify and distribute.
