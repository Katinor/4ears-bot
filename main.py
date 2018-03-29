import re
import requests
import json	
import random
import time
import os
import glob
import asyncio
import discord
from discord.ext import commands
from urllib import parse
import quadra_search_list
import quadra_search_vocab
import quadra_dialog_list
import quadra_game_list
import quadra_config
import quadra_lifetime
import quadra_user_module
from quadra_user_module import quadra_user
from quadra_message_module import quadra_message
import quadra_baseball, quadra_lotto, quadra_updown
from quadra_perm_module import server_permission
from quadra_memo_module import quadra_memo

bot_token = quadra_config.BOT_TOKEN
bot = commands.Bot(description="사잽아 도와줘 라고 말해주면 알려줄게!", command_prefix="")
uptime = 0
pingtime = 0
owner = [quadra_config.OWNER]
admin = []
LOTTO_CHARGE = 1000

def onGame(user_id):
	if quadra_baseball.enable(user_id) : return "야구게임을"
	if quadra_updown.enable(user_id) : return "업다운을"
	if quadra_lotto.enable(user_id) : return "로또를"
	else : return ""

def mention_user(user_id):
	return "<@"+str(user_id)+">"

def admin_load():
	fp = open('quadra_admin.txt','r')
	target = fp.readlines()
	for i in range(0,len(target)-1,1):
		target[i] = (target[i].split('\n'))[0]
	fp.close()
	temp_arr = []
	for i in target:
		temp_arr.append(i)
	return temp_arr

def admin_save(temp_arr):
	fp = open('quadra_admin.txt','w')
	for i in range(0,len(temp_arr),1):
		if i == len(temp_arr)-1: fp.write(temp_arr[i])
		else : fp.write(temp_arr[i]+"\n")
	fp.close()
	return admin_load()

def change_size(time):
	temp = time
	hour = temp // 3600
	temp -= hour * 3600
	min = temp // 60
	temp -= min * 60
	sec = temp
	return [int(hour),int(min),int(sec)]

def log_append(_chat_id, _text, _type, _subtype):
	_now = time.localtime()
	if _subtype!=0 : what_type = _type +'_' +_subtype
	else : what_type = _type
	target = "[%04d-%02d-%02d %02d:%02d:%02d] trgd [%10s] from [%15s] : %s" % (_now.tm_year, _now.tm_mon, _now.tm_mday, _now.tm_hour, _now.tm_min, _now.tm_sec, what_type,str(_chat_id),_text)	
	fp = open("log/quadra_bot_log.txt", 'a')
	if os.path.getsize("log/quadra_bot_log.txt") >= 102400:
		fp.close()
		filelist = glob.glob("log/*.*")
		filenum = len(filelist)
		filename = "log/quadra_bot_log_"+str(filenum)+".txt"
		os.rename("log/quadra_bot_log.txt",filename)
		fp = open("log/quadra_bot_log.txt", 'a')
	print(target)
	fp.write(target+"\n")
	fp.close()
	return _now

def url_encode(data):
	return (parse.quote(data).replace('/', '%2F'))

async def version(msg,user):
	chat_id = msg.channel.id
	now = log_append(chat_id, str(msg.content), "help",0)
	text="반가워! 나는 사잽이라고해! 지금은 베타 버전이야!\n"
	text+="나는 이런것들을 할 수 있어!\n"
	text+="* 4ears channel help : 채널 제한 설정 안내\n"
	text+="* 사잽아 누구니 : License Notice\n"
	text+="* 사잽아, 사잽아 뭐하니, 사잽아 놀아줘\n"
	#text+="* 쫑긋\n"
	text+="* 사잽아 ~~ 찾아줘/알려줘\n"
	text+="	* 지원 엔진 : 구글, 네이버, 나무위키, 리브레위키, 위키백과, 구스위키, 진보위키, 백괴사전\n"
	text+="* 사잽아 ~ 해줘/하자/어때/사줘\n * 사잽아 (게임이름) 하자\n"
	text+=" * 지원 게임 : 야구게임, 업다운, 로또(판당 1000원)\n"
	text+="* 사잽아 나 어때\n"
	text+="* 사잽아 용돈줘\n"
	text+="* 사잽아 네코 : nekos.life API를 사용해 무작위의 고양이귀 짤을 가져옵니다."
	user.mody(love = 1, love_time = True, exp = 5, exp_time = True)
	em = discord.Embed(title="여길 누르면 지원채널로 갈 수 있어!",description=text, colour=discord.Colour.blue(), url = "https://discord.gg/nywZ29w")
	em.set_image(url="https://i.imgur.com/VyRXaJw.png")
	await bot.send_message(msg.channel,mention_user(user.user_id)+" "+"너에게 직접 보낼거야! 확인해봐!")
	await bot.send_message(msg.author,embed=em)

async def credit_view(msg,user):
	chat_id = msg.channel.id
	now = log_append(chat_id, str(msg.content), "credit",0)
	text="QuadraEarsBotⓒKatinor, All Right Reserved.\n"
	text+=" https://blog.4ears.net/%EC%82%AC%EC%9E%BD%EC%9D%B4%EB%B4%87/ \n"
	text+=" katinor@4ears.net\n\n"
	text+="You can see source on GitHub. and also use under AGPLv3.0\n"
	text+=" https://github.com/Katinor/quadra_ears_bot_discord/\n\n"
	text+="Character Illustrated by 하얀로리, All Right Reserved.\n"
	text+=" https://www.pixiv.net/member.php?id=5882068 \n\n"
	text+="This bot use nekos.life API.\n"
	text+=" https://discord.services/api/"
	user.mody(love = 1, love_time = True, exp = 5, exp_time = True)
	em = discord.Embed(title="여길 누르면 블로그로 갈 수 있어!",description=text, colour=discord.Colour.blue(), url = "https://blog.4ears.net/%EC%82%AC%EC%9E%BD%EC%9D%B4%EB%B4%87/")
	em.set_image(url="https://i.imgur.com/VyRXaJw.png")
	await bot.send_message(msg.channel,mention_user(user.user_id)+" "+"너에게 직접 보낼거야! 확인해봐!")
	await bot.send_message(msg.author,embed=em)
	
async def lifetime(msg,user):
	chat_id = msg.channel.id
	now = log_append(chat_id, str(msg.content), "lifetime",0)
	user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
	text = mention_user(user.user_id)+" "+quadra_lifetime.checkSwitch(now)
	await bot.send_message(msg.channel,text)

async def dialog_how(msg,user):
	chat_id = msg.channel.id
	chat_from = user.user_id
	now = log_append(chat_id, str(msg.content), "d_how",0)
	target = re.search('^사잽아 ((?:(?! 어때).)*) 어때', str(msg.content))
	target = target.groups()
	user_list = msg.mentions
	
	if target[0] == "나":
		level_stat = user.level
		cash_stat = user.cash
		if level_stat == quadra_user_module.MAX_LEVEL:
			req_exp = quadra_user_module.REQ_EXP[level_stat-1] - quadra_user_module.REQ_EXP[level_stat-2]
			cur_exp = user.exp - quadra_user_module.REQ_EXP[level_stat-1]
		elif level_stat != 0 :
			req_exp = quadra_user_module.REQ_EXP[level_stat] - quadra_user_module.REQ_EXP[level_stat-1]
			cur_exp = user.exp - quadra_user_module.REQ_EXP[level_stat-1]
		else :
			req_exp = quadra_user_module.REQ_EXP[level_stat]
			cur_exp = user.exp
		if level_stat != quadra_user_module.MAX_LEVEL:
			exp_bar = ""
			exp_perc = (cur_exp / req_exp)
			exp_perc *= 100
			exp_perc_str = "(%3d %%)"%(exp_perc)
			for i in range(0,10,1):
				if exp_perc >= 10:
					exp_bar += "■"
					exp_perc -= 10
				else: exp_bar += "□"
			em = discord.Embed(title=msg.author.name+"#"+str(msg.author.discriminator)+" 의 프로필!",description="Lv."+str(level_stat)+" ( "+str(cur_exp)+" / "+str(req_exp)+" )\n"+exp_bar+exp_perc_str, colour=discord.Colour.blue())
		else : 
			em = discord.Embed(title=msg.author.name+"#"+str(msg.author.discriminator)+" 의 프로필!",description="Lv."+str(level_stat)+" ( "+str(cur_exp)+" )\n■■■■■■■■■■(최대레벨)", colour=discord.Colour.blue())
		if msg.author.avatar_url:	em.set_thumbnail(url=msg.author.avatar_url)
		else : em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
		em.add_field(name="돈", value=str(cash_stat), inline=True)
		em.add_field(name="호감도", value=user.love_short(), inline=True)
		if level_stat == 100: em.add_field(name="누적 경험치",value=str(user.exp),inline=False)
		else : em.add_field(name="누적 경험치",value=str(user.exp)+" / "+str(quadra_user_module.REQ_EXP[level_stat]),inline=False)
		await bot.send_message(msg.channel,mention_user(user.user_id)+",\n"+user.love_text(),embed = em)
	
	elif len(user_list) == 1 and user_list :
		trg_user = quadra_user(user_list[0].id)
		level_stat = trg_user.level
		cash_stat = trg_user.cash
		if level_stat == quadra_user_module.MAX_LEVEL:
			req_exp = quadra_user_module.REQ_EXP[level_stat-1] - quadra_user_module.REQ_EXP[level_stat-2]
			cur_exp = trg_user.exp - quadra_user_module.REQ_EXP[level_stat-1]
		elif level_stat != 0 :
			req_exp = quadra_user_module.REQ_EXP[level_stat] - quadra_user_module.REQ_EXP[level_stat-1]
			cur_exp = trg_user.exp - quadra_user_module.REQ_EXP[level_stat-1]
		else :
			req_exp = quadra_user_module.REQ_EXP[level_stat]
			cur_exp = trg_user.exp
		if level_stat != quadra_user_module.MAX_LEVEL:
			exp_bar = ""
			exp_perc = (cur_exp / req_exp)
			exp_perc *= 100
			exp_perc_str = "(%3d %%)"%(exp_perc)
			for i in range(0,10,1):
				if exp_perc >= 10:
					exp_bar += "■"
					exp_perc -= 10
				else: exp_bar += "□"
			em = discord.Embed(title=user_list[0].name+"#"+str(user_list[0].discriminator)+" 의 프로필!",description="Lv."+str(level_stat)+" ( "+str(cur_exp)+" / "+str(req_exp)+" )\n"+exp_bar+exp_perc_str, colour=discord.Colour.blue())
		else : 
			em = discord.Embed(title=user_list[0].name+"#"+str(user_list[0].discriminator)+" 의 프로필!",description="Lv."+str(level_stat)+" ( "+str(cur_exp)+" )\n■■■■■■■■■■(최대레벨)", colour=discord.Colour.blue())
		if user_list[0].avatar_url:	em.set_thumbnail(url=user_list[0].avatar_url)
		else : em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
		em.add_field(name="돈", value=str(cash_stat), inline=True)
		em.add_field(name="호감도", value=trg_user.love_short(), inline=True)
		if level_stat == 100: em.add_field(name="누적 경험치",value=str(trg_user.exp),inline=False)
		else : em.add_field(name="누적 경험치",value=str(trg_user.exp)+" / "+str(quadra_user_module.REQ_EXP[level_stat]),inline=False)
		await bot.send_message(msg.channel,mention_user(user.user_id)+", "+user_list[0].name+"#"+str(user_list[0].discriminator)+"에 대해서 묻는거지?",embed = em)
	elif target[0] in quadra_search_vocab.dis_list: 
		text=random.choice(quadra_dialog_list.dialog_dis_how)
		user.mody(love = 2, love_time = True, exp = 5, exp_time = True)
		await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)
	elif target[0] in quadra_search_vocab.adult_list:
		text=random.choice(quadra_dialog_list.dialog_hentai_how)
		inc = - 10 - 5*(quadra_user_module.MAX_LOVE - quadra_user_module.MIN_LOVE - user.love) / (quadra_user_module.MAX_LOVE-quadra_user_module.MIN_LOVE)
		user.mody(love = inc, exp = 5, exp_time = True)
		await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)
	elif target[0] in quadra_dialog_list.dialog_how_list:
		text=random.choice(quadra_dialog_list.dialog_how_list[target[0]])
		user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
		await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)
	else:
		text="미안. 무슨 말인지 모르겠어."
		user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
		await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)

