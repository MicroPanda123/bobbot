import os
import cleverbot
import discord
from discord.ext import commands
from discord.ext.commands.errors import *
import wikipedia
import pyjokes
import random
from os.path import isfile


TOKEN = 'token' #remove this when you commit dumbass
client = commands.Bot(command_prefix='.')
client.remove_command('help')
#cb = cleverbot.load('bob.bob')
permissions = [230750179874045952, 749989977294635038, 622185311707070504] #Don't remove or we will lose control over mutes and warns
#ludwig = Ludwiger(['tweet'], 'model/')
spam = ["Don't do this please", 'Can you stop doing that?',
        'No buddy', 'God dammit stop', 'Why are you doing that?',
        'bruh']  ## TODO: Use this somewhere
ignored = ['i', 'a', 'and', 'but', 'then', 'that', 'you', 'me']
blocked_shit = ["that’s", "cool", "but", "did", "you", "know", "geico", "can", "help", "you", "save", "15%", "on", "car", "insurance"] #wtf is that


def count_words(member, text):
    text = text.lower()
    if not(any(ignore in text for ignore in ignored)):
        if not(member == client.user.name):
            import json
            from os.path import isfile
            text = text.split(' ')
            if not(isfile('words.json')):
                with open('words.json', 'w') as words:
                    json.dump({'testmember': {'test_word': 1}}, words)
            with open('words.json') as words:
                data = json.load(words)
            try:
                member_data = data[f'{member}']
            except KeyError as e:
                print("New user")
                member_data = {'word': 0}
            for word in text:
                try:
                    said = member_data[f'{word}']
                except KeyError as e:
                    said = 0
                said += 1
                write_data = {f'{word}': said}
                member_data.update(write_data)
            final_data = {f'{member}': member_data}
            data.update(final_data)
            #print(data)
            with open('words.json', 'w') as words:
                json.dump(data, words)

def get_words():
    import json
    with open('words.json') as words:
        data = json.load(words)
    return data

def get_member_words(member: discord.Member):
    return get_words()[f'{member.nick}']


@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))
    await client.change_presence(activity=discord.Game("being bob"))  # set bots status as "being bob"
    #guild = await client.fetch_channel(770408786011226124)
    #await guild.send("the fuck do you want?")

@client.command()
async def words(ctx, member: discord.Member):
    try:
        import json
        embed = discord.Embed(
            title="Top 10 most used words",
            description=f"Top 10 most used words of user {member}",
            colour=discord.Colour.dark_blue())
        member_words = get_member_words(member)
        sorted_words = sorted(member_words, key=member_words.__getitem__, reverse=True)
        for i in range(10):
            try:
                word = sorted_words[i]
                usages = member_words[f'{word}']
                embed.add_field(name=word, value=f'Used: {usages}', inline=False)
            except:
                break
        await ctx.send(embed=embed)
    except TypeError:
        pass

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


"""@client.command()
async def sa(ctx, *, msg):
    try:
        replay = cb.say(msg)  # get reply from cleverbot
    except Exception as error:
        await ctx.send(f'Something bad happend, error: {error}, please report this to creator')
    else:
        await ctx.send(replay)  # send reply from cleverbot to server
"""
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
    print("Cleverbot closed")
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
    embed.add_field(name='.words @{member}', value='Displays top 10 most commonly used words by given member.', inline=False)
    #embed.add_field(name='.sa {message to answer}',
    #                value='Sends your message to cleverbot which answers to what you said.', inline=False)
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
    count_words(message.author.nick, msg)
    print(msg)
    await client.process_commands(message)


client.run(TOKEN)
