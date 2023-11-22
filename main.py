import discord, random, os
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def readyBot():
    await bot.add_cog(status=discord.Status.online, activity=discord.Game('보치타치 랜덤 팀 생성기가 일하고 싶어해요!'))

#팀 설정 관련 변수들
teamList = []
memberList = []

@bot.command(aliases=['안녕', 'ㅎㅇ'])
async def hello(ctx):
    await ctx.send(f'{ctx.author.mention}님 안녕하세요! 전 보치타치 랜덤 팀 생성기에요!')

@bot.command(aliases=['설명'])
async def info(ctx):
    await ctx.send(f'[팀 설정]: 우선 팀 설정을 통해 팀을 설정해주세요!\n' +
                '[추가]: 랜덤 팀에 추가하려는 팀원들을 추가해주세요! \n' +
                '[랜덤 팀 생성]: 랜덤 팀을 생성할 수 있어요!')

#1 팀생성을 통해 원하는 수의 팀을 설정, 추가 입력을 하지 않은 경우 기본적으로 1:1로 2개의 팀이 생성된다.
@bot.command(aliases=['팀 설정', '설정'])
async def setTeam(ctx, count = 0): 
    if (count == 0):
        count = 2

    for i in range(0, count):
        teamList.append(i)

    await ctx.send(str(count) + '개의 팀이 생성되었습니다.')

#2 팀에 추가하고 싶은 멤버 입력을 받는다.
@bot.command(aliases=['추가'])
async def addMember(ctx, nick = ''):
    if (nick == ''):
        await ctx.send(f'추가할 멤버의 이름을 입력해주세요!')
        return
    
    if nick in memberList:
        await ctx.send(f'이미 추가된 멤버입니다! 다른 멤버의 이름을 입력해주세요!')
        return

    memberList.append(nick)
    await ctx.send(f'{nick}님이 추가되었습니다!')

#3 랜덤 팀 생성으로 팀을 무작위 멤버로 설정한다.
@bot.command(aliases=['팀 생성', '시작'])
async def ranTeam(ctx):
    if (len(teamList) == 0):
        await ctx.send(f'팀이 생성되어있지 않아요!\n먼저 [!팀 설정]을 통해 팀을 생성해주세요!!')
        return

    if (len(memberList) == 0 | len(memberList) % len(teamList) != 0):
        await ctx.send(f'팀을 구성하기 위한 인원이 부족하거나 많아 팀을 나눌 수 없어요!\n[!추가]를 통해 인원을 추가하거나 [!멤버 초기화]를 통해 새로 멤버들을 추가해주세요!')
        return

    shuffle()

    emb = discord.Embed(title="무작위 팀 결과!", color=discord.Color.green())
    for i in range(0, len(teamList)):
        a = ''
        for j in range(0, len(teamList[i])):
            a = a + teamList[i][j] + '\n'
        
        emb.add_field(name='팀 '+str(i+1), value=a, inline=False)
    
    await ctx.send(embed=emb)

@ranTeam.error
async def ranError(ctx,error):
    await ctx.send('랜덤 팀 생성에 실패했습니다 ㅠㅜ')


def shuffle():     
    for i in range(0, len(teamList)):
        teamList[i] = []
        
    _team = []
    copyList = memberList.copy()

    #_team에 무작위로 섞은 멤버를을 순차적으로 넣는다.
    while True:
        r = random.randrange(0, len(copyList))
        _team.append(copyList[r])
        del copyList[r]

        if (len(copyList) == 0):
            break

    #이후 무작위로 섞인 멤버를을 차례대로 팀에 추가한다.
    v = len(_team)
    for k in range(0, len(_team)):
        j = len(_team) % v
        #나머지를 통해 순차적으로 배치되는 경우 남은 수가 1일경우 값을 특정해준다
        if (v == 1):
            j = len(teamList) - 1
        teamList[j].append(_team[k])
        v = v-1

#가존 플레이어가 설정, 입력한 것들을 초기화
@bot.command(aliases=['초기화'])
async def init(ctx):
    memberList = []
    teamList = []
    await ctx.send(f'초기화 되었어요!\n다시 팀 설정과 멤버추가를 해주세요!')

access_token = os.environ['BOT_TOKEN']
bot.run(access_token)