async def dialog_buy(msg,user):
	chat_id = msg.channel.id
	chat_from = msg.author.id
	now = log_append(chat_id, str(msg.content), "d_buy",0)
	text = mention_user(user.user_id)+", "
	target = re.search('^사잽아 ((?:(?! 사줘).)*) 사줘', str(msg.content))
	target = target.groups()
	if target[0] in quadra_search_vocab.dis_list: 
		text += random.choice(quadra_dialog_list.dialog_dis_buy)
		user.mody(love = 2,love_time = True, exp = 5, exp_time = True)
	elif target[0] in quadra_search_vocab.adult_list:
		text += random.choice(quadra_dialog_list.dialog_hentai_buy)
		inc = - 10 - 5*(quadra_user_module.MAX_LOVE - quadra_user_module.MIN_LOVE - user.love) / (quadra_user_module.MAX_LOVE-quadra_user_module.MIN_LOVE)
		user.mody(love = inc, exp = 5, exp_time = True)
	elif target[0] in quadra_dialog_list.dialog_buy_list:
		text += random.choice(quadra_dialog_list.dialog_buy_list[target[0]])
		user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
	else:
		text += "그건 니돈으로 사는게 어때?"
		user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
	await bot.send_message(msg.channel,text)

async def dialog_please(msg,user):
	chat_id = msg.channel.id
	now = log_append(chat_id, str(msg.content), "d_plz",0)
	target = re.search('^사잽아 ((?:(?! (해줘|할래)).)*) (해줘|할래)', str(msg.content))
	target = target.groups()
	
	if target[0] == "자동로또":
		game_name = onGame(user.user_id)
		if game_name == "로또를":
			user_in = [10,10,10,10,10,10]
			for i in range(0,6,1):
				swt = True
				while(swt):
					temp = random.randrange(1,36)
					if temp in user_in:
						continue
					else:
						user_in[i] = temp
						swt = False
			user_in.sort()
			data = quadra_lotto.check(user.user_id)
			result = quadra_lotto.gameManager(user_in,data[0],data[1])
			user_in_text = ""
			for i in user_in:
				user_in_text += str(i)+" "
			log_append(chat_id,"player : "+user_in_text, "lt","p_at")
			text2 = mention_user(user.user_id)+", "
			text = ""
			for i in data[0]:
				text += str(i)+" "
			comp_in_text = text+": "+str(data[1])
			log_append(chat_id,"rank "+str(result)+", answer is "+text+": "+str(data[1]), "lt","p_cor")
			dif_cash = 0
			dif_love = 0
			dif_exp = 0
			if result == 1:
				text2 += "1등이네! 축하해!! 8,145,060 분의 1의 확률인데, 너무 대단한걸?"
				dif_love = 10
				dif_exp = 100
				dif_cash = 2500000000
			elif result == 2:
				text2 += "2등이야. 1등이 아니라 아쉽겠지만, 그래도 축하해!"
				dif_love = 5
				dif_exp = 50
				dif_cash = 10000000
			elif result == 3:
				text2 += "3등. 이정도면 꽤나 운이 좋은걸?"
				dif_love = 4
				dif_exp = 25
				dif_cash = 3000000
			elif result == 4:
				text2 += "4등. 733명 중 한명. 축하해."
				dif_love = 3
				dif_exp = 25
				dif_cash = 50000
			elif result == 5:
				dif_love = 2
				dif_exp = 25
				dif_cash = 5000
				text2 += "5등. 45명중의 한명이야. 그래도 본전은 뽑았을려나?"
			else: text2 += "지나친 도박은 좋지 않다구. 결국 다 잃어버리잖아.."
			em = discord.Embed(title=msg.author.name+"#"+str(msg.author.discriminator)+" 의 로또 결과!",colour=discord.Colour.blue())
			if msg.author.avatar_url: em.set_thumbnail(url=msg.author.avatar_url)
			else : em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
			em.add_field(name="방식",value="자동",inline=True)
			if result <= 5: em.add_field(name="등수",value=str(result)+"등",inline=True)
			else : em.add_field(name="등수",value="--",inline=True)
			em.add_field(name="당첨금",value=str(dif_cash)+" 원",inline=False)
			em.add_field(name="플레이어", value=user_in_text, inline=False)
			em.add_field(name="당첨번호", value=comp_in_text, inline=False)
			await bot.send_message(msg.channel,text2,embed = em)
			quadra_lotto.end(user.user_id)
			user.mody(love = dif_love, exp = dif_exp, cash = dif_cash)
		else: 
			log_append(chat_id,"there are no game playing", "gm","p_no")
			await bot.send_message(msg.channel,mention_user(user.user_id)+", 게임을 안하고 있는것같은데?")

	elif target[0] in quadra_search_vocab.dis_list: 
		out_text = random.choice(quadra_dialog_list.dialog_dis_please)
		user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
		await bot.send_message(msg.channel,mention_user(user.user_id)+", "+out_text)
	elif target[0] in quadra_search_vocab.adult_list:
		out_text = random.choice(quadra_dialog_list.dialog_hentai_please)
		inc = -10-5*(quadra_user_module.MAX_LOVE - quadra_user_module.MIN_LOVE - user.love) / (quadra_user_module.MAX_LOVE-quadra_user_module.MIN_LOVE)
		user.mody(love = inc, exp = 5, exp_time = True)
		await bot.send_message(msg.channel,mention_user(user.user_id)+", "+out_text)
	elif target[0] in quadra_dialog_list.dialog_please_list:
		out_text = random.choice(quadra_dialog_list.dialog_please_list[target[0]])
		user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
		await bot.send_message(msg.channel,mention_user(user.user_id)+", "+out_text)
	else:
		out_text = "미안. 뭘 해달라는건지 모르겠어."
		user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
		await bot.send_message(msg.channel,mention_user(user.user_id)+", "+out_text)

