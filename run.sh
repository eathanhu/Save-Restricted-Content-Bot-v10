#!/bin/bash

# Kill any existing Python processes
pkill -f "python3 main.py" 2>/dev/null

# Clean up old session files
rm -f *.session *.session-journal 2>/dev/null

# Start the bot
python3 main.py
