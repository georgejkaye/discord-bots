import discord
import re
import glob
import os

client = discord.Client()
emoji = client.get_emoji(689266841025380359)

agda = ''

for root, dirs, files in os.walk('../../agda-stdlib/src') :
    for file in files :
        if file.endswith('.agda') :
            with open(os.path.join(root,file), 'rt') as current :
                print (os.path.join(root,file))
                agda = agda + current.read()

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



        pattern = r"\n(" + re.escape(content) + r" : (.+\n.+)*)\n\n"
        print (pattern)

        regex = re.compile(pattern)

        result = re.search(regex, agda)

        print (result)

        if(result is not None) :
            await message.channel.send('```agda\n' + result.group(1) + '```')    

    if message.content.startswith('$proof'):
        await message.channel.send('```agda\npostulate proof : n > succ n\n```')

    if message.content.startswith('$timeline'):

        content = message.content.decode("utf8");      
        await message.channel.send('You are in the **darkest** timeline...')

client.run('NzA4MDYzNjAwMDg1ODI3NTk1.XrR50Q.Kq2dh4iXO5fQL_HPLzXmwXWKyIo ')