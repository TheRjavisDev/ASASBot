import robloxpy
import discord
import os # default module
from dotenv import load_dotenv
from math import floor

load_dotenv() # load all the variables from the env file
bot = discord.Bot()

from discordLevelingSystem import DiscordLevelingSystem, LevelUpAnnouncement, RoleAward

lvl = DiscordLevelingSystem()
lvl.connect_to_database_file(r'./DiscordLevelingSystem.db')

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.event
async def on_message(message):
    await lvl.award_xp(amount=[15, 25], message=message)

@bot.slash_command(name = "createthread", description = "Creates a thread")
async def createthread(ctx,startingmessage:str,threadname:str):
    await ctx.respond("Created Thread!",ephemeral=True)
    message2 = await ctx.send(startingmessage)
    await message2.create_thread(name=threadname, auto_archive_duration=60)

#@bot.slash_command(name = "say", description = "Says something as Manual Dumb Announcements System")
#async def createthread(ctx,say:str):
#    await ctx.respond(say)

@bot.slash_command(name = "rank", description = "Check your rank")
async def rank(ctx):
    data = await lvl.get_data_for(ctx.author)
    await ctx.respond(f"You're on the level {data.level} (#{data.rank}) and you have {data.xp} XP!")



@bot.slash_command(name = "leaderboard", description = "Server Leaderboard")
async def leaderboard(ctx):
    data = await lvl.each_member_data(ctx.guild,sort_by='rank')
    if len(data) > 2:
        response = f"Top 1: {data[1].name} ({data[1].level})\nTop 2: {data[2].name} ({data[2].level})"
    if len(data) > 3:
        response += f"\nTop 3: {data[3].name} ({data[3].level})"
        response += "\nBeware that this is incorrect since the library broke lol"
        await ctx.respond(response)
    elif len(data) == 2:
     await ctx.respond(f"Top 1: {data[1].name} ({data[1].level})\nTop 2: {data[2].name} ({data[2].level})")
    elif len(data) == 1:
        await ctx.respond(f"Top 1: {data[1].name} ({data[1].level})")
    else:
     await ctx.respond("Not enough members to display leaderboard!")

@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")

@bot.slash_command(name = "shutdown", description = "Shuts the mainframe down")
async def shutdown(ctx):
    if await bot.is_owner(ctx.author) == True:
        await ctx.respond("Warning - Unauthorized mainframe shutdowns detected.")
        await bot.close()
        print("Bot Closed")
    else:
        await ctx.respond("Access Denied.")

@bot.slash_command(name = "leave", description = "Leaves current guild")
async def shutdown(ctx):
    if await bot.is_owner(ctx.author) == True:
        await ctx.respond("Time to leave!",ephemeral=True)
        await ctx.guild.leave()
        print(f"Bot Left {ctx.guild.name} {ctx.guild.id}")
    else:
        await ctx.respond("Access Denied.",ephemeral=True)

@bot.slash_command(name = "ping", description="Wanna know how bad is Rjavis' Wi-Fi is?")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {floor(bot.latency * 1000)} MS")

@bot.slash_command(name="userinfo", description="Gets info about a user.")
async def info(ctx: discord.ApplicationContext, user: discord.Member = None):
    user = (
        user or ctx.author
    )  # If no user is provided it'll use the author of the message
    embed = discord.Embed(
        fields=[
            discord.EmbedField(name="ID", value=str(user.id), inline=False),  # User ID
            discord.EmbedField(
                name="Created",
                value=discord.utils.format_dt(user.created_at, "F"),
                inline=False,
            ),  # When the user's account was created
        ],
    )
    embed.set_author(name=user.name)
    embed.set_thumbnail(url=user.display_avatar.url)

    if user.colour.value:  # If user has a role with a color
        embed.colour = user.colour

    if isinstance(user, discord.User):  # Checks if the user in the server
        embed.set_footer(text="This user is not in this server.")
    else:  # We end up here if the user is a discord.Member object
        embed.add_field(
            name="Joined",
            value=discord.utils.format_dt(user.joined_at, "F"),
            inline=False,
        )  # When the user joined the server

    await ctx.respond(embeds=[embed])  # Sends the embed

math = discord.SlashCommandGroup("math", "Math related commands")

@math.command(description="random math command idk")
async def add(ctx, num1: int, num2: int):
  sum = num1 + num2
  await ctx.respond(f"{num1} plus {num2} is {sum}.")

@math.command(description="random math command idk")
async def subtract(ctx, num1: int, num2: int):
  sum = num1 - num2
  await ctx.respond(f"{num1} minus {num2} is {sum}.")

advanced = math.create_subgroup("advanced", "Advanced math commands")

from math import sqrt

@advanced.command(description="sqrt")
async def square_root(ctx, x: int):
    await ctx.respond(sqrt(x))

@advanced.command(description="divide")
async def divide(ctx, num1: int, num2: int):
  sum = num1 / num2
  await ctx.respond(f"{num1} divided by {num2} is {sum}.")

@advanced.command(description="multiply")
async def multiply(ctx, num1: int, num2: int):
  sum = num1 * num2
  await ctx.respond(f"{num1} multiplied by {num2} is {sum}.")

bot.add_application_command(math)

administration = discord.SlashCommandGroup("administration", "Administration related commands (ban, etc)")

@administration.command()
@discord.default_permissions(
    manage_messages=True,
    ban_members=True,
)
async def ban(ctx: discord.ApplicationContext,reason:str,member:discord.Member):
  await member.ban(reason = reason)
  await ctx.respond(f"Banned {member}!")

@administration.command()
@discord.default_permissions(
    manage_messages=True,
    kick_members=True,
)
async def kick(ctx: discord.ApplicationContext,reason:str,member:discord.Member):
  await member.kick(reason = reason)
  await ctx.respond(f"Kicked {member}!")
    
#@bot.slash_command(name="badges",
#             description="Check the Roblox badges of a username",
#             options=[
#               create_option(
#                 name="username",
#                 description="The Roblox username to check",
#                 option_type=3,
#                 required=True
#               )
#             ])
#async def badges(ctx: discord.ApplicationContext, username: str):
#    user = await robloxpy.User(username)
#    if user is None:
#        await ctx.send(f"Could not find user {username}.")
#        return
#    badges = await user.get_badges()
#    if not badges:
#        await ctx.send(f"{username} has no badges.")
#        return
#    embed = discord.Embed(title=f"{username}'s Roblox badges")
#    for badge in badges:
#        embed.add_field(name=badge.name, value=badge.description, inline=False)
#    await ctx.send(embed=embed)


bot.add_application_command(administration)

bot.run(os.getenv('TOKEN'))