async def dialog_do(msg,user):
	chat_id = msg.channel.id
	target = re.search('^사잽아 ((?:(?! 하자).)*) 하자', str(msg.content))
	target = target.groups()
	
	if target[0] == "야구게임":
		if onGame(user.user_id) == "야구게임을":
			await bot.send_message(msg.channel,mention_user(user.user_id)+", 이미 플레이중인거 같은데?\n3자리 수를 생각해서 \"사잽아 ~ 맞아?\" 라고 말해줘.\n그만하고 싶다면 \"사잽아 그만할래\"라고 말해줘.")
		elif onGame(user.user_id) !="" :
			out_text=mention_user(user.user_id)+", 이미 "+onGame(user.user_id)+" 플레이중인거 같은데?"
			await bot.send_message(msg.channel,out_text)
		else:
			now = log_append(chat_id,str(msg.content), "bb","start1")
			temp = quadra_baseball.start(user.user_id)
			now = log_append(chat_id,str(user.user_id)+" "+str(temp), "bb","start2")
			out_text=mention_user(user.user_id)+", 좋아! 이제 시작해보자~\n \"사잽아 ~ 맞아?\" 라고 말해줘!\n그만하고 싶다면 \"사잽아\ 그만할래\"라고 말해줘!"
			await bot.send_message(msg.channel,out_text)

	elif target[0] == "업다운":
		if onGame(user.user_id) == "업다운을":
			out_text=mention_user(user.user_id)+", 이미 플레이중인거 같은데?\n3자리 수를 생각해서 \"사잽아 ~ 맞아?\" 라고 말해줘.\n그만하고 싶다면 \"사잽아 그만할래\"라고 말해줘."
			await bot.send_message(msg.channel,out_text)
		elif onGame(user.user_id)!= "" :
			out_text=mention_user(user.user_id)+", 이미 "+onGame(user.user_id)+" 플레이중인거 같은데?"
			await bot.send_message(msg.channel,out_text)
		else:
			now = log_append(chat_id, str(msg.content), "ud","start1")
			temp = quadra_updown.start(user.user_id)
			now = log_append(chat_id,str(user.user_id)+" "+str(temp), "ud","start2")
			out_text=mention_user(user.user_id)+", 좋아! 이제 시작해보자~\n \"사잽아 ~ 맞아?\" 라고 말해줘!\n그만하고 싶다면 \"사잽아 그만할래\"라고 말해줘!"
			await bot.send_message(msg.channel,out_text)

	elif target[0] == "로또":
		if onGame(user.user_id) == "로또를":
			out_text=mention_user(user.user_id)+", 이미 플레이중인거 같은데?\n1부터 35까지의 수 중 6개를 골라서 \"사잽아 ~ 맞아?\" 라고 말해줘. 예를 들면 \"사잽아 1 3 4 16 21 34 맞아?\" 느낌으로 써주면 돼!\n그만하고 싶다면 \"사잽아 그만할래\"라고 말해줘.\n\"사잽아 자동로또 해줘\"라고 말하면 자동으로 해볼게!."
			await bot.send_message(msg.channel,out_text)
		elif onGame(user.user_id)!= "" :
			out_text=mention_user(user.user_id)+", 이미 "+onGame(user.user_id)+" 플레이중인거 같은데?"
			await bot.send_message(msg.channel,out_text)
		else:
			if user.cash >= LOTTO_CHARGE :
				
				now = log_append(chat_id, str(msg.content), "lt","start1")
				temp = quadra_lotto.start(user.user_id)
				now = log_append(chat_id,str(user.user_id)+" "+str(temp), "lt","start2")
				out_text=mention_user(user.user_id)+", 좋아! 이제 시작해보자~\n 1부터 35까지의 수 중 6개를 골라서 \"사잽아 ~ 맞아?\" 라고 말해줘. 예를 들면 \"사잽아 1 3 4 16 21 34 맞아?\" 느낌으로 써주면 돼!\n그만하고 싶다면 \"사잽아 그만할래\"라고 말해줘!\n\"사잽아 자동로또 해줘\"라고 말하면 자동으로 해볼게!."
				em = discord.Embed(title=msg.author.name+"#"+str(msg.author.discriminator)+", 로또 구매 영수증이야!",colour=discord.Colour.blue())
				if msg.author.avatar_url:	em.set_thumbnail(url=msg.author.avatar_url)
				else : em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
				past_cash = user.cash
				user.mody(cash = (-1)*LOTTO_CHARGE)
				future_cash = user.cash
				em.add_field(name="사용전", value=str(past_cash), inline=True)
				em.add_field(name="비용", value="1000", inline=True)
				em.add_field(name="사용후", value=str(future_cash), inline=True)
				await bot.send_message(msg.channel,out_text,embed = em)
			else:
				now = log_append(chat_id,str(user.user_id)+" don't have enough money", "lt","nocs")
				out_text=mention_user(user.user_id)+", 로또를 하려면 1000원이 필요해!"
				await bot.send_message(msg.channel,out_text)

	else:
		log_append(chat_id, str(msg.content), "d_do",0)
		if target[0] in quadra_search_vocab.dis_list: 
			out_text=mention_user(user.user_id)+", "+random.choice(quadra_dialog_list.dialog_dis_do)
			await bot.send_message(msg.channel,out_text)
			user.mody(love = 2,love_time = True, exp = 5, exp_time = True)
		elif target[0] in quadra_search_vocab.adult_list:
			out_text=mention_user(user.user_id)+", "+random.choice(quadra_dialog_list.dialog_hentai_do)
			await bot.send_message(msg.channel,out_text)
			inc = - 10 - 5*(quadra_user_module.MAX_LOVE - quadra_user_module.MIN_LOVE - user.love) / (quadra_user_module.MAX_LOVE-quadra_user_module.MIN_LOVE)
			user.mody(love = inc, exp = 1, exp_time = True)
		elif target[0] in quadra_dialog_list.dialog_do_list:
			out_text=mention_user(user.user_id)+", "+random.choice(quadra_dialog_list.dialog_do_list[target[0]])
			await bot.send_message(msg.channel,out_text)
			user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
		else:
			out_text=mention_user(user.user_id)+", 미안. 뭘 하자는건지 모르겠어."
			user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
			await bot.send_message(msg.channel,out_text)

async def game_prog(msg,user):
	chat_id = msg.channel.id
	now = log_append(chat_id, str(msg.content), "gm","prog")
	game_name = onGame(user.user_id)
	if game_name == "야구게임을":
		target = re.search('^사잽아 ((?:(?! 맞아\?).)*) 맞아\?', str(msg.content))
		target = target.groups()
		if len(target[0]) != 3:
			log_append(chat_id,"you have to give answer 000 ~ 999", "bb","p_e1")
			out_text = mention_user(user.user_id)
			out_text+=", 혹시 하는말인데, 수는 3자리로 써야해. 까먹은건 아니지?\n그만하고 싶다면 \"사잽아 그만할래\"라고 말해줘!"
			await bot.send_message(msg.channel,out_text)
		else:
			data = quadra_baseball.check(user.user_id)
			temp_bool = quadra_baseball.check_equal(int(target[0]))
			if temp_bool:
				result = quadra_baseball.gameManager(int(target[0]),int(data[0]))
				data[0] = int(data[0])
				if result[0] == 3:
					log_append(chat_id,"answer is "+str(data[0]), "bb","p_cor")
					out_text=mention_user(user.user_id)+", 정답이야! "+str(int(data[1])+1)+"번만에 맞췄는걸!"
					quadra_baseball.end(user.user_id)
					em = discord.Embed(title=msg.author.name+"#"+str(msg.author.discriminator)+" 의 야구게임 결과!",colour=discord.Colour.blue())
					if msg.author.avatar_url:	em.set_thumbnail(url=msg.author.avatar_url)
					else : em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
					em.add_field(name="횟수", value=str(int(data[1])+1)+"회", inline=True)
					em.add_field(name="답안", value=target[0], inline=True)
					em.add_field(name="결과", value="게임 성공!", inline=False)
					temp_num = int(data[1])+1
					inc = 0
					if temp_num < 4 :
						inc = 100
						dif_love = 4
					elif temp_num < 6 :
						inc = 90
						dif_love = 3
					elif temp_num < 8 :
						inc = 75
						dif_love = 3
					elif temp_num < 11 :
						inc = 60
						dif_love = 2
					else:
						inc = 50
						dif_love = 1
					em.add_field(name="획득 경험치", value=str(inc), inline=False)
					await bot.send_message(msg.channel,out_text,embed = em)
					user.mody(love = dif_love, exp = inc)
				else:
					log_append(chat_id,str(result[0])+"-"+str(result[1])+", answer is "+str(data[0]), "bb","p_no")
					out_text=mention_user(user.user_id)+", 잘하고 있어! \n그만하고 싶다면 \"사잽아 그만할래\"라고 말해줘!"
					quadra_baseball.lose(user.user_id)
					em = discord.Embed(title=msg.author.name+"#"+str(msg.author.discriminator)+" 의 야구게임 결과!",colour=discord.Colour.blue())
					if msg.author.avatar_url:	em.set_thumbnail(url=msg.author.avatar_url)
					else : em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
					strike = int(result[0])
					ball = int(result[1])
					result_view = "S "
					for i in range(0,2,1):
						if strike > 0:
							strike -= 1
							result_view += '●'
						else : result_view += '○'
					result_view += "\nB "
					for i in range(0,3,1):
						if ball > 0:
							ball -= 1
							result_view += '●'
						else : result_view += '○'
					result_view += "\n ( "+str(result[0])+" - " + str(result[1]) + " )"
					em.add_field(name="횟수", value=str(int(data[1])+1)+"회", inline=True)
					em.add_field(name="답안", value=target[0], inline=True)
					em.add_field(name="결과", value=result_view, inline=False)
					await bot.send_message(msg.channel,out_text,embed = em)
			else:
				log_append(chat_id,"there are duplication", "bb","p_e2")
				out_text = mention_user(user.user_id)
				out_text+=", 혹시 하는말인데, 각 자리수에 같은 숫자가 들어가면 안돼. 까먹은건 아니지?\n그만하고 싶다면 \"사잽아 그만할래\"라고 말해줘!"
				await bot.send_message(msg.channel,out_text)
	elif game_name == "업다운을":
		target = re.search('^사잽아 ((?:(?! 맞아\?).)*) 맞아\?', str(msg.content))
		target = target.groups()
		if int(target[0]) < 0 or int(target[0]) > 100:
			log_append(chat_id,"you have to give answer 000 ~ 99", "ud","p_e1")
			out_text=mention_user(user.user_id)+", 혹시 하는말인데, 수는 100 미만의 자연수로 써야해. 까먹은건 아니지?\n그만하고 싶다면 \"사잽아 그만할래\"라고 말해줘!"
			await bot.send_message(msg.channel,out_text)
		else:
			data = quadra_updown.check(user.user_id)
			result = quadra_updown.gameManager(int(target[0]),int(data[0]))
			if result == 0:
				log_append(chat_id,"answer is "+str(data[0]), "ud","p_cor")
				out_text=mention_user(user.user_id)+", 정답이야! "+str(int(data[1])+1)+"번만에 맞췄는걸!"
				quadra_updown.end(user.user_id)
				
				em = discord.Embed(title=msg.author.name+"#"+str(msg.author.discriminator)+" 의 업다운 결과!",colour=discord.Colour.blue())
				if msg.author.avatar_url:	em.set_thumbnail(url=msg.author.avatar_url)
				else : em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
				em.add_field(name="회차", value=str(int(data[1])+1)+"회", inline=True)
				em.add_field(name="답안", value=str(int(target[0])), inline=True)
				em.add_field(name="결과", value="정답!", inline=False)
				temp_num = int(data[1])+1
				inc = 0
				if temp_num < 4 :
					inc = 75
					dif_love = 3
				elif temp_num < 6 :
					inc = 65
					dif_love = 3
				elif temp_num < 8 :
					inc = 60
					dif_love = 2
				else:
					inc = 50
					dif_love = 1
				em.add_field(name="획득 경험치", value=str(inc), inline=False)
				await bot.send_message(msg.channel,out_text,embed = em)
				user.mody(love = dif_love, exp = inc)

			elif result == 1:
				log_append(chat_id,"down, answer is "+str(data[0]), "ud","p_no")
				out_text=mention_user(user.user_id)+", 다운! 정답은 그거보다 낮은 수야! 이번이 "+str(int(data[1])+1)+"번째야!\n그만하고 싶다면 \"사잽아 그만할래\"라고 말해줘!"
				em = discord.Embed(title=msg.author.name+"#"+str(msg.author.discriminator)+" 의 업다운 결과!",colour=discord.Colour.blue())
				if msg.author.avatar_url:	em.set_thumbnail(url=msg.author.avatar_url)
				else : em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
				em.add_field(name="회차", value=str(int(data[1])+1)+"회", inline=True)
				em.add_field(name="답안", value=str(int(target[0])), inline=True)
				em.add_field(name="결과", value="다운! (정답은 더 낮은수!)", inline=False)
				await bot.send_message(msg.channel,out_text,embed = em)
				quadra_updown.lose(user.user_id)

			elif result == -1:
				log_append(chat_id,"up, answer is "+str(data[0]), "ud","p_no")
				out_text=mention_user(user.user_id)+", 업! 정답은 그거보다 높은 수야! 이번이 "+str(int(data[1])+1)+"번째야!\n그만하고 싶다면 \"사잽아 그만할래\"라고 말해줘!"
				em = discord.Embed(title=msg.author.name+"#"+str(msg.author.discriminator)+" 의 업다운 결과!",colour=discord.Colour.blue())
				if msg.author.avatar_url:	em.set_thumbnail(url=msg.author.avatar_url)
				else : em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
				em.add_field(name="회차", value=str(int(data[1])+1)+"회", inline=True)
				em.add_field(name="답안", value=str(int(target[0])), inline=True)
				em.add_field(name="결과", value="업! (정답은 더 높은수!)", inline=False)
				await bot.send_message(msg.channel,out_text,embed = em)
				quadra_updown.lose(user.user_id)
	elif game_name == "로또를":
		target = re.search('^사잽아 ((?:(?! 맞아\?).)*) 맞아\?', str(msg.content))
		target = target.groups()
		temp1 = target[0].split(" ")
		user_in = []
		swt = 0
		for i in temp1:
			user_in.append(int(i))
		if len(user_in) != 6 :
			log_append(chat_id,"you have to give answer 6 prices", "lt","p_e1")
			out_text=mention_user(user.user_id)+", 혹시 하는말인데, 로또는 6개의 수로 하는거야. 까먹은건 아니지?\n예를 들면 \"사잽아 1 3 4 16 21 34 맞아?\" 느낌으로 써주면 돼!\n그만하고 싶다면 \"사잽아 그만할래\"라고 말해줘!"
			swt = 1
			await bot.send_message(msg.channel,out_text)
		elif quadra_lotto.check_equal(user_in) == False:
			log_append(chat_id,"there are duplicated", "lt","p_e2")
			out_text=mention_user(user.user_id)+", 혹시 하는말인데, 각각의 수는 달라야 해.\n예를 들면 \"사잽아 1 3 4 16 21 34 맞아?\" 느낌으로 써주면 돼!\n그만하고 싶다면 \"사잽아 그만할래\"라고 말해줘!"
			swt = 1
			await bot.send_message(msg.channel,out_text)
		else:
			for i in user_in:
				if i < 1 or i > 35:
					swt = 1
					log_append(chat_id,"you have to give answer 1 ~ 35", "lt","p_e3")
					out_text=mention_user(user.user_id)+", 혹시 하는말인데, 각각의 번호는 1~35 중의 수로 써야해. 까먹은건 아니지?\n그만하고 싶다면 \"사잽아 그만할래\"라고 말해줘!"
					await bot.send_message(msg.channel,out_text)
		if swt == 0:
			data = quadra_lotto.check(user.user_id)
			result = quadra_lotto.gameManager(user_in,data[0],data[1])
			user_in_text = ""
			for i in user_in:
				user_in_text += str(i)+" "
			text2 = mention_user(user.user_id)+", "
			text = ""
			for i in data[0]:
				text += str(i)+" "
			comp_in_text = text+": "+str(data[1])
			log_append(chat_id,"rank "+str(result)+", answer is "+text+": "+str(data[1]), "lt","p_cor")
			dif_cash = 0
			dif_love = 0
			dif_exp = 0
			if result == 1:
				text2 += "1등이네! 축하해!! 8,145,060 분의 1의 확률인데, 너무 대단한걸?"
				dif_love = 10
				dif_exp = 100
				dif_cash = 2500000000
			elif result == 2:
				text2 += "2등이야. 1등이 아니라 아쉽겠지만, 그래도 축하해!"
				dif_love = 5
				dif_exp = 50
				dif_cash = 10000000
			elif result == 3:
				text2 += "3등. 이정도면 꽤나 운이 좋은걸?"
				dif_love = 4
				dif_exp = 25
				dif_cash = 3000000
			elif result == 4:
				text2 += "4등. 733명 중 한명. 축하해."
				dif_love = 3
				dif_exp = 25
				dif_cash = 50000
			elif result == 5:
				dif_love = 2
				dif_exp = 25
				dif_cash = 5000
				text2 += "5등. 45명중의 한명이야. 그래도 본전은 뽑았을려나?"
			else: text2 += "지나친 도박은 좋지 않다구. 결국 다 잃어버리잖아.."
			em = discord.Embed(title=msg.author.name+"#"+str(msg.author.discriminator)+" 의 로또 결과!",colour=discord.Colour.blue())
			if msg.author.avatar_url: em.set_thumbnail(url=msg.author.avatar_url)
			else : em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
			em.add_field(name="방식",value="수동",inline=True)
			if result <= 5: em.add_field(name="등수",value=str(result)+"등",inline=True)
			else : em.add_field(name="등수",value="--",inline=True)
			em.add_field(name="당첨금",value=str(dif_cash)+" 원",inline=False)
			em.add_field(name="플레이어", value=user_in_text, inline=False)
			em.add_field(name="당첨번호", value=comp_in_text, inline=False)
			await bot.send_message(msg.channel,text2,embed = em)
			quadra_lotto.end(user.user_id)
			user.mody(love = dif_love, exp = dif_exp, cash = dif_cash)
	else: 
		log_append(chat_id,"there are no game playing", "gm","p_no")
		out_text=mention_user(user.user_id)+", 게임을 안하고 있는것같은데?"
		await bot.send_message(msg.channel,out_text)

