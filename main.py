# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import asyncio
from shared_client import start_client
import importlib
import os
import sys
import signal

# Store client instances globally
clients = None

async def load_and_run_plugins():
    global clients
    clients = await start_client()
    plugin_dir = "plugins"
    plugins = [f[:-3] for f in os.listdir(plugin_dir) if f.endswith(".py") and f != "__init__.py"]

    for plugin in plugins:
        try:
            module = importlib.import_module(f"plugins.{plugin}")
            if hasattr(module, f"run_{plugin}_plugin"):
                print(f"Running {plugin} plugin...")
                await getattr(module, f"run_{plugin}_plugin")()
        except Exception as e:
            print(f"Error loading plugin {plugin}: {e}")

async def shutdown(signal_name=None):
    """Gracefully shutdown all clients"""
    global clients
    print(f"\n{'Received signal: ' + signal_name if signal_name else 'Shutting down'}...")
    
    if clients:
        telethon_client, pyrogram_app, userbot = clients
        
        try:
            # Stop all clients gracefully
            if telethon_client and telethon_client.is_connected():
                print("Stopping Telethon client...")
                await telethon_client.disconnect()
            
            if pyrogram_app:
                print("Stopping Pyrogram app...")
                await pyrogram_app.stop()
            
            if userbot:
                print("Stopping userbot...")
                await userbot.stop()
                
        except Exception as e:
            print(f"Error during shutdown: {e}")
    
    # Cancel all remaining tasks
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    print(f"Cancelling {len(tasks)} outstanding tasks...")
    for task in tasks:
        task.cancel()
    
    await asyncio.gather(*tasks, return_exceptions=True)
    print("Shutdown complete.")

async def main():
    # Setup signal handlers
    loop = asyncio.get_running_loop()
    
    def signal_handler(sig):
        print(f"\nReceived signal {sig}")
        asyncio.create_task(shutdown(signal.Signals(sig).name))
    
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, lambda s=sig: signal_handler(s))
    
    try:
        await load_and_run_plugins()
        # Keep running
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Main task cancelled")
    except KeyboardInterrupt:
        print("KeyboardInterrupt received")
    finally:
        await shutdown()

if __name__ == "__main__":
    try:
        print("Starting clients...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown initiated by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
