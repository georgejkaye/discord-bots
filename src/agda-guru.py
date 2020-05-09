import discord
import re
import glob
import os

client = discord.Client()
emoji = client.get_emoji(689266841025380359)

# Get the secret token from the token file
with open('token') as tokenfile:
    token = tokenfile.read()

with open('dirs') as dirfile:
    dirs = dirfile.read()

agda = []

# Get the entire standard library
for root, dirs, files in os.walk(dirs):
    for file in files:
        if file.endswith('.agda'):
            with open(os.path.join(root, file), 'rt') as current:
                print(os.path.join(root, file))

                module = os.path.join(root, file)[22:-5].replace('/', '.')
                agda.append((module, current.read()))

for module in agda:
    print(module[0])


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name='Agda 2.6.1'))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$agda'):

        await message.add_reaction(client.get_emoji(689266841025380359))

        await message.channel.send('I am the Agda Guru.')

        content = message.content[6:]

        args = content.split()

        target = False

        if (len(args) == 2):
            target = True
            targetmodule = args[0]
            function = args[1]
        else:
            function = args[0]

        pattern = r"(" + re.escape(function) + r" : (.+\n)*)"
        print(pattern)

        regex = re.compile(pattern)

        matches = []

        for module in agda:

            if(not target or targetmodule in module[0]):

                result = []

                result = re.search(regex, module[1])

                if (result is not None):

                    match = result.group(1)

                    print("Found a match in " + module[0] + ":\n\n" + match)
                    matches.append((module[0], match))

                else:
                    print("No matches in " + module[0])
            else:
                print("Not target module, skipping")

        if(len(matches) > 0):

            print("Matches!")

            matchtext = ''

            if len(matches) == 1:
                matchtext = "Found a match!"
            else:
                matchtext = "Found " + str(len(matches)) + " matches!"

            await message.channel.send(matchtext)

            reply = ""

            for match in matches:
                print(match)

                module = ""

                if not target:
                    module = 'In `' + match[0] + '`:\n'

                newfunction = module + '```agda\n' + match[1] + '```'
                potentialreply = reply + newfunction

                print(potentialreply)

                if(len(potentialreply) > 2000):
                    await message.channel.send(reply)
                    reply = newfunction
                else:
                    reply = reply + newfunction

            await message.channel.send(reply)

        else:
            await message.channel.send("No matches found!")

    if message.content.startswith('$proof'):
        await message.channel.send('```agda\npostulate proof : n > succ n\n```')

    if message.content.startswith('$timeline'):

        content = message.content.decode("utf8")
        await message.channel.send('You are in the **darkest** timeline...')

client.run(token)
