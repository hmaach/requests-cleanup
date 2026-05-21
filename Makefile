# Social Media Request Cancellation Tool Makefile (cross-platform)

PYTHON := python3
VENV := venv

ifeq ($(OS),Windows_NT)
    ACTIVATE = $(VENV)\Scripts\activate
    PIP = $(VENV)\Scripts\pip
    PY = $(VENV)\Scripts\python
else
    ACTIVATE = . $(VENV)/bin/activate
    PIP = $(VENV)/bin/pip
    PY = $(VENV)/bin/python
endif

.PHONY: all venv install browsers run clean help instagram linkedin facebook

all: install browsers

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install playwright

browsers:
	$(PY) -m playwright install

run:
	$(PY) main.py

# Platform-specific shortcuts
instagram:
	$(PY) main.py instagram

linkedin:
	$(PY) main.py linkedin

facebook:
	$(PY) main.py facebook

help:
	@echo "Social Media Request Cancellation Tool"
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "Setup:"
	@echo "  make all        - Install dependencies and browsers (default)"
	@echo "  make install    - Create venv and install Python dependencies"
	@echo "  make browsers   - Install Playwright browsers"
	@echo ""
	@echo "Run:"
	@echo "  make run        - Run with custom arguments"
	@echo "  make instagram  - Cancel Instagram requests (uses data/pending_follow_requests.json)"
	@echo "  make linkedin   - Cancel LinkedIn connection requests"
	@echo "  make facebook   - Cancel Facebook friend requests"
	@echo ""
	@echo "Options (with 'make run'):"
	@echo "  make run ARGS='instagram --json custom.json --headless'"
	@echo "  make run ARGS='linkedin --delay 3.0'"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean      - Remove virtual environment"
	@echo ""
	@echo "Direct python3 usage (outside venv):"
	@echo "  python3 main.py instagram"
	@echo "  python3 main.py linkedin"
	@echo "  python3 main.py facebook"

clean:
	rm -rf $(VENV)
