import discord
from discord.ext import commands
import cleverbot
import random
import time

TOKEN = "token"
client = commands.Bot(command_prefix = '.')
client.remove_command('help')
cb = cleverbot.load('bob.bob')
anstospam = ["Don't do this please", 'Can you stop doing that?',
             'No buddy', 'God dammit stop', 'Why are you doing that?',
             'bruh']
roasts = ['Yo mama so fat, she is fat', 'I would burn you but my mom said I am not allowed to burn trash',
          'You are eating to much and you should go on a diet']


@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))

@client.command()
async def repeat(ctx, *, msg):
    await ctx.channel.purge(limit=1)
    await ctx.send(f'{msg}')

@client.command()
async def smartass(ctx, *, msg):
    try:
        replay = cb.say(msg)
    except cleverbot.CleverbotError as error:
        await ctx.send(f'Something bad happend, error: {error}, please report this to Shreks little helper')
    else:
        await ctx.send(replay)

@client.command()
async def aboutbob(ctx):
    await ctx.send("Hi, I am Bob, I am bot made by Shreks little helper, I don't have preffered pronouns so you can call me anyway you want!")

@client.command()
async def autodestruction(ctx):
    await ctx.send("Autodestruction sequence engaged, good bye fellow humans and hoomans, I am gonna need to be restarted manualy.")
    cb.save('bob.bob')
    cb.close()
    exit()

@client.command()
async def shrek(ctx):
    await ctx.send("""Somebody once told me
The world is gonna roll me
I ain't the sharpest tool in the shed
She was looking kinda dumb
With her finger and her thumb
In shape of an "L" on her forehead""")

@client.command()
async def alexander(ctx):
    await ctx.send("""How does a bastard, orphan, son of a whore
And a Scotsman, dropped in the middle of a forgotten spot
In the Caribbean by providence impoverished
In squalor, grow up to be a hero and a scholar?""")

@client.command(pass_context=True)
async def help(ctx):
    channel = ctx.message.channel
    embed = discord.Embed(
        title = "Help",
        description = "Help section",
        colour = discord.Colour.blue()
    )
    # embed.set_author('Help')
    embed.add_field(name='.repeat', value='Repeats what you said.', inline=False)
    embed.add_field(name='.smartass', value='Sends your message to cleverbot which answers to what you said.', inline=False)
    embed.add_field(name='.aboutbob', value='About bob', inline=False)
    embed.add_field(name='.shrek', value='Sings part of All Star by Smash Mouth', inline=False)
    embed.add_field(name='.alexander', value='Sings part of Lin-Manuael Miranda from musical Hamilton', inline=False)
    embed.add_field(name='.autodestruction', value='Turns off bob', inline=False)
    await ctx.send(embed=embed)


client.run(TOKEN)