async def game_end(msg,user):
	chat_id = msg.channel.id
	now = log_append(chat_id, str(msg.content), "bb","end")
	out_text = mention_user(user.user_id)+", "
	game_name = onGame(user.user_id)
	if game_name == "야구게임을":
		data = quadra_baseball.check(user.user_id)
		data[0] = int(data[0])
		log_append(chat_id,"answer is "+str(data[0]), "bb","end2")
		out_text += "야구게임을 그만하려고? 하는수없지. 정답은 "+str(data[0])+"이었고, 너는 "+str(data[1])+"번 시도했어!"
		quadra_baseball.end(user.user_id)
	elif game_name == "업다운을":
		data = quadra_updown.check(user.user_id)
		log_append(chat_id,"answer is "+str(data[0]), "ud","end2")
		out_text += "업다운을 그만하려고? 하는수없지. 정답은 "+str(data[0])+"이었고, 너는 "+str(data[1])+"번 시도했어!"
		quadra_updown.end(user.user_id)
	elif game_name == "로또를":
		data = quadra_lotto.check(user.user_id)
		text = ""
		for i in data[0]:
			text += str(i)+" "
		log_append(chat_id,"answer is "+text+": "+str(data[1]), "lt","p_cor")
		text2 = " 정답은 "+text+" 에 보너스번호 "+str(data[1])+" 이었어!"
		log_append(chat_id,"answer is "+str(data[0]), "lt","end2")
		out_text += "로또를 그만하려고? 하는수없지."+text2
		quadra_lotto.end(user.user_id)
	else:
		log_append(chat_id,str(user.user_id)+" isn't playing baseball", "gm","e_e")
		out_text += "애초에 안하고 있었던 것 같은데.. 게임을 하고 싶다면 먼저 \"사잽아 (게임이름) 하자\" 라고 말해줘!"
	await bot.send_message(msg.channel,out_text)

async def get_supply(msg,user):
	chat_id = msg.channel.id
	now = log_append(chat_id, str(msg.content), "bb","end")
	if user.canSupply():
		out_text = mention_user(user.user_id)+", "+user.supply_text()
		inc_array = [1000,5000,10000,12000,15000,20000,30000]
		past_cash = user.cash
		inc = inc_array[user.love_level()-1]
		user.mody(cash = inc, cash_time=True)
		future_cash = user.cash
		em = discord.Embed(title=msg.author.name+"#"+str(msg.author.discriminator)+", 지원금 수령 완료!",colour=discord.Colour.blue())
		if msg.author.avatar_url:	em.set_thumbnail(url=msg.author.avatar_url)
		else : em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
		em.add_field(name="수령전", value=str(past_cash), inline=True)
		em.add_field(name="지원금", value=str(inc), inline=True)
		em.add_field(name="수령후", value=str(future_cash), inline=True)
		await bot.send_message(msg.channel,out_text,embed = em)
	else:
		out_text = mention_user(user.user_id)+", 내일 다시 와줘!"
		await bot.send_message(msg.channel,out_text)
	
