# --- IMPORTS ---
import os
from os import getenv
from dotenv import load_dotenv
import tracemalloc

from game_process.player import PlayerHand
from game_process.dealer import Dealer
from support.send_ticket import SendTicket


import discord
from discord.ui import Button, View
from discord.ext import commands
from loguru import logger

logger.remove()
logger.add(
    "disc_bot.log",
    level="DEBUG",
    format="{time:DD/MM/YYYY HH:mm} | <level>{level: <8}</level> | {message}",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
)


def load_config():
    """Load configuration with detailed debugging"""
    logger.info("\n=== Environment Check ===")
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.debug(f".env file exists: {os.path.exists('.env')}")

    # Try loading from .env file first
    try:
        load_dotenv()
        logger.debug("Successfully loaded .env file")
    except Exception as e:
        logger.error(f"Failed to load .env file: {str(e)}")

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

# --- SUPPORT COMMAND ---
class TicketView(View):
    def __init__(self, ticket_sender: discord.Member):
        super().__init__(timeout=None)  # No timeout for persistent buttons
        self.ticket_sender = ticket_sender  # Store ticket creator for permission checks

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, emoji="🔒")
    async def close_button(self, interaction: discord.Interaction, button: Button):
        # Check if the user is the ticket creator or has manage_channels permission
        if interaction.user != self.ticket_sender and not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("Only the ticket creator or admins can close this ticket!", ephemeral=True)
            return

        # Confirm before closing
        await interaction.response.send_message("Closing the ticket in 5 seconds...", ephemeral=True)
        await interaction.channel.delete()
        # Optionally notify the user in DM or a log channel
        try:
            await self.ticket_sender.send(f"Your ticket in {interaction.guild.name} has been closed.")
        except discord.errors.Forbidden:
            pass  # User might have DMs disabled

@bot.command()
async def ticket(ctx, *, content: str = None):
    """Create a new private channel for a ticket."""
    if content is None or content.strip() == "":
        await ctx.send("Hey, you forgot to provide a ticket description! Use the format: `!ticket <text>`")
        return

    try:
        # Validate content length
        if len(content) > 1000:
            await ctx.send("Your ticket description is too long! Please keep it under 1000 characters.")
            return

        ticket = SendTicket(
            ticket_name=f"ticket-{ctx.author.id}",
            ticket_description=content.strip(),
            ticket_sender=ctx.author
        )

        # Create the ticket channel
        ticket_channel = await ticket.send_ticket(ctx.guild, bot)

        # Send a message with the "Close Ticket" button in the ticket channel
        view = TicketView(ticket_sender=ctx.author)
        await ticket_channel.send(
            f"Ticket created by {ctx.author.mention}\nDescription: {content.strip()}\n\nClick the button below to close the ticket.",
            view=view
        )

        await ctx.send(f"✅ Your ticket is done: {ticket_channel.mention}")

    except discord.errors.Forbidden:
        await ctx.send("Error: I don't have permission to create a ticket channel. Please check my permissions!")
    except Exception as e:
        await ctx.send("An error occurred while creating your ticket. Please try again later.")
        print(f"Error in ticket command: {e}")
# --- PING COMMAND ---
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


# --- BLACKJACK COMMAND ---
class BlackjackView(View):
    def __init__(self, game: PlayerHand):
        super().__init__(timeout=180)  # 3-minute timeout
        self.game = game

        # Hit button
        hit_button = Button(label="Hit", style=discord.ButtonStyle.success, emoji="🎲")
        hit_button.callback = self.hit_callback

        # Stay button
        stay_button = Button(label="Stay", style=discord.ButtonStyle.danger, emoji="✋")
        stay_button.callback = self.stay_callback

        self.add_item(hit_button)
        self.add_item(stay_button)

    async def hit_callback(self, interaction: discord.Interaction):
        player_id = interaction.user.id
        if player_id not in active_games:
            await interaction.response.send_message(
                "No active game found! Start with `!blackjack`.", ephemeral=True
            )
            return

        game = active_games[player_id]
        score = game.hit_user_command()

        if score > 21:
            await interaction.response.edit_message(
                content=f"💥 You busted! Your hand: {game.player_hand} ({score})\nDealer wins!",
                view=None,
            )
            del active_games[player_id]
        else:
            await interaction.response.edit_message(
                content=(
                    f"Card taken! Your hand: {game.player_hand} ({score})\n"
                    f"Dealer's visible card: {game.dealer_hand[0]}"
                ),
                view=self,
            )

    async def stay_callback(self, interaction: discord.Interaction):
        player_id = interaction.user.id
        if player_id not in active_games:
            await interaction.response.send_message(
                "No active game found! Start with `!blackjack`.", ephemeral=True
            )
            return

        game = active_games[player_id]

        # Player stays
        game.stay_user_command()

        # Dealer plays
        dealer = Dealer()
        dealer.deck = game.deck
        dealer.dealer_hand = game.dealer_hand
        dealer.play()
        dealer_score = dealer.calculate_hand_value(dealer.dealer_hand)

        result_msg = (
            f"🏁 Final results:\n"
            f"You: {game.player_hand} ({game.player_hand_result})\n"
            f"Dealer: {dealer.dealer_hand} ({dealer_score})\n"
        )

        # Determine winner
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

        await interaction.response.edit_message(content=result_msg, view=None)
        del active_games[player_id]


@bot.command(description="Start a new Blackjack game")
async def blackjack(ctx):
    """Start a new Blackjack game for the player."""
    player_id = ctx.author.id

    if player_id in active_games:
        await ctx.reply(
            "You already have an active game! Finish it first.", ephemeral=True
        )
        return

    # Initialize game
    game = PlayerHand()
    game.deal_initial_cards()
    active_games[player_id] = game

    view = BlackjackView(game)
    await ctx.reply(
        f"🎲 **Blackjack started!**\n"
        f"Your hand: {game.player_hand} = {game.calculate_hand_value(game.player_hand)}\n"
        f"Dealer's visible card: {game.dealer_hand[0]}",
        view=view,
    )


@bot.event
async def on_interaction_error(interaction, error):
    """Global error handler for interactions"""
    if isinstance(error, discord.errors.MessageInteraction):
        await interaction.response.send_message(
            "This interaction has expired. Please start a new game!", ephemeral=True
        )
    else:
        raise error


# --- POINT OF ENTER  ---
def main():
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
