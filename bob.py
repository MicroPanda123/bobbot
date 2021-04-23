import os
import cleverbot
import discord
from discord.ext import commands
from discord.ext.commands.errors import *
import wikipedia
import pyjokes
import random
import psycopg2

TOKEN = "hidden" #remove this when you commit dumbass
conn = psycopg2.connect(database="BobBase", user="Bob", password="", host="localhost", port="5433") #remove this too
cur = conn.cursor()
client = commands.Bot(command_prefix='.')
client.remove_command('help')
cb = cleverbot.load('bob.bob')
permissions = [230750179874045952, 749989977294635038, 622185311707070504] #Don't remove or we will lose control over mutes and warns
#ludwig = Ludwiger(['tweet'], 'model/')
spam = ["Don't do this please", 'Can you stop doing that?',
        'No buddy', 'God dammit stop', 'Why are you doing that?',
        'bruh']  ## TODO: Use this somewhere

blocked_shit = ["that’s", "cool", "but", "did", "you", "know", "geico", "can", "help", "you", "save", "15%", "on", "car", "insurance"] #wtf is that

def is_muted(id):
    ## FIXME: If a lot of people are muted it could lag every time
    ## someone send messages, but there are like 30 people on this server so fuck this
    cur.execute(f"select user_id from mutes;")
    mutes = cur.fetchall()
    for mute in mutes:
        if mute[0] == int(id):
            return True
    return False


@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))
    await client.change_presence(activity=discord.Game("being bob"))  # set bots status as "being bob"
    #guild = await client.fetch_channel(770408786011226124)
    #await guild.send("the fuck do you want?")

@client.command()
async def warn(ctx, member: discord.Member, *, reason="No reason given"):
    if ctx.author.id in permissions:
        cur.execute(f"insert into warns (user_id, user_nick, reason) values ({member.id},'{member.nick}','{reason}');")
        conn.commit()
        await ctx.send(f"Warned user {member} for {reason}")
    else:
        await ctx.send("You aren't permitted to use this command")

@client.command()
async def mute(ctx, member: discord.Member, *, reason="No reason given"):
    if ctx.author.id in permissions:
        cur.execute(f"insert into mutes (user_id, user_nick, reason) values ({member.id},'{member.nick}','{reason}');")
        conn.commit()
        await ctx.send(f"Muted user {member} for {reason}")
    else:
        await ctx.send("You aren't permitted to use this command")

@client.command()
async def delwarn(ctx, ID: int):
    if ctx.author.id in permissions:
        cur.execute(f"delete from warns where id={ID};")
        conn.commit()
        await ctx.send(f"Warn {ID} removed")
    else:
        await ctx.send("You aren't permitted to use this command")

@client.command()
async def unmute(ctx, member: discord.Member):
    if ctx.author.id in permissions:
        cur.execute(f"delete from mutes where user_id={member.id};")
        conn.commit()
        await ctx.send(f"Mute removed from {member}")
    else:
        await ctx.send("You aren't permitted to use this command")

@client.command()
async def warnings(ctx, member: discord.Member):
    embed = discord.Embed(
        title="Warnings",
        description=f"Warnings of user {member}",
        colour=discord.Colour.dark_blue())
    cur.execute(f"select * from mutes where user_id={member.id};")
    mutes = cur.fetchall()
    cur.execute(f"select * from warns where user_id={member.id};")
    warns = cur.fetchall()
    for mute in mutes:
        embed.add_field(name=f'Mute status:', value=f"Muted for: {mute[3]}", inline=False)
    if not(mutes):
        embed.add_field(name='Mute status:', value="Not muted.", inline=False)
    for warn in warns:
        embed.add_field(name=f'Warn: {warn[2]}', value=f"Warn ID: {warn[0]}", inline=False)
    if not(mutes):
        if not(warns):
            embed.add_field(name="You don't have any warnings.", value="Good job!", inline=False)
    await ctx.send(embed=embed)

#@client.command()
#async def displaydb(ctx):
#    cur.execute("select * from warnings;")
#    await ctx.send(cur.fetchall())

