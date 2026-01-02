#imports discord.py library and commands
import discord
import asyncio
from discord.ext import commands
from recipe_store import get_random_recipe
from recipe_store import add_recipe
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

#helper function that checks the author and allows for a timeout in the addrecipe function
async def ask_question(ctx, question, timeout=60):
    await ctx.send(question)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    
    try:
        msg = await ctx.bot.wait_for("message", check=check, timeout=timeout)
        if msg.content.lower() == "cancel":
            return None
        return msg.content.strip()
    except asyncio.TimeoutError:
        return None

#command that lets you add a recipe to the database from discord
@bot.command()
async def addrecipe(ctx):
    await ctx.send("Let's add a recipe. Type **cancel** at any time to stop.")

    name = await ask_question(ctx, "Recipe name?")
    if not name:
        await ctx.send("Cancelled.")
        return
    
    url = await ask_question(ctx, "Recipe URL?")
    if not url:
        await ctx.send("Cancelled.")
        return
    
    source = await ask_question(ctx, "Recipe source?")
    if not source:
        await ctx.send("Cancelled.")
        return
    
    category = await ask_question(ctx, "Category? (e.g. Dinner, Dessert)")
    if not category:
        await ctx.send("Cancelled.")
        return
    
    tags_input = await ask_question(ctx, "Tags? (comma-seperated, optional)")
    tags = [t.strip() for t in tags_input.split(",")] if tags_input else []

    success = add_recipe(
        name=name,
        url=url,
        source=source,
        category=category,
        tags=tags
    )

    if success:
        await ctx.send("Recipe added successfully.")
    else:
        await ctx.send("That recipe already exists.")

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



