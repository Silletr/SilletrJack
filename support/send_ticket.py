import discord
from discord.ext import commands
from loguru import logger

class SendTicket:
    def __init__(self, ticket_name: str, ticket_description: str, ticket_sender: discord.Member):
        self.ticket_name = ticket_name
        self.ticket_description = ticket_description
        self.ticket_sender = ticket_sender

    async def send_ticket(self, guild: discord.Guild, bot: commands.Bot):
        """Creating private channel for ticket"""
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            self.ticket_sender: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        # Channel name
        channel_name = f"ticket-{self.ticket_sender.name}".lower()

        # Creating channel
        ticket_channel = await guild.create_text_channel(
            name=channel_name,
            overwrites=overwrites,
            reason=f"✔  Ticket created by {self.ticket_sender}"
        )

        # Send message to this channel 
        embed = discord.Embed(
            title=self.ticket_name,
            description=self.ticket_description,
            color=discord.Color.blue()
        )
        embed.set_author(name=str(self.ticket_sender))
        await ticket_channel.send(embed=embed)

        logger.info(f"Ticket channel {channel_name} created for {self.ticket_sender}")
        return ticket_channel