@client.command()
async def hangman(ctx, *, difficulty="N"):
    def is_correct(m):
        return m.author == ctx.author

    with open('sowpods.txt') as f:
        lista_slow = list(f)

    mistakes = 0
    if difficulty == 'E':
        while True:
            word = random.choice(lista_slow).strip()
            if len(word) < 5:
                break
            else:
                pass
    elif difficulty == 'N':
        while True:
            word = random.choice(lista_slow).strip()
            if len(word) > 6 and len(word) < 8:
                break
            else:
                pass
    elif difficulty == 'H':
        while True:
            word = random.choice(lista_slow).strip()
            if len(word) > 9:
                break
            else:
                pass
    spaces = []
    letters = list(word)
    for i in letters:
        spaces.append('_')
    while True:
        embed = discord.Embed(
            title="Hangman",
            description="Hangman",
            colour=discord.Colour.blue()
        )
        spaces_view = []
        spaces_view_str = ''
        for i in spaces:
            if i == '_':
                spaces_view.append('-')
            else:
                spaces_view.append(i)
        for i in spaces_view:
            spaces_view_str = spaces_view_str + i
        prev_spaces = list(spaces)
        embed.add_field(name='Word:', value=str(spaces_view_str))
        embed.add_field(name='Mistakes:', value=mistakes)
        embed.add_field(name='Player:', value=ctx.author)
        await ctx.send(embed=embed)
        litera = await client.wait_for('message', check=is_correct)
        try:
            if ord(litera.content) > 90:
                litera = chr(ord(litera.content) - 32)
            print(litera)
            for i in range(len(letters)):
                if litera == letters[i]:
                    spaces[i] = litera
                    #print(litera)
            if prev_spaces == spaces:
                mistakes += 1
            if mistakes >= 6:
                letters_view = ''
                for i in letters:
                    letters_view = letters_view + i.lower()
                await ctx.send(f'You lose! \nThe word was: {letters_view}')
                break
            num = 0
            for i in spaces:
                if i == '_':
                    num += 1
            if num == 0:
                letters_view = ''
                for i in letters:
                    letters_view = letters_view + i.lower()
                await ctx.send(f'Word is: {letters_view}. You won!')
                break
        except TypeError:
            pass

@client.command()
async def repeat(ctx, *, msg):
    await ctx.message.delete()
    words = 0
    chck_msg = msg.lower()
    for i in blocked_shit:
        #print(i)
        #print(chck_msg)
        if i in chck_msg:
            print("asshole")
            words = words + 1
    if words < 4:
        await ctx.send(f'{msg}')
    else:
        pass


@client.command()
async def sa(ctx, *, msg):
    try:
        replay = cb.say(msg)  # get reply from cleverbot
    except Exception as error:
        await ctx.send(f'Something bad happend, error: {error}, please report this to creator')
    else:
        await ctx.send(replay)  # send reply from cleverbot to server

@client.command()
async def joke(ctx):
    await ctx.send(pyjokes.get_joke())

@client.command()
async def wiki(ctx, *, msg):
    msg = msg.strip()
    await ctx.send(msg)
    try:
        await ctx.send(wikipedia.summary(msg, auto_suggest=False, sentences=3))
    except Exception as e:
        print(e)
        await ctx.send(e)

@client.command()
async def aboutbob(ctx):
    creator = await client.fetch_user(230750179874045952)
    await ctx.send(f"Hi, I am Bob, I am bot made by {creator}!")