async def searching(msg,user):
	chat_id = msg.channel.id
	target = re.search('^사잽아 (?:((?:(?!에서).)*)에서 )?((?:(?! (알려줘|찾아줘)).)*) (알려줘|찾아줘)', str(msg.content))
	target = target.groups()
	if target[0] == '스팀':
		search_target = target[1].lower()
		term_switch = 0
		game_dict = quadra_game_list.game_synonym.items()
		for i in game_dict :
			if search_target in i[1]:
				term_switch = 1
				game_real_name = i[0]
			if search_target == i[0]:
				term_switch = 1
				game_real_name = i[0]
		if term_switch == 0:
			now = log_append(chat_id, str(msg.content), "sch", "g_e")
			text="미안해. 무슨 게임인지 잘 몰라서 대신 검색해줄게! ( " + quadra_search_list.search_engine["스팀"] + url_encode(target[1]) + " )"
			user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
		else : 
			now = log_append(chat_id, str(msg.content), "sch", "g")
			game_target = quadra_game_list.game_number[game_real_name]
			if game_target[0] == 0:
				text="혹시 이 게임 찾으려는거 맞아? ( " + quadra_game_list.steam_shop+game_target[1] + " )"
				user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
			else :
				text=game_target[0]+" ( " + quadra_game_list.steam_shop+game_target[1] + " )"
				user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
	elif target[0] in quadra_search_list.search_engine:
		if target[1] in quadra_search_vocab.adult_list:
			now = log_append(chat_id, str(msg.content), "sch", "ad")
			text="변태.. 이런거까지 찾아줘야해? ( " + quadra_search_list.search_engine[target[0]] + url_encode(target[1]) + " )"
			inc = - 5 - 5*(quadra_user_module.MAX_LOVE - quadra_user_module.MIN_LOVE - user.love) / (quadra_user_module.MAX_LOVE-quadra_user_module.MIN_LOVE)
			user.mody(love = inc, exp = 5, exp_time = True)
		elif target[1] in quadra_search_vocab.dis_list:
			now = log_append(chat_id, str(msg.content), "sch", "dis")
			text="... 이런걸 생각중이라면 그만둬. ..내가 너랑 함께 있어줄테니까. ( " + quadra_search_list.search_engine[target[0]] + url_encode(target[1]) + " )"
			user.mody(love = 2,love_time = True, exp = 5, exp_time = True)
		elif target[1] in quadra_search_vocab.wonder_list:
			now = log_append(chat_id, str(msg.content), "sch", "won")
			text=quadra_search_vocab.wonder_list[target[1]] + " ( " + quadra_search_list.search_engine[target[0]] + url_encode(target[1]) + " )"
			user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
		else:
			now = log_append(chat_id, str(msg.content), "sch", 0)
			text="이거 찾으려는거 맞지? ( " + quadra_search_list.search_engine[target[0]] + url_encode(target[1]) + " )"
			user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
	elif target[1] in quadra_search_list.hentai_url:
		now = log_append(chat_id, str(msg.content), "sch", "d_ad")
		text="너는 정말 최악의 변태구나.. 자, 여깄어. ( " + quadra_search_list.hentai_url[target[1]] + " )"
		inc = - 5 - 5*(quadra_user_module.MAX_LOVE - quadra_user_module.MIN_LOVE - user.love) / (quadra_user_module.MAX_LOVE-quadra_user_module.MIN_LOVE)
		user.mody(love = inc, exp = 5, exp_time = True)
	elif target[1] in quadra_search_list.direct_url:
		now = log_append(chat_id, str(msg.content), "sch", "d")
		text="거기라면 나도 알고있어! 바로 보내줄께! ( " + quadra_search_list.direct_url[target[1]] + " )"
		user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
	else:
		if target[1] in quadra_search_vocab.adult_list:
			now = log_append(chat_id, str(msg.content), "sch", "n_ad")
			text=target[1] + "라니... 변태! 이런거까지 찾아줘야해? ( " + quadra_search_list.search_engine["구글"] + url_encode(target[1]) + " )"
			inc = - 5 - 5*(quadra_user_module.MAX_LOVE - quadra_user_module.MIN_LOVE - user.love) / (quadra_user_module.MAX_LOVE-quadra_user_module.MIN_LOVE)
			user.mody(love = inc, exp = 5, exp_time = True)
		elif target[1] in quadra_search_vocab.dis_list:
			now = log_append(chat_id, str(msg.content), "sch", "n_dis")
			text=target[1] + "같은걸 생각중이라면 그만둬. ..내가 너랑 함께 있어줄테니까. ( " + quadra_search_list.search_engine['구글'] + url_encode( target[1]) + " )"
			user.mody(love = 2,love_time = True, exp = 5, exp_time = True)
		elif target[1] in quadra_search_vocab.wonder_list:
			now = log_append(chat_id, str(msg.content), "sch", "n_won")
			text=quadra_search_vocab.wonder_list[target[1]] + " ( " + quadra_search_list.search_engine['구글'] + url_encode(target[1]) + " )"
			user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
		else:
			now = log_append(chat_id, str(msg.content), "sch", "n")
			text="이거 찾으려는거 맞지? ( " + quadra_search_list.search_engine["구글"] + url_encode(target[1]) + " )"
			user.mody(love = 1,love_time = True, exp = 5, exp_time = True)	
	await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)

async def neko_search(msg,user):
	now = log_append(msg.channel.id, str(msg.content), "neko",0)
	r = requests.get("https://nekos.life/api/v2/img/neko")
	r = r.text
	data = json.loads(r)
	file = data["url"]
	embed=discord.Embed(title="")
	embed.set_image(url=file)
	user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
	await bot.send_message(msg.channel, embed=embed)

async def neko_lewd_search(msg,user):
	now = log_append(msg.channel.id, str(msg.content), "neko",0)
	r = requests.get("https://nekos.life/api/v2/img/lewd")
	r = r.text
	data = json.loads(r)
	file = data["url"]
	embed=discord.Embed(title="")
	embed.set_image(url=file)
	user.mody(love = 1,love_time =True, exp = 5, exp_time = True)
	await bot.send_message(msg.channel, embed=embed)

async def dialog_lone(msg,user):
	chat_id = msg.channel.id
	chat_from = msg.author.id
	now = log_append(chat_id, str(msg.content), "d_lone",0)
	text = mention_user(user.user_id)+", "
	text += random.choice(quadra_dialog_list.dialog_lone_list)
	user.mody(love = 2,love_time = True, exp = 5, exp_time = True)
	await bot.send_message(msg.channel,text)	

async def memo_append(msg,user):
	chat_id = msg.channel.id
	chat_from = msg.author.id
	now = log_append(chat_id, str(msg.content), "mm_add",0)
	text = mention_user(user.user_id)+", "
	target = re.search('^사잽아 ((?:(?! 기억해줘).)*) 기억해줘', str(msg.content))
	target = target.groups()
	memo_status = quadra_memo(user.user_id)
	temp_swt = memo_status.append(str(target[0]))
	if temp_swt == 0:
		text += "메모로 기록할께! "+str(memo_status.memo_num + 1)+"번째 메모야!"
		now = log_append(chat_id, "add success! : current num = "+str(memo_status.memo_num + 1), "mm_add",0)
		await bot.send_message(msg.channel,text)
	if temp_swt == 1:
		text += "너무 길어서 기억 못하겠어!"
		now = log_append(chat_id, "add failed! : string stack overflow", "mm_add",0)
		await bot.send_message(msg.channel,text)
	if temp_swt == 2:
		text += "이미 너무 많이 기억하고있어!"
		now = log_append(chat_id, "add failed! : capacity stack overflow", "mm_add",0)
		await bot.send_message(msg.channel,text)
	if temp_swt == 3:
		text += "이상한게 끼여있어서 못기억하겠어!"
		now = log_append(chat_id, "add failed! : forbidden string included", "mm_add",0)
		await bot.send_message(msg.channel,text)

async def memo_delete(msg,user):
	chat_id = msg.channel.id
	chat_from = msg.author.id
	now = log_append(chat_id, str(msg.content), "mm_del",0)
	text = mention_user(user.user_id)+", "
	target = re.search('^사잽아 ((?:(?! 잊어줘).)*) 잊어줘', str(msg.content))
	target = target.groups()
	memo_status = quadra_memo(user.user_id)
	if target[0] == "전부":
		temp_swt = memo_status.purge()
		if temp_swt == 0:
			text += "메모를 전부 지웠어!"
			now = log_append(chat_id, "purge success!", "mm_del",0)
			await bot.send_message(msg.channel,text)
		if temp_swt == 1:
			text += "메모가 없어!"
			now = log_append(chat_id, "purge failed! : index out of range", "mm_del",0)
			await bot.send_message(msg.channel,text)
	else:
		target = (target[0].split('번'))[0]
		try : temp_swt = memo_status.delete(int(target))
		except Exception as ex: temp_swt = 3
		if temp_swt == 0:
			text += "메모를 지웠어! "+str(memo_status.memo_num - 1)+"개의 메모가 남아있어!"
			now = log_append(chat_id, "del success! : current num = "+str(memo_status.memo_num - 1), "mm_del",0)
			await bot.send_message(msg.channel,text)
		if temp_swt == 1:
			text += "그정도로 많이 기억하고 있진 않아!"
			now = log_append(chat_id, "del failed! : capacity stack overflow", "mm_del",0)
			await bot.send_message(msg.channel,text)
		if temp_swt == 2:
			text += "그런 번호는 없다구!"
			now = log_append(chat_id, "del failed! : num must be at least 1", "mm_del",0)
			await bot.send_message(msg.channel,text)
		if temp_swt == 3:
			text += "뭘 잊어달라는건지 모르겠어!"
			now = log_append(chat_id, "del failed! : error occured", "mm_del",0)
			await bot.send_message(msg.channel,text)

async def memo_check(msg,user):
	chat_id = msg.channel.id
	chat_from = msg.author.id
	now = log_append(chat_id, str(msg.content), "mm_ck",0)
	text = mention_user(user.user_id)+", "
	target = re.search('^사잽아 ((?:(?! 알려줘).)*) 알려줘', str(msg.content))
	target = target.groups()
	memo_status = quadra_memo(user.user_id)
	if target[0] == "전부":
		if memo_status.memo_num == 0:
			text += "기억하고 있는게 없어!"
			now = log_append(chat_id, "list failed! : no memo", "mm_ck",0)
			await bot.send_message(msg.channel,text)
		else :
			text += "메모를 찾았어!"
			now = log_append(chat_id, "list check!", "mm_ck",0)
			em = discord.Embed(title="내가 기억하고 있는 것들이야!", colour=discord.Colour.blue())
			temp_int = 1
			for i in memo_status.memo_str:
				em.add_field(name=str(temp_int)+"번", value=i, inline=False)
				now = log_append(chat_id,str(temp_int)+" : "+i, "mm_ck",0)
				temp_int += 1
			await bot.send_message(msg.channel,text,embed=em)
	else:
		target = (target[0].split('번'))[0]
		try : temp_swt = memo_status.check(int(target))
		except Exception as ex: temp_swt = 3
		if temp_swt == 1:
			text += "그정도로 많이 기억하고 있진 않아!"
			now = log_append(chat_id, "check failed! : capacity stack overflow", "mm_ck",0)
			await bot.send_message(msg.channel,text)
		elif temp_swt == 2:
			text += "그런 번호는 없다구!"
			now = log_append(chat_id, "check failed! : num must be at least 1", "mm_ck",0)
			await bot.send_message(msg.channel,text)
		elif temp_swt == 3:
			text += "뭘 알려달라는건지 모르겠어!"
			now = log_append(chat_id, "check failed! : error occured", "mm_ck",0)
			await bot.send_message(msg.channel,text)
		else:
			text += "메모를 찾았어!"
			now = log_append(chat_id, "check success! : "+temp_swt, "mm_ck",0)
			em = discord.Embed(title=target+"번 메모",description=temp_swt, colour=discord.Colour.blue())
			await bot.send_message(msg.channel,text,embed=em)

