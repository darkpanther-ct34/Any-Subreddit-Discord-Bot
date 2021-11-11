import os
import random
import discord
import json
from dotenv import load_dotenv
from reddit import any_sub

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


def write_json(data, filename='users.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(f'{message.author}: {message.content}')
    if message.content[0] == "!":
        msg = message.content[1::]
        msg = msg.split(" ")
        command = msg[0]
        print(msg, "\n", command)
        if command == "roll":
            print(len(msg))
            if len(msg) > 1:
                if msg[1].isnumeric():
                    dice = str(random.randint(0, int(msg[1])))
                    embed_var = discord.Embed(title="Dice Roll",
                                              description=f'I rolled a dice with {msg[1]} sides and got {str(dice)}',
                                              colour=0x206EEF)
                    await message.channel.send(embed=embed_var)
                else:
                    embed_var = discord.Embed(title="Failed Command",
                                              description=f'That is not a number.',
                                              colour=0xFF0000)
                    await message.channel.send(embed=embed_var)
            else:
                dice = str(random.randint(0, 6))
                embed_var = discord.Embed(title="Dice Roll",
                                          description=f'I rolled a dice with 6 sides and got {str(dice)}',
                                          colour=0x206EEF)
                await message.channel.send(embed=embed_var)
        elif command == "reddit":
            if len(msg) > 1:
                sub = msg[1]
                with open('users.json') as json_file:
                    data = json.load(json_file)
                if message.author in data:
                    nsfw = data[str(message.author)]["nsfw"]
                else:
                    data[str(message.author)] = {"nsfw": "False"}
                    write_json(data)
                    nsfw = False
                send = any_sub(sub, nsfw)
                await message.channel.send(embed=send)
            else:
                embed_var = discord.Embed(title="Failed Command",
                                          description="You need to specify the subreddit after the command",
                                          color=0xFF0000)
                await message.channel.send(embed=embed_var)
        elif command == "nsfw":
            if len(msg) > 1:
                if msg[1] == "on":
                    with open('users.json') as json_file:
                        data = json.load(json_file)
                    data[str(message.author)] = {"nsfw": "True"}
                    write_json(data)
                    embed_var = discord.Embed(title="NSFW",
                                              description="NSFW is turned on.",
                                              color=0x88D92C)
                    await message.channel.send(embed=embed_var)
                elif msg[1] == "off":
                    with open('users.json') as json_file:
                        data = json.load(json_file)
                    data[str(message.author)] = {"nsfw": "False"}
                    embed_var = discord.Embed(title="NSFW",
                                              description="NSFW is turned off.",
                                              color=0x88D92C)
                    await message.channel.send(embed=embed_var)
                else:
                    embed_var = discord.Embed(title="Failed Command",
                                              description="Please put on/off after the command.",
                                              color=0xFF0000)
                    await message.channel.send(embed=embed_var)
            else:
                embed_var = discord.Embed(title="Failed Command",
                                          description="Please put on/off after the command.",
                                          color=0xFF0000)
                await message.channel.send(embed=embed_var)


client.run(TOKEN)
