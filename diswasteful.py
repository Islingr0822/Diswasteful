#imports discord.py library and commands
import discord
from discord.ext import commands
from recipe_store import get_random_recipe
TOKEN = ''

#defines the dictionary holding the list of items in the users pantry
pantry_data = {
    "Chicken": "7/14/2025",
    "Milk": "7/15/2025",
    "Bread":"7/20/2025"
}

intents = discord.Intents.default() #Checks for permissions
intents.message_content = True # Enable message content intent if needed
intents.dm_messages = True # Enables ability to send direct messages to users
intents.members = True # Checks for members in server

client = discord.Client(intents=intents)  #Checks for permissions

@client.event #checks for log in to discord api
async def on_ready():
    print(f'Logged in as {client.user}')

bot = commands.Bot(command_prefix='!', intents=intents) #sets command pre-fix symbol

# My discord id
OWNER_ID = '' 

#function that prints to terminal when bot is connected and ready
@bot.event 
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    # Sends a message to user on discord when the bot is online and ready.
    user = await bot.fetch_user(OWNER_ID)
    if user:
        try:
            await user.send("👋 The bot is now online and ready!")
            print("Startup DM sent.")
        except discord.Forbidden:
            print("Cannot send DM – the user has DMs disabled or blocked the bot.")
    else:
        print("Could not fetch user.")

@bot.command() #funtion to ping bot
async def ping(ctx):
    await ctx.send('Pong!')

#command to grab a random recipe and send it
@bot.command()
async def recipe(ctx):
    recipe = get_random_recipe()
    if not recipe:
        await ctx.send("No recipes available.")
        return
    
    msg = f"**{recipe['name']}**\n{recipe['url']}"
    if recipe["source"]:
        msg += f"\nSource: {recipe['source']}"

    await ctx.send(msg)


@bot.command()
async def pantry(ctx):
    user = ctx.author
    #Creates the message to be sent to the user, by using a for loop to create a formatted string 
    #with every key and value from the dictionary.
    message = '\n'.join(f"{key}: {value}" for key, value in pantry_data.items())

    try:
        await user.send(f"Here is your data:\n{message}")
    except discord.Forbidden:
        await ctx.send(f"{user.mention}, I couldn't DM you! Do you have DMs disabled?")

@bot.command() #sends the user a picture of Kermit the Frog when !kermit is input
async def kermit(ctx):
    user = ctx.author
    try:
        await user.send("https://static.wikia.nocookie.net/sillyman/images/3/3c/Kermit_the_Frog.png/revision/latest?cb=20241024094927")
    except discord.Forbidden:
        await ctx.send(f"{user.mention}, I couldn't DM you! Do you have DMs disabled?")

@bot.command()
async def stop(ctx):
    user = ctx.author
    print("Bot shutting down...")
    await user.send(f"Goodbye for now, {user.mention}")
    exit()


# Starts the bot with your token
bot.run('')