async def general_system(msg,user):
	while(True):
		re_target = re.search('^사잽아 도와줘$',msg.content)
		if re_target:
			await version(msg,user)
			break
		perm_class = server_permission(msg.server.id)
		# for general usage
		if perm_class.perm_check("basic",msg.channel.id) or (msg.channel.permissions_for(msg.author)).administrator :
			re_target = re.search('^사잽아 보고싶어$',msg.content)
			if re_target:
				em = discord.Embed(title="Katinor, the Quadra Ears",description="Katiadea Selinor\nCharacter Illustrated by 하얀로리, All Right Reserved.", colour=discord.Colour.blue())
				em.set_image(url="https://i.imgur.com/VyRXaJw.png")
				await bot.send_message(msg.channel,embed=em)
				break
			re_target = re.search('^사잽아 누구니$',msg.content)
			if re_target:
				await credit_view(msg,user)
				break
			re_target = re.search('^사잽아 뭐하니$',msg.content)
			if re_target:
				await lifetime(msg,user)
				break
			re_target = re.search('^사잽(아*)$',msg.content)
			if re_target:
				await lifetime(msg,user)
				break
			re_target = re.search('^사잽아 놀아줘$',msg.content)
			if re_target:
				await lifetime(msg,user)
				break
			re_target = re.search('^사잽아 ((?:(?! 어때).)*) 어때',msg.content)
			if re_target:
				await dialog_how(msg,user)
				break
			re_target = re.search('^사잽아 ((?:(?! 사줘).)*) 사줘',msg.content)
			if re_target:
				await dialog_buy(msg,user)
				break
			re_target = re.search('^사잽아 ((?:(?! (해줘|할래)).)*) (해줘|할래)',msg.content)
			if re_target:
				await dialog_please(msg,user)
				break
			re_target = re.search('^사잽아 ((?:(?! 하자).)*) 하자',msg.content)
			if re_target:
				await dialog_do(msg,user)
				break
			re_target = re.search('^사잽아 ((?:(?! 맞아\?).)*) 맞아\?',msg.content)
			if re_target:
				await game_prog(msg,user)
				break
			re_target = re.search('^사잽아 그만할래$',msg.content)
			if re_target:
				await game_end(msg,user)
				break
			re_target = re.search('^사잽아 용돈줘$',msg.content)
			if re_target:
				await get_supply(msg,user)
				break
			re_target = re.search('^사잽아 (?:((?:(?!에서).)*)에서 )?((?:(?! 찾아줘).)*) 찾아줘',msg.content)
			if re_target:
				await searching(msg,user)
				break
			re_target = re.search('^사잽아 네코',msg.content)
			if re_target:
				await neko_search(msg,user)
				break
			re_target = re.search('^사잽아 ((?:(?! 기억해줘).)*) 기억해줘',msg.content)
			if re_target:
				await memo_append(msg,user)
				break
			re_target = re.search('^사잽아 ((?:(?! 잊어줘).)*) 잊어줘',msg.content)
			if re_target:
				await memo_delete(msg,user)
				break
			re_target = re.search('^사잽아 ((?:(?! 알려줘).)*) 알려줘',msg.content)
			if re_target:
				await memo_check(msg,user)
				break
			if "외로워" in msg.content:
				await dialog_lone(msg,user)
				break
			if "안녕" in msg.content:
				await lifetime(msg,user)
				break

		if perm_class.perm_check("nsfw",msg.channel.id) or (msg.channel.permissions_for(msg.author)).administrator :
			re_target = re.search('^사잽아 야한네코',msg.content)
			if re_target:
				await neko_lewd_search(msg,user)
				break
		break

