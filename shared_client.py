# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

from telethon import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN, STRING
from pyrogram import Client
import sys
import asyncio

client = None
app = None
userbot = None

async def start_client():
    global client, app, userbot
    
    try:
        # Start Telethon client
        client = TelegramClient("telethonbot", API_ID, API_HASH)
        await client.start(bot_token=BOT_TOKEN)
        print("✅ SpyLib (Telethon) started...")
        
        # Start userbot if STRING is provided
        if STRING:
            try:
                userbot = Client(
                    "4gbbot", 
                    api_id=API_ID, 
                    api_hash=API_HASH, 
                    session_string=STRING
                )
                await userbot.start()
                print("✅ Userbot started...")
            except Exception as e:
                print(f"⚠️ Warning: Could not start userbot. Error: {e}")
                print("Continuing without userbot (4GB upload feature will be disabled)")
                userbot = None
        
        # Start Pyrogram app
        app = Client("pyrogrambot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
        await app.start()
        print("✅ Pyro App started...")
        
        return client, app, userbot
        
    except Exception as e:
        print(f"❌ Error starting clients: {e}")
        # Cleanup on error
        if client and client.is_connected():
            await client.disconnect()
        if app:
            try:
                await app.stop()
            except:
                pass
        if userbot:
            try:
                await userbot.stop()
            except:
                pass
        sys.exit(1)

async def stop_clients():
    """Gracefully stop all clients"""
    global client, app, userbot
    
    try:
        if client and client.is_connected():
            await client.disconnect()
            print("Telethon client disconnected")
    except Exception as e:
        print(f"Error stopping Telethon client: {e}")
    
    try:
        if app:
            await app.stop()
            print("Pyrogram app stopped")
    except Exception as e:
        print(f"Error stopping Pyrogram app: {e}")
    
    try:
        if userbot:
            await userbot.stop()
            print("Userbot stopped")
    except Exception as e:
        print(f"Error stopping userbot: {e}")
