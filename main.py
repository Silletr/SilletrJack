# --- IMPORTS ---
import os
from os import getenv
from dotenv import load_dotenv
import tracemalloc

from game_process.player import PlayerHand
from game_process.dealer import Dealer

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

active_games = {}  # In format: player_id: PlayerHand() }
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
tracemalloc.start()


# --- START COMMAND ---
@bot.command()
async def start(ctx):
    await ctx.send("Hello from LazyDeveloper community!")


# -- HELP COMMAND ---
@bot.command()
async def help(ctx):
    await ctx.send(
        "So, you need help, right? Ill give you this.\n"
        "!help - well you understood, right?\n"
        "!blackjack - start game with dealer (algorithm, not a real human)\n"
        "!ping - pong!\n"
        "!clear - clear chat (for 14 days)\n"
    )


# -- CLEAR COMMAND ---
@bot.command()
async def clear(ctx):
    await ctx.channel.purge(limit=None)
    await ctx.send("Chat cleared (for this 14 days)", delete_after=3)


# --- PING COMMAND ---
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


# --- BLACKJACK COMMAND ---
@bot.command()
async def blackjack(ctx):
    """Start a new Blackjack game for the player."""
    player_id = ctx.author.id
    game = PlayerHand()
    game.deal_initial_cards()
    active_games[player_id] = game

    await ctx.send(
        f"🎲 **Blackjack started!**\n"
        f"Your hand: {game.player_hand} = {game.calculate_hand_value(game.player_hand)}\n"
        f"Dealer's visible card: {game.dealer_hand[0]}"
        f"\n\nType `!hit` to take a card or `!stay` to hold."
    )


@bot.command()
async def hit(ctx):
    """Player takes another card."""
    player_id = ctx.author.id
    if player_id not in active_games:
        await ctx.send("You don't have an active game! Start with `!blackjack`.")
        return

    game = active_games[player_id]
    score = game.hit_user_command()

    if score > 21:
        await ctx.send(
            f"💥 You busted! Your hand: {game.player_hand} ({score})\nDealer wins!"
        )
        del active_games[player_id]
    else:
        await ctx.send(
            f"Card taken! Your hand: {game.player_hand} ({score})\n"
            "Type `!hit` to take another card or `!stay` to hold."
        )


@bot.command()
async def stay(ctx):
    """Player stays, dealer plays automatically."""
    player_id = ctx.author.id
    if player_id not in active_games:
        await ctx.send("You don't have an active game! Start with `!blackjack`.")
        return

    game = active_games[player_id]
    dealer = Dealer()
    dealer.deck = game.deck  # continue with same deck
    dealer.dealer_hand = game.dealer_hand
    dealer.play()

    # Final comparison
    game.player_hand_result = game.calculate_hand_value(game.player_hand)
    dealer_score = dealer.calculate_hand_value(dealer.dealer_hand)

    result_msg = (
        f"🏁 Final results:\n"
        f"You: {game.player_hand} ({game.player_hand_result})\n"
        f"Dealer: {dealer.dealer_hand} ({dealer_score})\n"
    )

    if game.player_hand_result > 21:
        result_msg += "💥 You busted! Dealer wins!"
    elif dealer_score > 21:
        result_msg += "💥 Dealer busted! You win!"
    elif game.player_hand_result > dealer_score:
        result_msg += "🎉 You win!"
    elif dealer_score > game.player_hand_result:
        result_msg += "😢 Dealer wins!"
    else:
        result_msg += "🤝 It's a tie!"

    await ctx.send(result_msg)
    del active_games[player_id]


# --- POINT OF ENTER  ---
def main():
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
