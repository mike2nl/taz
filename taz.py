import discord
import json

from discord_token import TOKEN

with open('commands.json') as c:
    cmds = json.load(c)

with open('links.json') as l:
    links = json.load(l)

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content == "!help":

        msg = "I provide quick access to various commands used in Tasmota software.\nIf you know the exact command (without parameters)," \
              " use prefix \"!\" to read its summary (for example !switchtopic).\nAlternatively, you can use prefix \"?\" so I can find commands by partial name (for example ?topic)."
        await client.send_message(message.author, msg)


    elif message.content == "+links":
        link_list = ["+{}".format(k) for k in links.keys()]

        msg = '{0.author.mention} Available links:\n{1}'.format(message, ",".join(link_list))

        await client.send_message(message.channel, msg)

    elif message.content.startswith('!') and len(message.content) > 1:
        cmd = cmds.get(message.content.split(" ")[0][1:].lower(), None)

        if cmd:
            msg = '{}\n```{}```'.format(" ".join([m.mention for m in message.mentions]), "\n".join(cmd))

        else:
            msg = '{0.author.mention} Command not found. Use ? prefix to search.'.format(message)

        await client.send_message(message.channel, msg)

    elif message.content.startswith('+'):
        lnk = links.get(message.content[1:].lower(), None)

        if lnk:
            msg = lnk

        else:
            msg = '{0.author.mention} Shortlink not found.'.format(message)

        await client.send_message(message.channel, msg)

    elif message.content.startswith('?') and len(message.content) > 1:
        cmd = message.content.split(" ")[0][1:].lower()

        result = [c for c in cmds.keys() if cmd in c]

        if result:

            if len(result) > 9:
                msg = '{0.author.mention} Search yielded too many results. Narrow your query.'.format(message)

            else:
                msg = "{0.author.mention} I've found these commands:\n```{1}```".format(message, " ".join(result))

        else:
            msg = '{0.author.mention} No commands found.'.format(message)

        await client.send_message(message.channel, msg)


@client.event
async def on_member_join(member):
    await client.send_message(member, "Welcome to our server. You best behave.")


@client.event
async def on_ready():
    print('Logged in as {} ({})'.format(client.user.name, client.user.id))

client.run(TOKEN)