@client.command()
async def autodestruction(ctx):
    await ctx.send(
        "Autodestruction sequence engaged, good bye fellow humans and hoomans, I am gonna need to be restarted manualy.")
    cb.save('bob.bob')
    cb.close()
    print("Cleverbot closed")
    conn.close()
    print("SQL database closed")
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
        title="Help",
        description="Help section",
        colour=discord.Colour.blue()
    )
    embed.add_field(name='.repeat {message to repeat}', value='Repeats what you said.', inline=False)
    embed.add_field(name='.sa {message to answer}',
                    value='Sends your message to cleverbot which answers to what you said.', inline=False)
    embed.add_field(name='.wiki {thing from wikipedia}', value='Gets summary of searched thing from wikipedia', inline=False)
    embed.add_field(name='.joke', value='Tells a joke', inline=False)
    embed.add_field(name='.hangman', value='Play hangman, you need to specify difficulty: E is easy, N is normal and H is hard', inline=False)
    embed.add_field(name='.aboutbob', value='About bob', inline=False)
    embed.add_field(name='.shrek', value='Sings part of All Star by Smash Mouth', inline=False)
    embed.add_field(name='.alexander', value='Sings part of Lin-Manuael Miranda from musical Hamilton', inline=False)
    # embed.add_field(name='.join', value='Bob joins voice chat you are currently in (Work in progress, wont join to other voice chat if already in one)', inline=False)
    # embed.add_field(name='.play {link to music on youtube}', value='Plays music from link (Work in progress, it takes some time until it will play music, DO NOT PLAY MUSIC OVER 15 MINUTES, using it when music already plays will change music instantly)', inline=False)
    # embed.add_field(name='.replay', value='Replays last played audio', inline=False)
    # embed.add_field(name='.pause', value='Pauses music', inline=False)
    # embed.add_field(name='.resume', value='Resumes paused music', inline=False)
    # embed.add_field(name='.stop', value='Stops playing music.', inline=False)
    # embed.add_field(name='.speak {2 letter language code (e.g. pl or en)} {what you want bob to say}', value='Bob will say anything you tell bob to on voice chat, egzample of use: ".speak en asshole" (work in progress, can be buggy)')
    embed.add_field(name='.autodestruction', value='Turns off bob', inline=False)
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def join(ctx):
    try:
        channel = ctx.message.author.voice.channel  # check on which voice chat author of message is
    except AttributeError as er:
        await ctx.send("You are not in a voice channel")
        return
    await channel.connect()  # connect to voice chat


@client.command(pass_context=True)
async def leave(ctx):
    try:
        voice_clients = client.voice_clients
        voice_client = voice_clients[0]
        await voice_client.disconnect()
    except:
        await ctx.send(f"I am not connected to any channel")
        return


@client.command(pass_context=True)
async def play(ctx, *, msg):
    ## FIXME: This shit is stupid but it works so idgaf
    try:
        voice_clients = client.voice_clients
        voice_client = voice_clients[0]
        os.system(f'youtube-dl {msg} -f "bestaudio" -x --audio-format mp3 --output "./audio.%(ext)s"')
        await voice_client.play(discord.FFmpegPCMAudio(source="./audio.mp3"))
    except TypeError as err:
        pass
    except:
        await ctx.send("I am not connected to any channel")


#@client.command(pass_contest=True)
#async def replay(ctx):
#    try:
#        voice_clients = client.voice_clients
#        voice_client = voice_clients[0]
#        await voice_client.play(discord.FFmpegPCMAudio(source="./audio.mp3"))
#    except TypeError as err:
#        pass
#    except:
#        await ctx.send("I am not connected to any channel")


@client.command(pass_context=True)
async def pause(ctx):
    # channel = ctx.message.author.voice.channel
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
    voice_clients = client.voice_clients
    voice_client = voice_clients[0]
    if not voice_client.is_paused():
        await ctx.send("Nothing to resume")
        return
    await voice_client.resume()


@client.command(pass_context=True)
async def stop(ctx):
    try:
        voice_clients = client.voice_clients
        voice_client = voice_clients[0]
        if voice_client.is_playing() or voice_client.is_paused():
            await voice_client.stop()
            os.remove('./audio.mp3')
        else:
            await ctx.send("Nothing to stop")
    except TypeError as er:
        return
    except:
        await ctx.send("Not connected to any voice channel")


#@client.command(pass_contest=True)
#async def speak(ctx, language, *, msg):
#    try:
#        tts = gTTS(msg, lang=language)
#        tts.save('speak.mp3')
#        voice_clients = client.voice_clients
#        voice_client = voice_clients[0]
#        await voice_client.play(discord.FFmpegPCMAudio(source="./speak.mp3"))
#    except TypeError as er:
#        return
#    except:
#        await ctx.send("I am not connected to any channel")

@client.event
async def on_command_error(ctx, error):
    creator = await client.fetch_user(230750179874045952)
    if isinstance(error, MissingRequiredArgument) or isinstance(error, BadArgument) or isinstance(error, ArgumentParsingError):
        await ctx.channel.send(error)
    else:
        await ctx.channel.send(error + f" report that to {creator}")


@client.event
async def on_message(message):
    msg = message.content
    print(msg)
    if is_muted(message.author.id):
        await message.delete()
    await client.process_commands(message)


client.run(TOKEN)
