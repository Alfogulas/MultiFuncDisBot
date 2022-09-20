import discord
import random
import time
from discord.ext import commands, tasks
import youtube_dl

client = commands.Bot(command_prefix='~')


@client.event
async def on_ready():
    print("Bot is online")


# functional -----------------------------------------------------------------------------------------------------------


@client.command()
async def ping(ctx):
    ping_responses = ["I'm trying to sleep :(", "Hello!", "Online and reporting for duty", "I hope you're not a mod"]
    await ctx.send(f"{random.choice(ping_responses)}\nPing: {round(client.latency * 1000)}ms")


@client.command()
async def purge(ctx, amount=1):
    await ctx.send(f"Purging {amount} messages...")
    await ctx.channel.purge(limit=amount + 2)


# music ----------------------------------------------------------------------------------------------------------------


@client.command(aliases=["p"])
async def play(ctx, url):
    if ctx.author.voice is None:
        await ctx.send("Please connect to a voice channel first!")
    else:
        if ctx.voice_client is None:
            await ctx.send(f"Connecting to **{ctx.author.display_name}** in **{ctx.author.voice.channel}**")
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send(f"Connecting to **{ctx.author.display_name}** in **{ctx.author.voice.channel}**")
            await ctx.voice_client.move_to(ctx.author.voice.channel)

    ctx.voice_client.stop()
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1  -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format': "bestaudio"}
    vc = ctx.voice_client

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        vc.play(source)


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await ctx.message.add_reaction("⏸️")
    voice.pause()


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await ctx.message.add_reaction("▶️")
    voice.resume()


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await ctx.message.add_reaction("🛑")
    voice.stop()


@client.command(aliases=["join"])
async def connect(ctx):
    if ctx.author.voice is None:
        await ctx.send("Please connect to a voice channel first!")
    else:
        if ctx.voice_client is None:
            await ctx.send(f"Connecting to **{ctx.author.display_name}** in **{ctx.author.voice.channel}**")
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send(f"Connecting to **{ctx.author.display_name}** in **{ctx.author.voice.channel}**")
            await ctx.voice_client.move_to(ctx.author.voice.channel)


@client.command(aliases=["dc"])
async def disconnect(ctx):
    await ctx.send("Bye!")
    await ctx.guild.voice_client.disconnect()


# fun ------------------------------------------------------------------------------------------------------------------


@client.command(aliases=["8ball"])
async def _8ball(ctx, *, question):
    _8ball_responses = ["It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely",
                        "You may rely on it", "As I see it, yes", "Most Likely", "Outlook is good", "yes",
                        "Signs point to yes", "Im not too sure", "It's best not to tell you", "Don't count on it",
                        "My reply is no", "My sources say no", "Outlook is negative", "Very Doubtful"]
    await ctx.send(random.choice(_8ball_responses))


@client.command()
async def say(ctx, *, quote):
    heisenburg = ["Heisenburg", ctx.author.display_name, ctx.author.display_name, ctx.author.display_name]
    if quote == "my name":
        await ctx.send(random.choice(heisenburg))
    else:
        await ctx.channel.purge(limit=1)
        await ctx.send(quote)


