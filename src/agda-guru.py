import discord
import re
import glob
import os

func = 0
data = 1
record = 2


class Function:
    def __init__(self, type, name, signature, source):
        self.type = type
        self.name = name
        self.signature = signature
        self.source = source


client = discord.Client()
emoji = client.get_emoji(689266841025380359)

# structure of module tuple
libn = 0
modn = 1
srcn = 2

scriptpath = os.path.dirname(os.path.realpath(__file__))
tokenpath = scriptpath + '/token'
libspath = scriptpath + '/dirs'

pattern = r"(?:data (.+?)|record (.+?)|(.+?)) : (?:(?:.+?\n)*? where|((?:.+?\n)*?)).+? = ((?:.+\n)*)"
regex = re.compile(pattern)

# Get the secret token from the token file
with open(tokenpath) as tokenfile:
    token = tokenfile.read()

with open(libspath) as libfile:
    libs = libfile.readlines()

agda = []

for lib in libs:

    print(lib)

    # get the name of the library and its path
    libpair = lib.strip().split(':')
    libname = libpair[0]
    libpath = libpair[1]

    # Get the source of each library file
    for root, dirs, files in os.walk(libpath):
        print(root)
        for file in files:
            if file.endswith('.agda') or file.endswith('.lagda'):
                with open(os.path.join(root, file), 'rt') as current:

                    modulepath = os.path.splitext(os.path.join(root, file))[0]

                    module = modulepath[
                        len(libpath) + 1:].replace('/', '.')

                    source = current.read()

                    matches = re.finditer(pattern, source)

                    functions = []

                    for match in matches:
                        groups = match.groups()

                        if match.group(1) is not None:
                            funtype = data
                        elif match.group(2) is not None:
                            funtype = record
                        else:
                            funtype = func

                        function = Function(funtype, match.group(
                            3), match.group(4)[:-1].split(" → "), match.group(0))

                        functions.append(function)

                    agda.append((libname, module, functions))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name='Agda 2.6.1'))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$proof'):
        await message.channel.send('```agda\npostulate proof : n > succ n\n```')
        return

    if message.content.startswith('$timeline'):

        content = message.content.decode("utf8")
        await message.channel.send('You are in the **darkest** timeline...')
        return

    if message.content.startswith('Ah!') or message.content.startswith("ah!"):
        await message.channel.send('Ah!')
        return

    matches = []

    search = False

    if message.content.startswith('$agda'):

        await message.add_reaction(client.get_emoji(689266841025380359))

        await message.channel.send('I am the Agda Guru.')

        content = message.content[6:]

        args = content.split()

        error = False

        tlibrary = False
        tmodule = False
        if (len(args) == 5):
            if(args[0] == "-l"):
                tlibrary = True
                targetlibrary = args[1]
            elif(args[0] == "-m"):
                tmodule = True
                targetmodule = args[1]

            if(args[2] == "-l"):
                tlibrary = True
                targetlibrary = args[3]
            elif(args[2] == "-m"):
                tmodule = True
                targetmodule = args[3]

            else:
                error = True

            function = args[4]

        elif (len(args) == 4):
            error = True

        elif (len(args) == 3):

            if(args[0] == "-l"):
                tlibrary = True
                targetlibrary = args[1]
            elif(args[0] == "-m"):
                tmodule = True
                targetmodule = args[1]
            else:
                tmodule = True
                tlibrary = True
                targetlibrary = args[0]
                targetmodule = args[1]

            function = args[2]

        elif (len(args) == 2):
            tmodule = True
            targetmodule = args[0]
            function = args[1]

        elif (len(args) == 1):
            function = args[0]

        else:
            error = True

        if (not error):

            for module in agda:

                if((not tlibrary or targetlibrary == module[libn]) and (not tmodule or targetmodule in module[modn])):

                    for func in module[srcn]:
                        if (func.name is not None and function in func.name):
                            matches.append(
                                (module[libn], module[modn], func.source))
                            break
        
            search = True

        else:
            await message.channel.send("I didn't understand what you said...")

    if message.content.startswith('$type'):
        await message.add_reaction(client.get_emoji(689266841025380359))

        content = message.content[6:]

        args = content.split(" -> ")

        if "N" in args:
            newargs = []
            for arg in args:
                if arg == "N":
                    newargs.append("ℕ")
                else:
                    newargs.append(arg)
            args = newargs

        print(args)

        for module in agda:

            for func in module[srcn]:
                if(args == func.signature):
                    matches.append((module[libn], module[modn], func.source))
                    break
        
        search = True

    if(len(matches) > 0):

        if len(matches) == 1:
            reply = "Found a match!"
        else:
            reply = "Found " + str(len(matches)) + " matches!"

        reply = reply + "\n"

        for match in matches:
            module = 'In `' + match[modn] + '` from `' + match[libn] + '`:\n'

            print(match[srcn])

            newfunction = module + '```agda\n' + match[srcn] + '```'
            potentialreply = reply + "\n" + newfunction

            if(len(potentialreply) > 2000):
                await message.channel.send(reply)
                reply = newfunction
            else:
                reply = reply + "\n" + newfunction

        await message.channel.send(reply)

    elif search :
        await message.channel.send("No matches found!")

client.run(token)
