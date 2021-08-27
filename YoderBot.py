import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import platform
import discord_components
import random
import youtube_dl

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

def getMembers(): # function for fetching all server members
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    server_members = []
    for member in guild.members:
        server_members.append(member.name)
    return server_members

class CommandErrorHandler(commands.Cog): # class for all error handling
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.RoleNotFound):
            await ctx.send("Role not available on this server! Try again or use %help for more.")

        if isinstance(error, commands.MemberNotFound):
            await ctx.send("Member not found! Try again or use %help for more.")

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing a required argument. Try again or use %help for more.")

        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Command entered does not exist. Type %help for more options.")

        if isinstance(error, commands.UserNotFound):
            await ctx.send("User could not be found! Try again or use %help for more.")

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(ctx.author.mention + ' Command is on cooldown, please try again after {:.2f} seconds.'.format(error.retry_after))


intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix='%')
bot.remove_command('help')  # gets rid of default help command
bot.remove_command('kick')
bot.add_cog(CommandErrorHandler(bot))


@bot.event
async def on_ready(): # sets bot's game status and runs some things when bot is connected to discord
    discord_components.DiscordComponents(bot)
    await bot.change_presence(activity=discord.Game(name="Just yodering about...  |  %help"))
    print(f'{bot.user} has connected to Discord!')
    print(f'{GUILD}\n')
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")

    currentmembers = getMembers()
    members = '\n - '.join(currentmembers)
    print(f'Guild Members:\n - {members}')
    print('*'*10)
    print("Bot is connected and operational!")
    print('*'*10)


async def on_message(ctx):
    #ignores announcement channel
    if ctx.channel.id == 258011659866603527:
        return
    elif bot.user.mentioned_in(ctx):
        await ctx.channel.send('You mentioned me!') # replies when a user mentions the bot

    shatten = bot.get_user(199756209484464129)
    if ctx.channel.id == 258011659866603527:
        return
    elif shatten.mentioned_in(ctx):
        await ctx.channel.send('https://tenor.com/view/fat-cheese-mac-and-cheese-gif-5496078') # replies a funny gif when @shatten is tagged

bot.add_listener(on_message)

@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
async def help(ctx, command=None):
    #print(command)
    commandlist = ['greetings', 'yoder', 'jferrell', 'addrole', 'removerole', 'admins', 'kick', 'RPS', 'pfp', 'nickname', 'announce', 'coinflip'] # sets list for available command
    if command in commandlist: # checks if command given by user in discord is a set command
        chosen_command = command
        author = ctx.author.mention
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        if chosen_command == "greetings":
            embed.set_author(name='Help for greetings')
            embed.description = 'Usage: ```%greetings```\n Greets the user by mention!'
            await ctx.send(author, embed=embed)
        elif chosen_command == "yoder":
            embed.set_author(name='Help for yoder')
            embed.description = 'Usage: ```%yoder```\n Replies to the user with the almighty Yoder Bot!'
            await ctx.send(author, embed=embed)
        elif chosen_command == "jferrell":
            embed.set_author(name='Help for jferrell')
            embed.description = 'Usage: ```%jferrell```\n Plugs our boy Justin\'s animation youtube channel!'
            await ctx.send(author, embed=embed)
        elif chosen_command == "addrole":
            embed.set_author(name='Help for addrole')
            embed.description = 'Usage: ```%addrole <specified role> <discord member>```\n Promotes a chosen member to a chosen role! ' \
                                'User activating the command must possess the "administrator" permission!'
            await ctx.send(author, embed=embed)
        elif chosen_command == "removerole":
            embed.set_author(name='Help for removerole')
            embed.description = 'Usage: ```%removerole <specified role> <discord member>```\n Removes a chosen role from a chosen member! ' \
                                'User activating the command must possess the "administrator" permission!'
            await ctx.send(author, embed=embed)
        elif chosen_command == "admins":
            embed.set_author(name='Help for admins')
            embed.description = 'Usage: ```%admins```\n Lists out all current server adminstrators and their status on the server.'
            await ctx.send(author, embed=embed)
        elif chosen_command == "kick":
            embed.set_author(name='Help for kick')
            embed.description = 'Usage: ```%kick <discord member> <reason>```\n Kicks a chosen member from the server. Listing a reason for kicking is optional. ' \
                                'User activating the command must possess the "kick_members" permission!'
            await ctx.send(author, embed=embed)
        elif chosen_command == "RPS":
            embed.set_author(name='Help for RPS')
            embed.description = 'Usage: ```%RPS <move>```\n Plays "Rock, Paper, Scissors" versus YoderBot!. <move> can consist of "Rock", "Paper", or "Scissors" to make a valid selection.'
            await ctx.send(author, embed=embed)
        elif chosen_command == "pfp":
            embed.set_author(name='Help for pfp')
            embed.description = 'Usage: ```%pfp <discord member>```\n Fetches the selected user\'s profile picture. If no member is given, replies with the user\'s profile picture.'
            await ctx.send(author, embed=embed)
        elif chosen_command == "nickname":
            embed.set_author(name='Help for nickname')
            embed.description = 'Usage: ```%nickname <discord member> <new nickname>```\n Changes a selected user\'s nickname. ' \
                                'User activating the command must possess the "administrator" permission!'
            await ctx.send(author, embed=embed)
        elif chosen_command == "announce":
            embed.set_author(name='Help for announce')
            embed.description = 'Usage: ```%announce <text>```\n Announces something to the whole server by mentioning everyone. ' \
                                'User activating the command must possess the "administrator" permission!'
            await ctx.send(author, embed=embed)
        elif chosen_command == "coinflip":
            embed.set_author(name='Help for coinflip')
            embed.description = 'Usage: ```%coinflip```\n Flips a coin!'
            await ctx.send(author, embed=embed)

    elif command == None: #displays help menu if no specific command is typed
        author = ctx.author.mention
        embed = discord.Embed(
            color=discord.Color.red()
        )
        embed.set_author(name='Help Menu')
        embed.description = 'Make sure to use the "%" prefix before entering a command!\n When using commands that need the input of a specific member, " " are required around a member whose name is multiple words.'
        embed.add_field(name='User Commands', value='```help, greetings, yoder, jferrell, admins, RPS, pfp, coinflip```', inline=False)
        embed.add_field(name='Admin Commands', value='```addrole, removerole, kick, nickname, announce```', inline=False)
        embed.add_field(name='More Information', value='For more help please visit: https://github.com/TRJoseph/YoderBot', inline=False)
        await ctx.send(author, embed=embed)
    else: #handles command entered not existing
        await ctx.send("No help could be found for " + str(command))


