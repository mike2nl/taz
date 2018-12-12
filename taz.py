import discord
import json

from discord_token import TOKEN

with open('commands.json') as c:
    cmds = json.load(c)

with open('links.json') as l:
    links = json.load(l)

client = discord.Client()

help_mesg = """I provide quick access to various commands used in Tasmota software.
If you know the exact command (without parameters), use prefix "!" to read its summary (for example `!switchtopic`).
Alternatively, you can use prefix "?" so I can find commands by partial name (for example `?topic`)."""

welcome_mesg = """Hello and welcome to the Tasmota Discord server!

If you have generic questions regarding settings, functionality, or need help with configuration of your device, feel free to ask in the #general channel.
Do you think you've encountered a bug? The device doesn't work as expected? The #issues channel is for such questions.

Solutions or suggestions related to common issues and problems, especially for those new to Tasmota and compatible devices, are available on our wiki:

https://github.com/arendst/Sonoff-Tasmota/wiki/Initial-Configuration
https://github.com/arendst/Sonoff-Tasmota/wiki/FAQs
https://github.com/arendst/Sonoff-Tasmota/wiki/Troubleshooting (especially this one)

Please keep in mind that we're all volunteers here. Please be polite and patient. While we allow off-topic conversations, the channels are moderated. Flooding the chat, spamming links, being rude etc. is a quick way to be kicked (and/or banned, depending on the case).

Just be a decent human being and we'll all get along just fine."""

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content == "!help":
        await client.send_message(message.author, help_mesg)

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
    await client.send_message(member, welcome_mesg)


@client.event
async def on_ready():
    print('Logged in as {} ({})'.format(client.user.name, client.user.id))

client.run(TOKEN)
