import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
import cleverbot
import os
import random
import time

TOKEN = "token"
client = commands.Bot(command_prefix = '.')
client.remove_command('help')
cb = cleverbot.load('bob.bob')
anstospam = ["Don't do this please", 'Can you stop doing that?',
             'No buddy', 'God dammit stop', 'Why are you doing that?',
             'bruh']


@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))
    await client.change_presence(activity=discord.Game("being bob"))

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
    embed = discord.Embed(
        title = "Help",
        description = "Help section",
        colour = discord.Colour.blue()
    )
    embed.add_field(name='.repeat', value='Repeats what you said.', inline=False)
    embed.add_field(name='.smartass', value='Sends your message to cleverbot which answers to what you said.', inline=False)
    embed.add_field(name='.aboutbob', value='About bob', inline=False)
    embed.add_field(name='.shrek', value='Sings part of All Star by Smash Mouth', inline=False)
    embed.add_field(name='.alexander', value='Sings part of Lin-Manuael Miranda from musical Hamilton', inline=False)
    embed.add_field(name='.join', value='Bob joins voice chat you are currently in (Work in progress, wont join to other voice chat if already in one)', inline=False)
    embed.add_field(name='.play {link to music on youtube}', value='Plays music from link (Work in progress, it takes some time until it will play music, DO NOT PLAY MUSIC OVER 15 MINUTES, using it when music already plays will change music instantly)', inline=False)
    embed.add_field(name='.pause', value='Pauses music', inline=False)
    embed.add_field(name='.resume', value='Resumes paused music', inline=False)
    embed.add_field(name='.stop', value='Stops playing music.', inline=False)
    embed.add_field(name='.autodestruction', value='Turns off bob', inline=False)
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def join(ctx):
    try:
        channel = ctx.message.author.voice.channel
    except AttributeError as er:
        await ctx.send("You are not in a voice channel")
        return
    await channel.connect()

@client.command(pass_context=True)
async def leave(ctx):
    try:
        voice_clients = client.voice_clients
        voice_client = voice_clients[0]
        await voice_client.disconnect()
    except:
        await ctx.send("I am not connected to any channel")
        return
    #voice_client = client.voice_channel_in(server)
    #await voice_client.disconnect()
    #print(server)

@client.command(pass_context=True)
async def play(ctx, *, msg):
    channel = ctx.message.author.voice.channel
    voice_clients = client.voice_clients
    voice_client = voice_clients[0]
    os.system(f'youtube-dl {msg} -f "bestaudio" -x --audio-format mp3 --output "./audio.%(ext)s"')
    await voice_client.play(discord.FFmpegPCMAudio(source="./audio.mp3"))

@client.command(pass_context=True)
async def pause(ctx):
    channel = ctx.message.author.voice.channel
    voice_clients = client.voice_clients
    voice_client = voice_clients[0]
    if not voice_client.is_playing():
        await ctx.send("Currently I am not playing anything")
        return
    if voice_client.is_paused():
        await ctx.send("Already paused")
        return
    await voice_client.pause()

@client.command(pass_context=True)
async def resume(ctx):
    channel = ctx.message.author.voice.channel
    voice_clients = client.voice_clients
    voice_client = voice_clients[0]
    if not voice_client.is_paused():
        await ctx.send("Nothing to resume")
        return
    await voice_client.resume()

@client.command(pass_context=True)
async def stop(ctx):
    channel = ctx.message.author.voice.channel
    voice_clients = client.voice_clients
    voice_client = voice_clients[0]
    await voice_client.stop()
    os.remove('./audio.mp3')

@client.command(pass_context=True)
async def gay(ctx):
    #print(ctx.message.author.roles)
    for i in ctx.message.author.roles:
        if i.id == 777956547283648532:
            await ctx.send('no')
            return

    await ctx.send('YES')
    #print(ctx.message.author.roles)

client.run(TOKEN)