async def admin_system(msg,user):
	while(True):
		global admin
		global owner
		re_target = re.search('^4ears admin help$',msg.content)
		if re_target:
			now = log_append(msg.channel.id, str(msg.content), "adm","help1")
			if str(user.user_id) in owner:	out_text = mention_user(user.user_id)+", 너는 내 주인님이야!"
			elif str(user.user_id) in admin: out_text = mention_user(user.user_id)+", 너는 권한을 가지고 있어!"
			else : out_text = mention_user(user.user_id)+", 너는 따로 권한을 가지고 있지 않아!"
			text = "start with \"4ears admin \"\n"
			text += "stats : show how many server use this bot.\n"
			text += "4ears admin help admin to show commands about permission.\n"
			text += "4ears admin help user to show commands about user data."
			em = discord.Embed(title="QuadraEarsBot admin manual - main",description=text, colour=discord.Colour.blue())
			em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
			await bot.send_message(msg.channel,out_text,embed=em)
			break
		re_target = re.search('^4ears admin help admin$',msg.content)
		if re_target:
			now = log_append(msg.channel.id, str(msg.content), "adm","help2")
			if str(user.user_id) in owner:	out_text = mention_user(user.user_id)+", 너는 내 주인님이야!"
			elif str(user.user_id) in admin: out_text = mention_user(user.user_id)+", 너는 권한을 가지고 있어!"
			else : out_text = mention_user(user.user_id)+", 너는 따로 권한을 가지고 있지 않아!"
			text = "start with \"4ears admin \"\n"
			text += "list : show your role of this bot. if Katinor did, show list of admin.\n"
			text += "└use -server to show it directly on channel.\n"
			text += "└use -mention to show it directly on channel with mention them. except user not in that server.\n"
			text += "add : append user to admin list. Katinor only.\n"
			text += "del : remove user from admin list. Katinor only."
			em = discord.Embed(title="QuadraEarsBot admin manual - admin",description=text, colour=discord.Colour.blue())
			em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
			await bot.send_message(msg.channel,out_text,embed=em)
			break
		re_target = re.search('^4ears admin help user$',msg.content)
		if re_target:
			now = log_append(msg.channel.id, str(msg.content), "adm","help3")
			if str(user.user_id) in owner:	out_text = mention_user(user.user_id)+", 너는 내 주인님이야!"
			elif str(user.user_id) in admin: out_text = mention_user(user.user_id)+", 너는 권한을 가지고 있어!"
			else : out_text = mention_user(user.user_id)+", 너는 따로 권한을 가지고 있지 않아!"
			text = "start with \"4ears admin \"\n"
			text += "check commands can used by admin, change commands only available to Katinor\n"
			text += "check commands with -server option to show it directly on channel you said\n"
			text += "change commands with -add or -del option to change it as a delta\n"
			text += "love : check user's popularity of this bot.\n"
			text += "lvcng : change user's popularity of this bot.\n"
			text += "level : check user's level of this bot.\n"
			text += "levcng : change user's level of this bot.\n"
			text += "expcng : change user's experiance point of this bot.\n"
			text += "cash : check user's cash of this bot.\n"
			text += "cashcng : change user's cash of this bot."
			em = discord.Embed(title="QuadraEarsBot admin manual - user",description=text, colour=discord.Colour.blue())
			em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
			await bot.send_message(msg.channel,out_text,embed=em)
			break
		re_target = re.search('^4ears admin list$',msg.content)
		if re_target:
			now = log_append(msg.channel.id, str(msg.content), "adm","list")
			if str(user.user_id) in owner:
				text = ""
				number = 0
				num_un = 0
				admin_name = []
				admin_disc = []
				admin_id = []
				for i in admin:
					try:
						user = await bot.get_user_info(i)
						admin_name.append(user.name)
						admin_disc.append(user.discriminator)
						admin_id.append(user.id)
					except: num_un += 1
				for i in range(0,len(admin_name),1):
					text += admin_name[i]+"#"+str(admin_disc[i])+" : "+str(admin_id[i])+"\n"
					number += 1
				out_text = text+"총 "+str(number)+"명을 내가 인정했어!"
				if num_un > 0 : out_text += " "+str(num_un)+"명은 잘 모르겠어.."
				await bot.send_message(msg.author,out_text)
			elif str(user.user_id) in admin:
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 내가 인정한 사람이야!")
			else:
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 내가 인정한 사람이 아니야!")
			break
		re_target = re.search('^4ears admin list -server$',msg.content)
		if re_target:
			now = log_append(msg.channel.id, str(msg.content), "adm","list")
			if str(user.user_id) in owner:
				text = ""
				number = 0
				num_un = 0
				admin_name = []
				admin_disc = []
				for i in admin:
					try:
						user = await bot.get_user_info(i)
						admin_name.append(user.name)
						admin_disc.append(user.discriminator)
					except: num_un += 1
				for i in range(0,len(admin_name),1):
					text += admin_name[i]+"#"+str(admin_disc[i])+"\n"
					number += 1
				out_text = text+"총 "+str(number)+"명을 내가 인정했어!"
				if num_un > 0 : out_text += " "+str(num_un)+"명은 잘 모르겠어.."
				await bot.send_message(msg.channel,out_text)
			elif str(user.user_id) in admin:
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 내가 인정한 사람이야!")
			else:
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 내가 인정한 사람이 아니야!")
			break
		re_target = re.search('^4ears admin list -mention$',msg.content)
		if re_target:
			now = log_append(msg.channel.id, str(msg.content), "adm","list")
			if str(user.user_id) in owner:
				text = ""
				number = 0
				num_un = 0
				num_ot = 0
				admin_id = []
				for i in admin:
					try:
						user = await bot.get_user_info(i)
						if user in msg.server.members:
							admin_id.append(user.id)
						else: num_ot += 1
					except: num_un += 1
				for i in range(0,len(admin_id),1):
					text += "<@"+str(admin_id[i])+">\n"
					number += 1
				out_text = text+"총 "+str(number)+"명을 내가 인정했어!"
				if num_ot > 0 : out_text += " "+str(num_ot)+"명은 이곳에 없어."
				if num_un > 0 : out_text += " "+str(num_un)+"명은 잘 모르겠어.."
				await bot.send_message(msg.channel,out_text)
			elif str(user.user_id) in admin:
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 내가 인정한 사람이야!")
			else:
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 내가 인정한 사람이 아니야!")
			break
		re_target = re.search('^4ears admin add',msg.content)
		if re_target:
			now = log_append(msg.channel.id, str(msg.content), "adm","add")
			if str(user.user_id) in owner:
				add_list = msg.mentions
				if add_list:
					temp_s1 = 0
					temp_s2 = 0
					for i in add_list:
						if i.id in admin : 
							temp_text = i.name+"#"+i.discriminator+" : "+i.id
							now = log_append(msg.channel.id,"already admin - "+temp_text, "adm","add")
							temp_s2 += 1
						else :
							admin.append(i.id)
							temp_text = i.name+"#"+i.discriminator+" : "+i.id
							now = log_append(msg.channel.id,"success to append - "+temp_text, "adm","add")
							temp_s1 += 1
					admin = admin_save(admin)
					temp_txt = "권한을 부여했어!"
					if temp_s1 > 0 : temp_txt += "\n"+str(temp_s1)+"명에게 권한을 부여했어!"
					if temp_s2 > 0 : temp_txt += "\n"+str(temp_s2)+"명은 이미 권한이 있어!"
					await bot.send_message(msg.channel,mention_user(user.user_id)+" "+temp_txt)
				else: await bot.send_message(msg.channel,mention_user(user.user_id)+"대상이 잘못된거같은데?")
			else:
				log_text = msg.author.name+"#"+msg.author.discriminator+" : "+msg.author.id
				now = log_append(msg.channel.id,"access denied - "+log_text, "adm","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 내 주인님이 아냐!")
			break
		re_target = re.search('^4ears admin del',msg.content)
		if re_target:
			now = log_append(msg.channel.id, str(msg.content), "adm","del")
			if str(user.user_id) in owner:
				del_list = msg.mentions
				if del_list:
					temp_s1 = 0
					temp_s2 = 0
					for i in del_list:
						if str(i.id) in admin :
							admin.remove(str(i.id))
							temp_text = i.name+"#"+i.discriminator+" : "+i.id
							now = log_append(msg.channel.id,"success to delete - "+temp_text, "adm","del")
							temp_s2 += 1
						else :
							temp_text = i.name+"#"+i.discriminator+" : "+i.id
							now = log_append(msg.channel.id,"not admin - "+temp_text, "adm","del")
							temp_s1 += 1
					admin = admin_save(admin)
					temp_txt = "권한을 다시 회수했어!"
					if temp_s2 > 0 : temp_txt += "\n"+str(temp_s2)+"명의 권한을 회수했어!"
					if temp_s1 > 0 : temp_txt += "\n"+str(temp_s1)+"명은 권한명단에 없어!"
					await bot.send_message(msg.channel,mention_user(user.user_id)+" "+temp_txt)
				else: await bot.send_message(msg.channel,mention_user(user.user_id)+"대상이 잘못된거같은데?")
			else:
				log_text = msg.author.name+"#"+msg.author.discriminator+" : "+msg.author.id
				now = log_append(msg.channel.id,"access denied - "+log_text, "adm","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 내 주인님이 아냐!")	
			break
		re_target = re.search('^4ears admin profile',msg.content)
		if re_target:
			now = log_append(msg.channel.id, str(msg.content), "adm","prof")
			if str(user.user_id) in admin or str(user.user_id) in owner :
				trg_list = msg.mentions
				if len(trg_list) == 1:
					trg_id = trg_list[0].id
					trg_user = quadra_user(trg_id)
					realuser = await bot.get_user_info(trg_id)
					level_stat = trg_user.level
					cash_stat = trg_user.cash
					love_stat = trg_user.love
					if level_stat == quadra_user_module.MAX_LEVEL:
						req_exp = quadra_user_module.REQ_EXP[level_stat-1] - quadra_user_module.REQ_EXP[level_stat-2]
						cur_exp = trg_user.exp - quadra_user_module.REQ_EXP[level_stat-1]
					elif level_stat != 0 :
						req_exp = quadra_user_module.REQ_EXP[level_stat] - quadra_user_module.REQ_EXP[level_stat-1]
						cur_exp = trg_user.exp - quadra_user_module.REQ_EXP[level_stat-1]
					else :
						req_exp = quadra_user_module.REQ_EXP[level_stat]
						cur_exp = trg_user.exp
					if level_stat != quadra_user_module.MAX_LEVEL:
						exp_bar = ""
						exp_perc = (cur_exp / req_exp)
						exp_perc *= 100
						exp_perc_str = "(%3d %%)"%(exp_perc)
						for i in range(0,10,1):
							if exp_perc >= 10:
								exp_bar += "■"
								exp_perc -= 10
							else: exp_bar += "□"
						em = discord.Embed(title=realuser.name+"#"+str(realuser.discriminator)+" 의 프로필!",description="Lv."+str(level_stat)+" ( "+str(cur_exp)+" / "+str(req_exp)+" )\n"+exp_bar+exp_perc_str, colour=discord.Colour.blue())
					else : 	em = discord.Embed(title=realuser.name+"#"+str(realuser.discriminator)+" 의 프로필!",description="Lv."+str(level_stat)+" ( "+str(cur_exp)+" )\n■■■■■■■■■■(최대레벨)", colour=discord.Colour.blue())
					if realuser.avatar_url:	em.set_thumbnail(url=realuser.avatar_url)
					else : em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
					em.add_field(name="돈", value=str(cash_stat), inline=True)
					em.add_field(name="호감도", value=str(love_stat), inline=True)
					em.add_field(name="누적 경험치",value=str(trg_user.exp)+" / "+str(quadra_user_module.REQ_EXP[level_stat]),inline=False)
					if "-server" in msg.content:
						await bot.send_message(msg.channel,mention_user(user.user_id)+"!",embed = em)
					else:
						await bot.send_message(msg.author,mention_user(user.user_id)+"!",embed = em)
				else: await bot.send_message(msg.channel,mention_user(user.user_id)+" 한번에 한명만 물어봐줘!")
			else:
				log_text = msg.author.name+"#"+msg.author.discriminator+" : "+msg.author.id
				now = log_append(msg.channel.id,"access denied - "+log_text, "adm","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 가르쳐 줄수 없어!")	
			break	
		re_target = re.search('^4ears admin love',msg.content)
		if re_target:
			now = log_append(msg.channel.id, str(msg.content), "adm","love")
			if str(user.user_id) in admin or str(user.user_id) in owner :
				trg_list = msg.mentions
				if len(trg_list) == 1:
					trg_id = trg_list[0].id
					trg_user = quadra_user(trg_id)
					love_stat = trg_user.love
					if "-server" in msg.content:	await bot.send_message(msg.channel,mention_user(user.user_id)+"!\n"+"<@"+str(trg_id)+"> 의 친밀도는 "+str(love_stat)+" 이야!")
					else: await bot.send_message(msg.author,mention_user(user.user_id)+"!\n"+"<@"+str(trg_id)+"> 의 친밀도는 "+str(love_stat)+" 이야!")
				else: await bot.send_message(msg.channel,mention_user(user.user_id)+" 한번에 한명만 물어봐줘!")
			else:
				log_text = msg.author.name+"#"+msg.author.discriminator+" : "+msg.author.id
				now = log_append(msg.channel.id,"access denied - "+log_text, "adm","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 가르쳐 줄수 없어!")
			break
		re_target = re.search('^4ears admin lvcng',msg.content)
		if re_target:
			now = log_append(msg.channel.id, str(msg.content), "adm","lvcng")
			if str(user.user_id) in owner:
				trg_list = msg.mentions
				if len(trg_list) == 1:
					trg_id = trg_list[0].id
					trg_user = quadra_user(trg_id)
					data = str(msg.content).split(" ")
					val1 = int(data[len(data)-1])
					if "-add" in msg.content: val1 = trg_user.love + val1 
					elif "-del" in msg.content : val1 = trg_user.love - val1
					if val1 > quadra_user_module.MAX_LOVE : val1 = quadra_user_module.MAX_LOVE
					if val1 < quadra_user_module.MIN_LOVE : val1 = quadra_user_module.MIN_LOVE
					trg_user.change(love = val1)
					await bot.send_message(msg.channel,mention_user(user.user_id)+"!\n"+"<@"+str(trg_id)+"> 의 친밀도는 이제 "+str(val1)+" 이야!")
				else: await bot.send_message(msg.channel,mention_user(user.user_id)+" 한번에 한명만 물어봐줘!")
			else:
				log_text = msg.author.name+"#"+msg.author.discriminator+" : "+msg.author.id
				now = log_append(msg.channel.id,"access denied - "+log_text, "adm","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 내 주인님이 아니야!!")
			break
		re_target = re.search('^4ears admin stats$',msg.content)
		if re_target:
			now = log_append(msg.channel.id, str(msg.content), "adm","stats")
			if str(user.user_id) in admin or str(user.user_id) in owner:
				fp = open("quadra_server_list.txt","w")
				for i in bot.servers:
					fp.write(i.name+"\n")
				fp.close()
				text = mention_user(user.user_id)+", 현재 "+ str(len(bot.servers))+" 개의 서버에서 사용중이야! "+str(len(set(bot.get_all_members())))+" 명이 날 보고있어!"
				await bot.send_message(msg.channel,text)
			else:
				log_text = msg.author.name+"#"+msg.author.discriminator+" : "+msg.author.id
				now = log_append(msg.channel.id,"access denied - "+log_text, "adm","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 내가 인정한 사람이 아니야!")
			break
		re_target = re.search('^4ears admin level',msg.content)
		if re_target:
			now = log_append(msg.channel.id, str(msg.content), "adm","lv")
			if str(user.user_id) in admin or str(user.user_id) in owner :
				trg_list = msg.mentions
				if len(trg_list) == 1:
					trg_id = trg_list[0].id
					trg_user = quadra_user(trg_id)
					level_stat = trg_user.level
					if level_stat != 0 :
						req_exp = quadra_user_module.REQ_EXP[level_stat] - quadra_user_module.REQ_EXP[level_stat-1]
						cur_exp = trg_user.exp - quadra_user_module.REQ_EXP[level_stat-1]
					else :
						req_exp = quadra_user_module.REQ_EXP[level_stat]
						cur_exp = trg_user.exp
					if "-server" in msg.content:
						await bot.send_message(msg.channel,mention_user(user.user_id)+"!\n"+"<@"+str(trg_id)+"> 의 레벨은 "+str(level_stat)+" 이야! \n"+str(cur_exp)+" / "+str(req_exp)+" ( "+str(trg_user.exp)+" / "+str(quadra_user_module.REQ_EXP[level_stat])+" )")
					else:
						await bot.send_message(msg.author,mention_user(user.user_id)+"!\n"+"<@"+str(trg_id)+"> 의 레벨은 "+str(level_stat)+" 이야! \n"+str(cur_exp)+" / "+str(req_exp)+" ( "+str(trg_user.exp)+" / "+str(quadra_user_module.REQ_EXP[level_stat])+" )")
				else: await bot.send_message(msg.channel,mention_user(user.user_id)+" 한번에 한명만 물어봐줘!")
			else:
				log_text = msg.author.name+"#"+msg.author.discriminator+" : "+msg.author.id
				now = log_append(msg.channel.id,"access denied - "+log_text, "adm","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 가르쳐 줄수 없어!")
			break
		re_target = re.search('^4ears admin levcng',msg.content)
		if re_target:
			now = log_append(msg.channel.id, str(msg.content), "adm","levcng")
			if str(user.user_id) in owner:
				trg_list = msg.mentions
				if len(trg_list) == 1:
					trg_id = trg_list[0].id
					trg_user = quadra_user(trg_id)
					data = str(msg.content).split(" ")
					val1 = int(data[len(data)-1])
					if "-add" in msg.content: val1 = trg_user.level + val1
					elif "-del" in msg.content: val1 = trg_user.level - val1
					if val1 < 0 : val1 = 0
					if val1 >= len(quadra_user_module.REQ_EXP) : val1 = len(quadra_user_module.REQ_EXP)
					trg_user.change(level = val1)
					await bot.send_message(msg.channel,mention_user(user.user_id)+"!\n"+"<@"+str(trg_id)+"> 의 레벨은 이제 "+str(val1)+" 이야!\n")
				else: await bot.send_message(msg.channel,mention_user(user.user_id)+" 한번에 한명만 물어봐줘!")
			else:
				log_text = msg.author.name+"#"+msg.author.discriminator+" : "+msg.author.id
				now = log_append(msg.channel.id,"access denied - "+log_text, "adm","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 내 주인님이 아니야!!")
			break
		re_target = re.search('^4ears admin expcng',msg.content)
		if re_target:
			now = log_append(msg.channel.id, str(msg.content), "adm","expcng")
			if str(user.user_id) in owner:
				trg_list = msg.mentions
				if len(trg_list) == 1:
					trg_id = trg_list[0].id
					trg_user = quadra_user(trg_id)
					data = str(msg.content).split(" ")
					val1 = int(data[len(data)-1])
					if "-add" in msg.content: val1 = trg_user.exp + val1
					elif "-del" in msg.content: val1 = trg_user.exp - val1
					trg_user.change(exp = val1)
					await bot.send_message(msg.channel,mention_user(user.user_id)+"!\n"+"<@"+str(trg_id)+"> 의  경험치는 이제 "+str(val1)+" 이야!")
				else: await bot.send_message(msg.channel,mention_user(user.user_id)+" 한번에 한명만 물어봐줘!")
			else:
				log_text = msg.author.name+"#"+msg.author.discriminator+" : "+msg.author.id
				now = log_append(msg.channel.id,"access denied - "+log_text, "adm","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 내 주인님이 아니야!!")
			break
		re_target = re.search('^4ears admin cash',msg.content)
		if re_target and not ("cashcng" in msg.content):
			now = log_append(msg.channel.id, str(msg.content), "adm","cs")
			if str(user.user_id) in admin or str(user.user_id) in owner :
				trg_list = msg.mentions
				if len(trg_list) == 1:
					trg_id = trg_list[0].id
					trg_user = quadra_user(trg_id)
					cash_stat = trg_user.cash
					if "-server" in msg.content:
						await bot.send_message(msg.channel,mention_user(user.user_id)+"!\n"+"<@"+str(trg_id)+"> 의 돈은 "+str(cash_stat)+" 이야!")
					else:
						await bot.send_message(msg.author,mention_user(user.user_id)+"!\n"+"<@"+str(trg_id)+"> 의 돈은 "+str(cash_stat)+" 이야!")
				else: await bot.send_message(msg.channel,mention_user(user.user_id)+" 한번에 한명만 물어봐줘!")
			else:
				log_text = msg.author.name+"#"+msg.author.discriminator+" : "+msg.author.id
				now = log_append(msg.channel.id,"access denied - "+log_text, "adm","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 가르쳐 줄수 없어!")
			break
		re_target = re.search('^4ears admin cashcng',msg.content)
		if re_target:
			now = log_append(msg.channel.id, str(msg.content), "adm","cscng")
			if str(user.user_id) in owner:
				trg_list = msg.mentions
				if len(trg_list) == 1:
					trg_id = trg_list[0].id
					data = str(msg.content).split(" ")
					val1 = int(data[len(data)-1])
					trg_user = quadra_user(trg_id)
					if "-add" in msg.content: val1 = trg_user.cash + val1
					elif "-del" in msg.content: val1 = trg_user.cash - val1
					trg_user.change(cash = val1)
					await bot.send_message(msg.channel,mention_user(user.user_id)+"!\n"+"<@"+str(trg_id)+"> 의 돈은 이제 "+str(val1)+" 이야!")
				else: await bot.send_message(msg.channel,mention_user(user.user_id)+" 한번에 한명만 물어봐줘!")
			else:
				log_text = msg.author.name+"#"+msg.author.discriminator+" : "+msg.author.id
				now = log_append(msg.channel.id,"access denied - "+log_text, "adm","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 내 주인님이 아니야!!")
			break
		re_target = re.search('^4ears admin game',msg.content)
		if re_target:
			now = log_append(msg.channel.id, str(msg.content), "adm","game")
			if str(user.user_id) in admin or str(user.user_id) in owner:
				trg_list = msg.mentions
				if len(trg_list) == 1:
					trg_id = trg_list[0].id
					out_text = mention_user(trg_id)
					temp_swt = onGame(trg_id)
					if temp_swt == "야구게임을":
						data = quadra_baseball.check(trg_id)
						out_text += " 는 야구게임을 하고 있어."
						out_text += "\n정답은 "+str(data[0])+" 인데, "+str(data[1])+" 번 시도했어."
						log_append(msg.channel.id,"he play baseball. answer is "+str(data[0]), "adm","game")
					elif temp_swt == "업다운을":
						data = quadra_updown.check(trg_id)
						out_text = +" 는 업다운을 하고 있어."
						out_text = +"\n정답은 "+str(data[0])+" 인데, "+str(data[1])+" 번 시도했어."
						log_append(msg.channel.id,"he play updown. answer is "+str(data[0]), "adm","game")
					elif temp_swt == "로또를":
						data = quadra_lotto.check(trg_id)
						out_text = +" 는 로또를 하고 있어."
						temp_text = ""
						for i in data[0]:
							temp_text += str(i)+" "
						out_text = +"\n정답은 "+temp_text+" 에 보너스번호 "+str(data[1])+" 이었어!"
						log_append(msg.channel.id,"he play lotto. answer is "+temp_text+" : "+str(data[1]), "adm","game")
					else :
						log_append(msg.channel.id,"he play nothing", "adm","game")
						out_text = +" 는 아무것도 플레이하고 있지 않아."
					if "-server" in msg.content:	await bot.send_message(msg.channel,mention_user(user.user_id)+", "+out_text)
					else : await bot.send_message(msg.author,out_text)
				else: await bot.send_message(msg.channel,mention_user(user.user_id)+", 한번에 한명만 물어봐줘!")
			else:
				log_text = msg.author.name+"#"+msg.author.discriminator+" : "+msg.author.id
				now = log_append(msg.channel.id,"access denied - "+log_text, "adm","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 가르쳐 줄수 없어!")
			break
		break

