import discord
import re
import glob
import os

client = discord.Client()
emoji = client.get_emoji(689266841025380359)

# structure of module tuple
libn = 0
modn = 1
srcn = 2

scriptpath = os.path.dirname(os.path.realpath(__file__))
tokenpath = scriptpath + '/token'
libspath = scriptpath + '/dirs'

# Get the secret token from the token file
with open(tokenpath) as tokenfile:
    token = tokenfile.read()

with open(libspath) as libfile:
    libs = libfile.readlines()

agda = []

for lib in libs:

    # get the name of the library and its path
    libpair = lib.strip().split(':')
    libname = libpair[0]
    libpath = libpair[1]

    # Get the source of each library file
    for root, dirs, files in os.walk(libpath):
        print (root)
        for file in files:
            if file.endswith('.agda') or file.endswith('.lagda'):
                with open(os.path.join(root, file), 'rt') as current:

                    modulepath = os.path.splitext(os.path.join(root, file))[0]

                    module = modulepath[
                        len(libpath) + 1:].replace('/', '.')

                    agda.append((libname, module, current.read()))


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

            if(not target or targetmodule in module[modn]):

                result = []

                result = re.search(regex, module[srcn])

                if (result is not None):

                    match = result.group(1)

                    print("Found a match in " +
                          module[libn] + ":" + module[modn])
                    matches.append((module[libn], module[modn], match))

                else:
                    print(module[libn] + ":" +
                          module[modn] + ": no matches")
            else:
                print(module[libn] + ":" +
                      module[modn] + ": not target module, skipping")

        if(len(matches) > 0):

            if len(matches) == 1:
                reply = "Found a match!"
            else:
                reply = "Found " + str(len(matches)) + " matches!"

            reply = reply + "\n"

            for match in matches:
                module = 'In `' + match[modn] + \
                    '` from `' + match[libn] + '`:\n'

                newfunction = module + '```agda\n' + match[srcn] + '```'
                potentialreply = reply + "\n" + newfunction

                if(len(potentialreply) > 2000):
                    await message.channel.send(reply)
                    reply = newfunction
                else:
                    reply = reply + "\n" + newfunction

            await message.channel.send(reply)

        else:
            await message.channel.send("No matches found!")

    if message.content.startswith('$proof'):
        await message.channel.send('```agda\npostulate proof : n > succ n\n```')

    if message.content.startswith('$timeline'):

        content = message.content.decode("utf8")
        await message.channel.send('You are in the **darkest** timeline...')

client.run(token)