@bot.command(pass_context= True)
@commands.cooldown(1, 3, commands.BucketType.guild)
async def greetings(ctx):
    message = f'Hello, {ctx.author.mention} my name is YoderBot!'
    await ctx.send(message)

"""@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
async def test(ctx, *args):
    await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))"""

@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
async def yoder(ctx):
    image = 'https://media.discordapp.net/attachments/872159832076058684/872352115228565565/latest.png?width=901&height=676'
    await ctx.send('The Great and Almighty Yoder. Circa 2021.')
    await ctx.send(image)

@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
async def jferrell(ctx): #this command promotes my boy justin's long time animation youtube channel!
    ytchannel = 'https://www.youtube.com/channel/UCKQyUCFvmilciKu-ZjJAfRw'
    await ctx.send(ytchannel)


@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def addrole(ctx, role: discord.Role, member: discord.Member=None): #adds a role to a user
    member = member or ctx.message.author
    await member.add_roles(role)
    await ctx.send("Promoted " + str(member) + " to " + str(role))


@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def removerole(ctx, role: discord.Role, member: discord.Member=None): #removes a role from a user
    member = member or ctx.message.author
    await member.remove_roles(role)
    await ctx.send("Removed the role: " + str(role) + " from " + str(member))

@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member:discord.Member, reason=None): # kicks a given user with a provided reason
    member = member
    await member.kick(reason=reason)
    await ctx.send(f'{member} has been kicked by ' + ctx.author.mention)

@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
async def admins(ctx, guild: discord.Guild=None): # fetchs current server adminstrators
    try:
        role = ctx.guild.get_role(318895655248592907)
        adminlist = []
        adminstatus = []
        for member in role.members: # fetches admins and current statuses and groups them
            adminlist.append(str(member))
            status = member.status
            adminstatus.append(str(status))

        completelist = []
        for i in range(0, len(adminstatus), 1): # combines list of admins and their current status on the server
            completelist.append(adminlist[i] + " - "*5 + adminstatus[i])

        #print(completelist)
        statuses = ' \n > '.join(completelist)
        await ctx.send(f'Administrators:\n > {statuses}')
    except AttributeError: # handles the admin role not being present on the server
        await ctx.send('The Administrator role does not exist on this server!')

@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
async def RPS(ctx, move): # fun rock, paper, scissors game for a member to interact with!
    move = move.lower()
    moves = ['rock','paper','scissors']
    if move in moves:
        await ctx.send('You threw ' + str(move))
        bot_throw = random.choice(moves)
        if move == 'rock' and bot_throw == 'scissors':
            await ctx.send("You win! You threw " + str(move) + " while Yoderbot threw " + bot_throw + ".")
        elif move == 'rock' and bot_throw == 'paper':
            await ctx.send("You lose! You threw " + str(move) + " while Yoderbot threw " + bot_throw + ". throw better next time so you can get out of bronze")
        elif move == 'paper' and bot_throw == 'scissors':
            await ctx.send("You lose! You threw " + str(move) + " while Yoderbot threw " + bot_throw + ". LOL GET OWNED")
        elif move == 'paper' and bot_throw == 'rock':
            await ctx.send("You win! You threw " + str(move) + " while Yoderbot threw " + bot_throw + ".")
        elif move == 'scissors' and bot_throw == 'paper':
            await ctx.send("You win! You threw " + str(move) + " while Yoderbot threw " + bot_throw + ".")
        elif move == 'scissors' and bot_throw == 'rock':
            await ctx.send("You lose! You threw " + str(move) + " while Yoderbot threw " + bot_throw + ". xd u r trash")
        else:
            await ctx.send('It is a tie! Both you and Yoderbot both threw ' + str(move) + ".")
    else:
        await ctx.send('Your move is not valid. Try again or type %help for more')

@bot.command()
@commands.cooldown(1, 6, commands.BucketType.guild)
async def coinflip(ctx):
    options = ["Heads", "Tails"]
    await ctx.send(ctx.author.mention + " flipped a coin and it landed on " + random.choice(options) + ".")

@bot.command()
@commands.cooldown(1, 6, commands.BucketType.guild)
async def pfp(ctx, *, user: discord.Member=None):
    user = user or ctx.author
    await ctx.send(f"Profile picture of: **{user.name}**\n{user.avatar_url_as(size=1024)}")

@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def nickname(ctx, *, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send("Nickname for " + member.mention + "has changed.")

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def announce(ctx, *args):
    Achannel = bot.get_channel(258011659866603527)
    await Achannel.send('@everyone' + ' '.join(args))

bot.run(TOKEN)