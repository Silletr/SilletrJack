# --- IMPORTS ---
import os
from os import getenv
from dotenv import load_dotenv
import tracemalloc

import discord 
from discord.ext import commands


def load_config():
    """Load configuration with detailed debugging"""
    print("\n=== Environment Check ===")
    print(f"Current working directory: {os.getcwd()}")
    print(f".env file exists: {os.path.exists('.env')}")
    
    # Try loading from .env file first
    try:
        load_dotenv()
        print("Successfully loaded .env file")
    except Exception as e:
        print(f"Failed to load .env file: {str(e)}")
    
    # Get token and validate
    token = getenv("JACK_TOKEN")
    print("\nToken status:")
    print(f"- Token type: {type(token)}")
    print(f"- Token value: {'[REDACTED]' if token else 'None'}")
    
    if token is None:
        print("\nERROR: Token not found!")
        print("Possible causes:")
        print("1. .env file not found")
        print("2. JACK_TOKEN not defined in .env")
        print("3. Environment variables not accessible")
        exit(1)
    
    return token

# Load configuration
TOKEN = load_config()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=';', intents=intents, help_command=None) 
tracemalloc.start()

# --- START COMMAND ---
@bot.command()
async def start(ctx):
    await ctx.send('Hello from LazyDeveloper community!')

# -- HELP COMMAND ---
@bot.command()
async def help(ctx):
    await ctx.send(
        "So, you need help, right? Ill give you this.\n"
        "!help - well you understood, right?\n"
        "!blackjack - start game with dealer (algorithm, not a real human)\n"
        "!ping - pong!\n"
    )

# --- PING COMMAND ---
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# --- BLACKJACK COMMAND ---
@bot.command()
async def blackjack(ctx):
    await ctx.reply("Will be soon, wait a little bit!")


# --- POINT OF ENTER  ---
def main():
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