@client.command()
async def roulette(ctx, *, temp):
    if temp == "start":
        global roulette_p1
        roulette_p1 = " -"
        global roulette_p2
        roulette_p2 = " -"
        global roulette_p3
        roulette_p3 = " -"
        global roulette_p4
        roulette_p4 = " -"
        global roulette_p5
        roulette_p5 = " -"
        global roulette_p6
        roulette_p6 = " -"
        await ctx.send("Started a new russian roulette game\nUse **Roulette join** to join the game or **roulette "
                       "play** to start")
    elif temp == "join":
        valid = True
        if roulette_p1 == ctx.author.display_name or roulette_p2 == ctx.author.display_name:
            valid = False
        elif roulette_p3 == ctx.author.display_name or roulette_p4 == ctx.author.display_name:
            valid = False
        elif roulette_p5 == ctx.author.display_name or roulette_p6 == ctx.author.display_name:
            valid = False
        else:
            pass
        if valid == True:
            if roulette_p1 == " -":
                roulette_p1 = ctx.author.display_name
                await ctx.send(f"{roulette_p1} has joined russian roulette as player 1")
            elif roulette_p2 == " -":
                roulette_p2 = ctx.author.display_name
                await ctx.send(f"{roulette_p2} has joined russian roulette as player 2")
            elif roulette_p3 == " -":
                roulette_p3 = ctx.author.display_name
                await ctx.send(f"{roulette_p3} has joined russian roulette as player 3")
            elif roulette_p4 == " -":
                roulette_p4 = ctx.author.display_name
                await ctx.send(f"{roulette_p4} has joined russian roulette as player 4")
            elif roulette_p5 == " -":
                roulette_p5 = ctx.author.display_name
                await ctx.send(f"{roulette_p5} has joined russian roulette as player 5")
            elif roulette_p6 == " -":
                roulette_p6 = ctx.author.display_name
                await ctx.send(f"{roulette_p6} has joined russian roulette as player 6")
            else:
                await ctx.send(f"The game is already full, sorry {ctx.author.display_name}")
            await ctx.send(f"**Current players**\n**1.**{roulette_p1}\n**2.**{roulette_p2}\n**3.**{roulette_p3}\n**4.**"
                           f"{roulette_p4}\n**5.**"f"{roulette_p5}\n**6.**{roulette_p6}")
    elif temp == "play":
        if roulette_p6 == " -":
            if roulette_p5 == " -":
                if roulette_p4 == " -":
                    if roulette_p3 == " -":
                        if roulette_p2 == " -":
                            if roulette_p1 == " -":
                                await ctx.send("You don't have any players")
                            else:
                                await ctx.send("You only have one player")
                        else:
                            players = 2
                    else:
                        players = 3
                else:
                    players = 4
            else:
                players = 5
        else:
            players = 6
        if players > 1:
            if players == 6:
                roulette_p1_dead = False
                roulette_p2_dead = False
                roulette_p3_dead = False
                roulette_p4_dead = False
                roulette_p5_dead = False
                roulette_p6_dead = False
            elif players == 5:
                roulette_p1_dead = False
                roulette_p2_dead = False
                roulette_p3_dead = False
                roulette_p4_dead = False
                roulette_p5_dead = False
                roulette_p6_dead = True
            elif players == 4:
                roulette_p1_dead = False
                roulette_p2_dead = False
                roulette_p3_dead = False
                roulette_p4_dead = False
                roulette_p5_dead = True
                roulette_p6_dead = True
            elif players == 3:
                roulette_p1_dead = False
                roulette_p2_dead = False
                roulette_p3_dead = False
                roulette_p4_dead = True
                roulette_p5_dead = True
                roulette_p6_dead = True
            elif players == 2:
                roulette_p1_dead = False
                roulette_p2_dead = False
                roulette_p3_dead = True
                roulette_p4_dead = True
                roulette_p5_dead = True
                roulette_p6_dead = True
            else:
                pass
            dead = [10]
            rand = 10
            for i in range(players - 1):
                for x in range(len(dead)):
                    while rand != dead[x]:
                        rand = random.randint(1, players)
                    if rand == 1:
                        await ctx.send(f"Bang!\n{roulette_p1} was shot!")
                        roulette_p1_dead = True
                    elif rand == 2:
                        await ctx.send(f"Bang!\nI bet {roulette_p2} regrets that!")
                        roulette_p2_dead = True
                    elif rand == 3:
                        await ctx.send(f"Bang!\nThats an F for {roulette_p3}")
                        roulette_p3_dead = True
                    elif rand == 4:
                        await ctx.send(f"Bang!\nA bullet for my {roulette_p4}")
                        roulette_p4_dead = True
                    elif rand == 5:
                        await ctx.send(f"Bang!\n{roulette_p5} bit the dust")
                        roulette_p5_dead = True
                    else:
                        await ctx.send(f"Bang!\n{roulette_p6} has a portion of their brain removed")
                        roulette_p6_dead = True

            if roulette_p1_dead == False:
                await ctx.send(f"{roulette_p1} wins, good job!")
            elif roulette_p2_dead == False:
                await ctx.send(f"{roulette_p2} wins, good job!")
            elif roulette_p3_dead == False:
                await ctx.send(f"{roulette_p3} wins, good job!")
            elif roulette_p4_dead == False:
                await ctx.send(f"{roulette_p4} wins, good job!")
            elif roulette_p5_dead == False:
                await ctx.send(f"{roulette_p5} wins, good job!")
            elif roulette_p6_dead == False:
                await ctx.send(f"{roulette_p6} wins, good job!")


@client.command()
async def spam(ctx, target: discord.User, *, mess):
    print(target)
    for i in range(100):
        await target.send(mess)
        time.sleep(2)


client.run("ODQxMzgwMzgwOTMwMzQyOTIz.YJl6ig.Cc6PxMGA8TDbOCdZ7B8HFYYE9Es")
