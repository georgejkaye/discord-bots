import discord
import re
import glob
import os

client = discord.Client()
emoji = client.get_emoji(689266841025380359)

# Get the secret token from the token file
with open ('token') as tokenfile :
    token = tokenfile.read()

agda = []

# Get the entire standard library
for root, dirs, files in os.walk('../../agda-stdlib/src') :
    for file in files :
        if file.endswith('.agda') :
            with open(os.path.join(root,file), 'rt') as current :
                print (os.path.join(root,file))

                module = os.path.join(root,file)[22:-5].replace('/','.')
                agda.append((module, current.read()))

for module in agda :
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

        if content == 'nat' or content == "Nat" or content == "N" :
            await message.channel.send('```agda\ndata ℕ : Set where\n\tzero : ℕ\n\tsucc : ℕ → ℕ```')    

        if content == "Bool" :
            await message.channel.send('```agda\ndata Bool : Set where\n\ttrue : Bool\n\tfalse : Bool```')    

        if content == "+" :
            await message.channel.send('```agda\n_+_ : ℕ → ℕ → ℕ\nzero     + y = y\n(succ x) + y = succ(x + y)```')    

        pattern = r"(" + re.escape(content) + r" : (.+\n)*)"
        print (pattern)

        regex = re.compile(pattern)

        matches = []

        for module in agda :

            result = []

            result = re.search(regex, module[1])

            if (result is not None) :

                match = result.group(1)

                print("Found a match in " + module[0] + ":\n\n" + match)
                matches.append((module[0], match))

            else :
                print("No matches in " + module[0])

        if(len(matches) > 0) :

            print ("Matches!")

            await message.channel.send("Found " + str(len(matches)) + " matches")

            for match in matches :
                print (match)
                reply = 'In `' + match[0] + '`:\n```agda\n' + match[1] + '```'
                await message.channel.send(reply)

        else :
            await message.channel.send("I couldn't find anything!")

    if message.content.startswith('$proof'):
        await message.channel.send('```agda\npostulate proof : n > succ n\n```')

    if message.content.startswith('$timeline'):

        content = message.content.decode("utf8");      
        await message.channel.send('You are in the **darkest** timeline...')

client.run(token)