async def channel_system(msg,user):
	while(True):
		if(msg.channel.permissions_for(msg.author)).administrator or str(user.user_id) in admin or str(user.user_id) in owner:
			perm_class = server_permission(msg.server.id)
			re_target = re.search('^4ears channel help$',msg.content)
			if re_target:
				now = log_append(msg.channel.id, str(msg.content), "chl","help1")
				text = "start with \"4ears channel \"\n"
				text += "add : 채널에 권한을 추가합니다.\n"
				text += "del : 채널에 권한을 뺍니다.\n"
				text += "purge : 채널을 초기화합니다.."
				em = discord.Embed(title="QuadraEarsBot admin manual - main",description=text, colour=discord.Colour.blue())
				em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
				await bot.send_message(msg.channel,embed=em)
				break
			re_target = re.search('^4ears channel add',msg.content)
			if re_target:
				now = log_append(msg.channel.id, str(msg.content), "chl","add")
				if "-nsfw" in msg.content:
					if perm_class.perm_check_admin("nsfw",msg.channel.id):
						now = log_append(msg.channel.id, "already permissioned", "chl","add")
						await bot.send_message(msg.channel,mention_user(user.user_id)+", 여긴 이미 허가되어있어!")
					else:
						perm_class.add("nsfw",msg.channel.id)
						now = log_append(msg.channel.id, "permission success", "chl","add")
						await bot.send_message(msg.channel,mention_user(user.user_id)+", 이제 여기서 쫑긋 할께!")
				else:
					if perm_class.perm_check_admin("basic",msg.channel.id):
						now = log_append(msg.channel.id, "already permissioned", "chl","add")
						await bot.send_message(msg.channel,mention_user(user.user_id)+", 여긴 이미 허가되어있어!")
					else:
						perm_class.add("basic",msg.channel.id)
						now = log_append(msg.channel.id, "permission success", "chl","add")
						await bot.send_message(msg.channel,mention_user(user.user_id)+", 이제 여기서 쫑긋 할께!")
				break
			re_target = re.search('^4ears channel del',msg.content)
			if re_target:
				now = log_append(msg.channel.id, str(msg.content), "chl","del")
				if "-nsfw" in msg.content:
					if perm_class.perm_check_admin("nsfw",msg.channel.id):
						perm_class.delete("nsfw",msg.channel.id)
						now = log_append(msg.channel.id, "permission delete", "chl","del")
						await bot.send_message(msg.channel,mention_user(user.user_id)+", 이제부터 여긴 안들을께!")
					else:
						now = log_append(msg.channel.id, "never heard", "chl","del")
						await bot.send_message(msg.channel,mention_user(user.user_id)+", 여긴 원래부터 안듣고있었어!")
				else:
					if perm_class.perm_check_admin("basic",msg.channel.id):
						perm_class.delete("basic",msg.channel.id)
						now = log_append(msg.channel.id, "permission delete", "chl","del")
						await bot.send_message(msg.channel,mention_user(user.user_id)+", 이제부터 여긴 안들을께!")
					else:
						now = log_append(msg.channel.id, "never heard", "chl","del")
						await bot.send_message(msg.channel,mention_user(user.user_id)+", 여긴 원래부터 안듣고있었어!")
				break
			re_target = re.search('^4ears channel purge',msg.content)
			if re_target:
				now = log_append(msg.channel.id, str(msg.content), "chl","pg")
				if "-nsfw" in msg.content:
					perm_class.delete_all("nsfw")
					now = log_append(msg.channel.id, "purged", "chl","pg")
					await bot.send_message(msg.channel,mention_user(user.user_id)+", 이제부터 모든 채널을 안들을께!")
				else:
					perm_class.delete_all("basic")
					now = log_append(msg.channel.id, "purged", "chl","pg")
					await bot.send_message(msg.channel,mention_user(user.user_id)+", 이제부터 모든 채널을 안들을께!")
				break
		else:
			await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 이 채널에 권한이 없어!")
			break

@bot.event
async def on_ready():
	global admin
	now = log_append('system', 'Bot running Start', 'system',0)
	admin = admin_load()
	await bot.change_presence(game=discord.Game(name='사잽아 도와줘 <-- 도움말'))

@bot.event
async def on_message(msg):
	global admin
	global owner
	said_user = quadra_user(msg.author.id)
	chat_id = msg.channel.id

	if msg.content.startswith("4ears admin"):
		await admin_system(msg,said_user)
	elif msg.content.startswith("4ears channel"):
		await channel_system(msg,said_user)
	elif msg.content.startswith("사잽아"):
		await general_system(msg,said_user)
	elif msg.author.bot == False :
		said_user.mody(exp = 1, exp_time = True)


bot.run(bot_token)