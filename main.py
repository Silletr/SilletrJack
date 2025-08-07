# --- IMPORTS ---
from os import getenv



import discord 
from discord.ext import commands

# --- VARIABLES AND .ENV ---
TOKEN = getenv("JACK_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None) 


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
        "Bot creator - @silletr_wt\n"
        "Username of creator in Telegram - @Python_tor"
    )

# --- PING COMMAND ---
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# --- BLACKJACK COMMAND ---
@bot.command()
async def blackjack(ctx):
    pass


# --- POINT OF ENTER  ---
def main():
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
