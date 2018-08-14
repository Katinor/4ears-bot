import re, requests, json, random, time, datetime, os, glob, asyncio, discord
from discord.ext import commands
from urllib import parse
import quadra_search_list, quadra_search_vocab, quadra_dialog_list, quadra_game_list, quadra_config, quadra_lifetime, quadra_user_module
import quadra_baseball, quadra_lotto, quadra_updown
from quadra_user_module import quadra_user
from quadra_perm_module import server_permission, user_permission
from quadra_memo_module import quadra_memo
import quadra_nsfw_module as nsfw_m
from quadra_log_module import log_append
from quadra_admin_command import admin_command
from quadra_version import version, credit_view, tou_view
from googletrans import Translator

bot_token = quadra_config.BOT_TOKEN
bot = commands.Bot(description="사잽아 도와줘 라고 말해주면 알려줄게!", command_prefix="")
user_perm = user_permission()

def onGame(user_id):
	if quadra_baseball.enable(user_id) : return "야구게임을"
	if quadra_updown.enable(user_id) : return "업다운을"
	if quadra_lotto.enable(user_id) : return "로또를"
	else : return ""

def mention_user(user_id):
	return "<@"+str(user_id)+">"

def url_encode(data):
	return (parse.quote(data).replace('/', '%2F'))
	
async def lifetime(msg,user):
	chat_id = msg.channel.id
	now = log_append(chat_id, str(msg.content), "lifetime",0)
	dup_num = user.lifetime_enable(now)
	if dup_num[0] < 6:
		user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
		text = mention_user(user.user_id)+" "+quadra_lifetime.checkSwitch(now)
		await bot.send_message(msg.channel,text)
	else:
		user.mody(love = -10)
		text = mention_user(user.user_id)+" "+quadra_lifetime.checkSwitch2(now, user.love_level())
		await bot.send_message(msg.channel,text)

async def dialog_how(msg,user):
	chat_id = msg.channel.id
	log_append(chat_id, str(msg.content), "d_how",0)
	target = re.search('^사잽아 ((?:(?! 어때).)*) 어때', str(msg.content))
	target = target.groups()
	user_list = msg.mentions
	
	if target[0] == "나":
		await bot.send_message(msg.channel,mention_user(user.user_id)+", 조금만 기다려줘! 시간이 좀 걸려!")
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
		ranking = user.user_rank()
		em.add_field(name="순위",value=str(ranking[0])+" / "+str(ranking[1]),inline=True)
		await bot.send_message(msg.channel,mention_user(user.user_id)+",\n"+user.love_text(),embed = em)
	elif len(user_list) == 1 and user_list :
		await bot.send_message(msg.channel,mention_user(user.user_id)+", 조금만 기다려줘! 시간이 좀 걸려!")
		if user_list[0].bot == False :
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
			ranking = trg_user.user_rank()
			em.add_field(name="순위",value=str(ranking[0])+" / "+str(ranking[1]),inline=True)
			await bot.send_message(msg.channel,mention_user(user.user_id)+", "+user_list[0].name+"#"+str(user_list[0].discriminator)+"에 대해서 묻는거지?",embed = em)
		else :
			await bot.send_message(msg.channel,mention_user(user.user_id)+", "+user_list[0].name+"#"+str(user_list[0].discriminator)+"는 봇이잖아!" )
	elif target[0] in quadra_search_vocab.dis_list: 
		text=random.choice(quadra_dialog_list.dialog_dis_how)
		user.mody(love = 2, love_time = True, exp = 5, exp_time = True)
		await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)
	elif target[0] in quadra_search_vocab.adult_list:
		text=random.choice(quadra_dialog_list.dialog_hentai_how)
		inc = - 10 - 5*(quadra_user_module.MAX_LOVE - quadra_user_module.MIN_LOVE - user.love) / (quadra_user_module.MAX_LOVE-quadra_user_module.MIN_LOVE)
		user.mody(love = inc, exp = 5, exp_time = True)
		await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)
	else:
		text="미안. 무슨 말인지 모르겠어."
		user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
		await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)

async def dialog_please(msg,user):
	chat_id = msg.channel.id
	log_append(chat_id, str(msg.content), "d_plz",0)
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
			log_append(chat_id,str(msg.content), "bb","start1")
			temp = quadra_baseball.start(user.user_id)
			log_append(chat_id,str(user.user_id)+" "+str(temp), "bb","start2")
			out_text=mention_user(user.user_id)+", 좋아! 이제 시작해보자~\n \"사잽아 ~ 맞아?\" 라고 말해줘!\n그만하고 싶다면 \"사잽아 그만할래\"라고 말해줘!"
			await bot.send_message(msg.channel,out_text)

	elif target[0] == "업다운":
		if onGame(user.user_id) == "업다운을":
			out_text=mention_user(user.user_id)+", 이미 플레이중인거 같은데?\n3자리 수를 생각해서 \"사잽아 ~ 맞아?\" 라고 말해줘.\n그만하고 싶다면 \"사잽아 그만할래\"라고 말해줘."
			await bot.send_message(msg.channel,out_text)
		elif onGame(user.user_id)!= "" :
			out_text=mention_user(user.user_id)+", 이미 "+onGame(user.user_id)+" 플레이중인거 같은데?"
			await bot.send_message(msg.channel,out_text)
		else:
			log_append(chat_id, str(msg.content), "ud","start1")
			temp = quadra_updown.start(user.user_id)
			log_append(chat_id,str(user.user_id)+" "+str(temp), "ud","start2")
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
			if user.cash >= quadra_config.LOTTO_CHARGE :
				log_append(chat_id, str(msg.content), "lt","start1")
				temp = quadra_lotto.start(user.user_id)
				log_append(chat_id,str(user.user_id)+" "+str(temp), "lt","start2")
				out_text=mention_user(user.user_id)+", 좋아! 이제 시작해보자~\n 1부터 35까지의 수 중 6개를 골라서 \"사잽아 ~ 맞아?\" 라고 말해줘. 예를 들면 \"사잽아 1 3 4 16 21 34 맞아?\" 느낌으로 써주면 돼!\n그만하고 싶다면 \"사잽아 그만할래\"라고 말해줘!\n\"사잽아 자동로또 해줘\"라고 말하면 자동으로 해볼게!."
				em = discord.Embed(title=msg.author.name+"#"+str(msg.author.discriminator)+", 로또 구매 영수증이야!",colour=discord.Colour.blue())
				if msg.author.avatar_url:	em.set_thumbnail(url=msg.author.avatar_url)
				else : em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
				past_cash = user.cash
				user.mody(cash = (-1)*quadra_config.LOTTO_CHARGE)
				future_cash = user.cash
				em.add_field(name="사용전", value=str(past_cash), inline=True)
				em.add_field(name="비용", value="1000", inline=True)
				em.add_field(name="사용후", value=str(future_cash), inline=True)
				await bot.send_message(msg.channel,out_text,embed = em)
			else:
				log_append(chat_id,str(user.user_id)+" don't have enough money", "lt","nocs")
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
		else:
			out_text=mention_user(user.user_id)+", 미안. 뭘 하자는건지 모르겠어."
			user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
			await bot.send_message(msg.channel,out_text)

async def game_prog(msg,user):
	chat_id = msg.channel.id
	log_append(chat_id, str(msg.content), "gm","prog")
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
	log_append(chat_id, str(msg.content), "bb","end")
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
	log_append(chat_id, str(msg.content), "bb","end")
	if user.canSupply():
		out_text = mention_user(user.user_id)+", "+user.supply_text()
		inc_array = quadra_config.SUPPLY_ARRAY
		past_cash = user.cash
		inc = inc_array[user.love_level()-1]
		swt = 0
		if user.cash + inc > quadra_user_module.CASH_SOFTCAP:
			if user.cash > quadra_user_module.CASH_SOFTCAP: swt = 2
			else: swt = 1
		if swt == 0 : user.mody(cash = inc, cash_time=True)
		elif swt == 1 : user.mody(cash = quadra_user_module.CASH_SOFTCAP - user.cash, cash_time=True)
		if swt <= 1:
			future_cash = user.cash
			em = discord.Embed(title=msg.author.name+"#"+str(msg.author.discriminator)+", 지원금 수령 완료!",colour=discord.Colour.blue())
			if msg.author.avatar_url:	em.set_thumbnail(url=msg.author.avatar_url)
			else : em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
			em.add_field(name="수령전", value=str(past_cash), inline=True)
			em.add_field(name="지원금", value=str(inc), inline=True)
			em.add_field(name="수령후", value=str(future_cash), inline=True)
			await bot.send_message(msg.channel,out_text,embed = em)
		else:
			out_text = mention_user(user.user_id)+", 미안해. 너무 돈을 많이 가지고 있는 것 같아."
			em = discord.Embed(title=msg.author.name+"#"+str(msg.author.discriminator)+", 지원금 수령 불가",colour=discord.Colour.blue())
			if msg.author.avatar_url:	em.set_thumbnail(url=msg.author.avatar_url)
			else : em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
			em.add_field(name="수령전", value=str(past_cash), inline=True)
			em.add_field(name="지원금", value="0", inline=True)
			em.add_field(name="수령후", value=str(past_cash), inline=True)
			await bot.send_message(msg.channel,out_text,embed = em)
	else:
		out_text = mention_user(user.user_id)+", 내일 다시 와줘!"
		await bot.send_message(msg.channel,out_text)
	
async def searching(msg,user,perm):
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
			log_append(chat_id, str(msg.content), "sch", "g_e")
			text="미안해. 무슨 게임인지 잘 몰라서 대신 검색해줄게! ( " + quadra_search_list.search_engine["스팀"] + url_encode(target[1]) + " )"
			user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
			await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)
		else : 
			log_append(chat_id, str(msg.content), "sch", "g")
			game_target = quadra_game_list.game_number[game_real_name]
			if game_target[0] == 0:
				text="혹시 이 게임 찾으려는거 맞아? ( " + quadra_game_list.steam_shop+game_target[1] + " )"
				user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
				await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)
			else :
				text=game_target[0]+" ( " + quadra_game_list.steam_shop+game_target[1] + " )"
				user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
				await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)
	elif target[0] in quadra_search_list.search_engine:
		if target[1] in quadra_search_vocab.adult_list:
			log_append(chat_id, str(msg.content), "sch", "ad")
			text="변태.. 이런거까지 찾아줘야해? ( " + quadra_search_list.search_engine[target[0]] + url_encode(target[1]) + " )"
			inc = - 5 - 5*(quadra_user_module.MAX_LOVE - quadra_user_module.MIN_LOVE - user.love) / (quadra_user_module.MAX_LOVE-quadra_user_module.MIN_LOVE)
			user.mody(love = inc, exp = 5, exp_time = True)
			await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)
		elif target[1] in quadra_search_vocab.dis_list:
			log_append(chat_id, str(msg.content), "sch", "dis")
			text="... 이런걸 생각중이라면 그만둬. ..내가 너랑 함께 있어줄테니까. ( " + quadra_search_list.search_engine[target[0]] + url_encode(target[1]) + " )"
			user.mody(love = 2,love_time = True, exp = 5, exp_time = True)
			await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)
		elif target[1] in quadra_search_vocab.wonder_list:
			log_append(chat_id, str(msg.content), "sch", "won")
			text=quadra_search_vocab.wonder_list[target[1]] + " ( " + quadra_search_list.search_engine[target[0]] + url_encode(target[1]) + " )"
			user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
			await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)
		else:
			log_append(chat_id, str(msg.content), "sch", 0)
			text="이거 찾으려는거 맞지? ( " + quadra_search_list.search_engine[target[0]] + url_encode(target[1]) + " )"
			user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
			await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)
	elif target[1] in quadra_search_list.hentai_url:
		log_append(chat_id, str(msg.content), "sch", "d_ad")
		text="너는 정말 최악의 변태구나.. 자, 여깄어. ( " + quadra_search_list.hentai_url[target[1]] + " )"
		inc = - 5 - 5*(quadra_user_module.MAX_LOVE - quadra_user_module.MIN_LOVE - user.love) / (quadra_user_module.MAX_LOVE-quadra_user_module.MIN_LOVE)
		user.mody(love = inc, exp = 5, exp_time = True)
		await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)
	elif target[1] in quadra_search_list.direct_url:
		log_append(chat_id, str(msg.content), "sch", "d")
		text="거기라면 나도 알고있어! 바로 보내줄께! ( " + quadra_search_list.direct_url[target[1]] + " )"
		user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
		await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)
	elif target[0] == "겔부루":
		if perm >= 2 :
			log_append(chat_id, str(msg.content), "sch", "g")
			temp_pid = str(random.randrange(0,1000))
			if target[1] == "아무거나":
				temp_url = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=1&pid="+temp_pid+"&json=1"
				tag_raw = "아무거나"
			elif target[1] == "야한거":
				temp_url = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=1&pid="+temp_pid+"&tags=rating:explicit&json=1"
				tag_raw = "야한거"
			elif target[1] == "안야한거":
				temp_url = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=1&pid="+temp_pid+"&tags=rating:safe&json=1"
				tag_raw = "안야한거"
			else:
				tag_list = target[1].split(" ")
				tag_raw = ""
				for i in range(0,len(tag_list),1):
					if tag_list[i] == "야한거": tag_list[i] = "rating:explicit"
					elif tag_list[i] == "안야한거": tag_list[i] = "rating:safe"
					if i == len(tag_list)-1 : tag_raw += tag_list[i]
					else : tag_raw += tag_list[i]+"+"
				temp_url = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=1&pid="+temp_pid+"&tags="+tag_raw+"&json=1"
			try:
				log_append(chat_id,"target : \""+ tag_raw+"\"", "sch", "g")
				r = requests.get(temp_url)
				r = r.text
				data = json.loads(r)
				file = data[0]["file_url"]
				embed=discord.Embed(title="태그:"+tag_raw)
				embed.set_image(url=file)
				log_append(chat_id,"transmit success!", "sch", "g")
				await bot.send_message(msg.channel, embed=embed)
			except Exception as ex:
				text="오류가 발생했어! 미안해."
				log_append(chat_id,"error occured!", "sch", "g")
				log_append(chat_id,ex, "sch", "g")
				if str(ex) == "list index out of range": text+=" 그 태그를 가진 그림이 충분히 없는 것 같아."
				else: text+=" 그 태그를 가진 그림이 없어!"
				await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)
		else :
			log_append(chat_id, str(msg.content), "sch", "g")
			temp_pid = str(random.randrange(0,1000))
			if target[1] == "아무거나":
				temp_url = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=1&pid="+temp_pid+"&tags=rating:safe&json=1"
				tag_raw = "rating:safe"
			else:
				tag_list = target[1].split(" ")
				if "rating:safe" in tag_list:
					tag_raw = ""
				else:
					tag_raw = "rating:safe+"
				for i in range(0,len(tag_list),1):
					if i == len(tag_list)-1 : tag_raw += tag_list[i]
					else : tag_raw += tag_list[i]+"+"
				temp_url = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=1&pid="+temp_pid+"&tags="+tag_raw+"&json=1"
			try:
				log_append(chat_id,"target : \""+ tag_raw+"\"", "sch", "g")
				r = requests.get(temp_url)
				r = r.text
				data = json.loads(r)
				file = data[0]["file_url"]
				embed=discord.Embed(title="태그:"+tag_raw)
				embed.set_image(url=file)
				log_append(chat_id,"transmit success!", "sch", "g")
				await bot.send_message(msg.channel, embed=embed)
			except Exception as ex:
				text="오류가 발생했어! 미안해."
				log_append(chat_id,"error occured!", "sch", "g")
				log_append(chat_id,ex, "sch", "g")
				if str(ex) == "list index out of range": text+=" 그 태그를 가진 그림이 충분히 없는 것 같아."
				else: text+=" 그 태그를 가진 그림이 없어!"
				await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)
	else:
		if target[1] in quadra_search_vocab.adult_list:
			log_append(chat_id, str(msg.content), "sch", "n_ad")
			text=target[1] + "라니... 변태! 이런거까지 찾아줘야해? ( " + quadra_search_list.search_engine["구글"] + url_encode(target[1]) + " )"
			inc = - 5 - 5*(quadra_user_module.MAX_LOVE - quadra_user_module.MIN_LOVE - user.love) / (quadra_user_module.MAX_LOVE-quadra_user_module.MIN_LOVE)
			user.mody(love = inc, exp = 5, exp_time = True)
			await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)
		elif target[1] in quadra_search_vocab.dis_list:
			log_append(chat_id, str(msg.content), "sch", "n_dis")
			text=target[1] + "같은걸 생각중이라면 그만둬. ..내가 너랑 함께 있어줄테니까. ( " + quadra_search_list.search_engine['구글'] + url_encode( target[1]) + " )"
			user.mody(love = 2,love_time = True, exp = 5, exp_time = True)
			await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)
		elif target[1] in quadra_search_vocab.wonder_list:
			log_append(chat_id, str(msg.content), "sch", "n_won")
			text=quadra_search_vocab.wonder_list[target[1]] + " ( " + quadra_search_list.search_engine['구글'] + url_encode(target[1]) + " )"
			user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
			await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)
		else:
			log_append(chat_id, str(msg.content), "sch", "n")
			text="이거 찾으려는거 맞지? ( " + quadra_search_list.search_engine["구글"] + url_encode(target[1]) + " )"
			user.mody(love = 1,love_time = True, exp = 5, exp_time = True)
			await bot.send_message(msg.channel,mention_user(user.user_id)+", "+text)

async def dialog_lone(msg,user):
	chat_id = msg.channel.id
	log_append(chat_id, str(msg.content), "d_lone",0)
	text = mention_user(user.user_id)+", "
	text += random.choice(quadra_dialog_list.dialog_lone_list)
	user.mody(love = 2,love_time = True, exp = 5, exp_time = True)
	await bot.send_message(msg.channel,text)	

async def memo_append(msg,user):
	chat_id = msg.channel.id
	log_append(chat_id, str(msg.content), "mm_add",0)
	text = mention_user(user.user_id)+", "
	target = re.search('^사잽아 ((?:(?! 기억해줘).)*) 기억해줘', str(msg.content))
	target = target.groups()
	memo_status = quadra_memo(user.user_id)
	temp_swt = memo_status.append(str(target[0]))
	if temp_swt == 0:
		text += "메모로 기록할께! "+str(memo_status.memo_num + 1)+"번째 메모야!"
		log_append(chat_id, "add success! : current num = "+str(memo_status.memo_num + 1), "mm_add",0)
		await bot.send_message(msg.channel,text)
	if temp_swt == 1:
		text += "너무 길어서 기억 못하겠어!"
		log_append(chat_id, "add failed! : string stack overflow", "mm_add",0)
		await bot.send_message(msg.channel,text)
	if temp_swt == 2:
		text += "이미 너무 많이 기억하고있어!"
		log_append(chat_id, "add failed! : capacity stack overflow", "mm_add",0)
		await bot.send_message(msg.channel,text)
	if temp_swt == 3:
		text += "이상한게 끼여있어서 못기억하겠어!"
		log_append(chat_id, "add failed! : forbidden string included", "mm_add",0)
		await bot.send_message(msg.channel,text)

async def memo_delete(msg,user):
	chat_id = msg.channel.id
	log_append(chat_id, str(msg.content), "mm_del",0)
	text = mention_user(user.user_id)+", "
	target = re.search('^사잽아 ((?:(?! 잊어줘).)*) 잊어줘', str(msg.content))
	target = target.groups()
	memo_status = quadra_memo(user.user_id)
	if target[0] == "전부":
		temp_swt = memo_status.purge()
		if temp_swt == 0:
			text += "메모를 전부 지웠어!"
			log_append(chat_id, "purge success!", "mm_del",0)
			await bot.send_message(msg.channel,text)
		if temp_swt == 1:
			text += "메모가 없어!"
			log_append(chat_id, "purge failed! : index out of range", "mm_del",0)
			await bot.send_message(msg.channel,text)
	else:
		target = (target[0].split('번'))[0]
		try : temp_swt = memo_status.delete(int(target))
		except Exception: temp_swt = 3
		if temp_swt == 0:
			text += "메모를 지웠어! "+str(memo_status.memo_num - 1)+"개의 메모가 남아있어!"
			log_append(chat_id, "del success! : current num = "+str(memo_status.memo_num - 1), "mm_del",0)
			await bot.send_message(msg.channel,text)
		if temp_swt == 1:
			text += "그정도로 많이 기억하고 있진 않아!"
			log_append(chat_id, "del failed! : capacity stack overflow", "mm_del",0)
			await bot.send_message(msg.channel,text)
		if temp_swt == 2:
			text += "그런 번호는 없다구!"
			log_append(chat_id, "del failed! : num must be at least 1", "mm_del",0)
			await bot.send_message(msg.channel,text)
		if temp_swt == 3:
			text += "뭘 잊어달라는건지 모르겠어!"
			log_append(chat_id, "del failed! : error occured", "mm_del",0)
			await bot.send_message(msg.channel,text)

async def memo_check(msg,user):
	chat_id = msg.channel.id
	log_append(chat_id, str(msg.content), "mm_ck",0)
	text = mention_user(user.user_id)+", "
	target = re.search('^사잽아 ((?:(?! 알려줘).)*) 알려줘', str(msg.content))
	target = target.groups()
	memo_status = quadra_memo(user.user_id)
	if target[0] == "전부":
		if memo_status.memo_num == 0:
			text += "기억하고 있는게 없어!"
			log_append(chat_id, "list failed! : no memo", "mm_ck",0)
			await bot.send_message(msg.channel,text)
		else :
			text += "메모를 찾았어!"
			log_append(chat_id, "list check!", "mm_ck",0)
			em = discord.Embed(title="내가 기억하고 있는 것들이야!", colour=discord.Colour.blue())
			temp_int = 1
			for i in memo_status.memo_str:
				em.add_field(name=str(temp_int)+"번", value=i, inline=False)
				log_append(chat_id,str(temp_int)+" : "+i, "mm_ck",0)
				temp_int += 1
			await bot.send_message(msg.channel,text,embed=em)
	else:
		target = (target[0].split('번'))[0]
		try : temp_swt = memo_status.check(int(target))
		except Exception: temp_swt = 3
		if temp_swt == 1:
			text += "그정도로 많이 기억하고 있진 않아!"
			log_append(chat_id, "check failed! : capacity stack overflow", "mm_ck",0)
			await bot.send_message(msg.channel,text)
		elif temp_swt == 2:
			text += "그런 번호는 없다구!"
			log_append(chat_id, "check failed! : num must be at least 1", "mm_ck",0)
			await bot.send_message(msg.channel,text)
		elif temp_swt == 3:
			text += "뭘 알려달라는건지 모르겠어!"
			log_append(chat_id, "check failed! : error occured", "mm_ck",0)
			await bot.send_message(msg.channel,text)
		else:
			text += "메모를 찾았어!"
			log_append(chat_id, "check success! : "+temp_swt, "mm_ck",0)
			em = discord.Embed(title=target+"번 메모",description=temp_swt, colour=discord.Colour.blue())
			await bot.send_message(msg.channel,text,embed=em)

async def quadra_trans(msg,user,perm):
	chat_id = msg.channel.id
	log_append(chat_id, str(msg.content), "trans",0)
	target = re.search('^사잽아 (?:((?:(?!로).)*)로 )?((?:(?! 번역해줘).)*) 번역해줘', str(msg.content))
	target = target.groups()

	translator = Translator()

	lang_dest = "ko"

	if target[0] in quadra_search_list.lang_list.keys():
		lang_dest = quadra_search_list.lang_list[target[0]]
	elif target[0]:
		lang_dest = target[0]
	try:
		asw = translator.translate(target[1],dest = lang_dest)
		em = discord.Embed(title="번역결과",description=asw.text, colour=discord.Colour.blue())
		if not(asw.dest == 'ko' or asw.dest == 'en'): em.add_field(name="발음", value=asw.pronunciation, inline=False)
		em.add_field(name="원문", value=asw.origin, inline=False)
		em.add_field(name="시작언어", value=asw.src, inline=True)
		em.add_field(name="결과언어", value=asw.dest, inline=True)
		text = mention_user(user.user_id)+", 번역을 마쳤어!"
		log_append(chat_id, "Success! : "+asw.text, "trans",0)
		await bot.send_message(msg.channel,text,embed=em)
		return 0
	except Exception as ex:
		if ex == ValueError:
			log_append(chat_id, "Cannot understand dest language.", "trans",0)
			await bot.send_message(msg.channel,mention_user(user.user_id)+", 어느 언어로 번역할지 제대로 이해못했어!")
			return 0
		else:
			log_append(chat_id, "Unknown Error : "+str(ex), "trans",0)
			await bot.send_message(msg.channel,mention_user(user.user_id)+", 미안해! 번역이 잘 안돼..")
			return 0

async def general_system(msg,user,perm):
	while(True):
		if msg.content == "사잽아 도와줘":
			await version(msg,user,"main",bot)
			break
		re_target = re.search('^사잽아 ((?:(?! 도와줘).)*) 도와줘',msg.content)
		if re_target:
			re_target = re_target.groups()
			await version(msg,user,re_target[0],bot)
			break
		# for general usage
		if perm > 0 or (msg.channel.permissions_for(msg.author)).administrator :
			if msg.content == "사잽아 보고싶어":
				em = discord.Embed(title="Katinor, the Quadra Ears",description="Katiadea Selinor\nCharacter Illustrated by Muku, All Right Reserved.", colour=discord.Colour.blue())
				em.set_image(url="https://i.imgur.com/VyRXaJw.png")
				await bot.send_message(msg.channel,embed=em)
				break
			if msg.content == "사잽아 누구니":
				await credit_view(msg,user,bot)
				break
			if msg.content == "사잽아 저작권":
				await credit_view(msg,user,bot)
				break
			if msg.content.startswith("사잽아 이용약관"):
				await tou_view(msg,user,bot)
				break
			if msg.content == "사잽아 뭐하니":
				await lifetime(msg,user)
				break
			if msg.content == "사잽아 놀아줘":
				await lifetime(msg,user)
				break
			re_target = re.search('^사잽(아*)$',msg.content)
			if re_target:
				await lifetime(msg,user)
				break
			re_target = re.search('^사잽아 ((?:(?! 어때).)*) 어때',msg.content)
			if re_target:
				await dialog_how(msg,user)
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
			if msg.content == "사잽아 그만할래":
				await game_end(msg,user)
				break
			if msg.content == "사잽아 용돈줘":
				await get_supply(msg,user)
				break
			if msg.content == "사잽아 돈내놔":
				await get_supply(msg,user)
				break
			re_target = re.search('^사잽아 (?:((?:(?!에서).)*)에서 )?((?:(?! 찾아줘).)*) 찾아줘',msg.content)
			if re_target:
				await searching(msg,user,perm)
				break
			re_target = re.search('^사잽아 (?:((?:(?!로).)*)로 )?((?:(?! 번역해줘).)*) 번역해줘',msg.content)
			if re_target:
				await quadra_trans(msg,user,perm)
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
			if "네코" in msg.content:
				log_append(msg.channel.id, str(msg.content), "neko",0)
				result = nsfw_m.neko_search(msg.content,user,perm)
				if result[2] >= 1:
					await bot.send_message(msg.channel, embed=result[0])
					log_append(msg.channel.id, "flag name : "+result[1], "neko",0)
				else : await bot.send_message(msg.channel, mention_user(user.user_id)+", "+result[3])
				break
			if "야옹" in msg.content:
				log_append(msg.channel.id, str(msg.content), "neko",0)
				result = nsfw_m.neko_search(msg.content,user,perm)
				if result[2] >= 1:
					await bot.send_message(msg.channel, embed=result[0])
					log_append(msg.channel.id, "flag name : "+result[1], "neko",0)
				else : await bot.send_message(msg.channel, mention_user(user.user_id)+", "+result[3])
				break
		break

async def channel_system(msg,user,perm, user_perm):
	while(True):
		if "owner" in user_perm or "ch_admin" in user_perm:
			perm_class = server_permission(msg.server.id)
			re_target = re.search('^4ears channel help$',msg.content)
			if re_target:
				log_append(msg.channel.id, str(msg.content), "chl","help1")
				text = "start with \"4ears channel \"\n"
				text += "add : 채널에 권한을 추가합니다.\n"
				text += "del : 채널에 권한을 뺍니다.\n"
				text += "purge : 채널을 초기화합니다.\n"
				text += "stat : 현 채널의 권한을 확인합니다."
				em = discord.Embed(title="QuadraEarsBot channel manual",description=text, colour=discord.Colour.blue())
				em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
				await bot.send_message(msg.channel,embed=em)
				break
			re_target = re.search('^4ears channel add',msg.content)
			if re_target:
				log_append(msg.channel.id, str(msg.content), "chl","add")
				if "-nsfw" in msg.content:
					if perm_class.perm_check_admin("nsfw",msg.channel.id):
						log_append(msg.channel.id, "already permissioned", "chl","add")
						await bot.send_message(msg.channel,mention_user(user.user_id)+", 여긴 이미 허가되어있어!")
					else:
						perm_class.add("nsfw",msg.channel.id)
						log_append(msg.channel.id, "permission success", "chl","add")
						await bot.send_message(msg.channel,mention_user(user.user_id)+", 이제 여기서 쫑긋 할께!")
				else:
					if perm_class.perm_check_admin("basic",msg.channel.id):
						log_append(msg.channel.id, "already permissioned", "chl","add")
						await bot.send_message(msg.channel,mention_user(user.user_id)+", 여긴 이미 허가되어있어!")
					else:
						perm_class.add("basic",msg.channel.id)
						log_append(msg.channel.id, "permission success", "chl","add")
						await bot.send_message(msg.channel,mention_user(user.user_id)+", 이제 여기서 쫑긋 할께!")
				break
			re_target = re.search('^4ears channel del',msg.content)
			if re_target:
				log_append(msg.channel.id, str(msg.content), "chl","del")
				if "-nsfw" in msg.content:
					if perm_class.perm_check_admin("nsfw",msg.channel.id):
						perm_class.delete("nsfw",msg.channel.id)
						log_append(msg.channel.id, "permission delete", "chl","del")
						await bot.send_message(msg.channel,mention_user(user.user_id)+", 이제부터 여긴 안들을께!")
					else:
						log_append(msg.channel.id, "never heard", "chl","del")
						await bot.send_message(msg.channel,mention_user(user.user_id)+", 여긴 원래부터 안듣고있었어!")
				else:
					if perm_class.perm_check_admin("basic",msg.channel.id):
						perm_class.delete("basic",msg.channel.id)
						log_append(msg.channel.id, "permission delete", "chl","del")
						await bot.send_message(msg.channel,mention_user(user.user_id)+", 이제부터 여긴 안들을께!")
					else:
						log_append(msg.channel.id, "never heard", "chl","del")
						await bot.send_message(msg.channel,mention_user(user.user_id)+", 여긴 원래부터 안듣고있었어!")
				break
			re_target = re.search('^4ears channel purge',msg.content)
			if re_target:
				log_append(msg.channel.id, str(msg.content), "chl","pg")
				if "-nsfw" in msg.content:
					perm_class.delete_all("nsfw")
					log_append(msg.channel.id, "purged", "chl","pg")
					await bot.send_message(msg.channel,mention_user(user.user_id)+", 이제부터 모든 채널을 안들을께!")
				else:
					perm_class.delete_all("basic")
					log_append(msg.channel.id, "purged", "chl","pg")
					await bot.send_message(msg.channel,mention_user(user.user_id)+", 이제부터 모든 채널을 안들을께!")
				break
			re_target = re.search('^4ears channel stat',msg.content)
			if re_target:
				log_append(msg.channel.id, str(msg.content), "chl","st")
				perm_list_str = ""
				if perm_class.perm_check("basic",msg.channel.id): perm_list_str += "basic,"
				if perm_class.perm_check("nsfw",msg.channel.id): perm_list_str += "nsfw,"
				em = discord.Embed(title="QuadraEarsBot channel status", colour=discord.Colour.blue())
				em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
				em.add_field(name="basic 갯수", value=str(len(perm_class.allow_channel)), inline=True)
				if len(perm_class.allow_nsfw) > 0 : em.add_field(name="nsfw 갯수", value=str(len(perm_class.allow_nsfw)), inline=True)
				em.add_field(name="본채널", value=perm_list_str, inline=True)
				await bot.send_message(msg.channel,embed=em)
				break
		else:
			await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 이 채널에 권한이 없어!")
			break

@bot.event
async def on_ready():
	log_append('system', 'Bot running Start', 'system',0)
	await bot.change_presence(game=discord.Game(name='사잽아 도와줘 <-- 도움말'))

@bot.event
async def on_message(msg):
	perm_rank = 0
	try:
		perm_class = server_permission(msg.server.id)
		if perm_class.perm_check("nsfw",msg.channel.id): perm_rank = 2
		elif perm_class.perm_check("basic",msg.channel.id): perm_rank = 1
		else: perm_rank = 0
	except Exception:
		perm_rank = 1

	if msg.author.bot == False :
		said_user = quadra_user(msg.author.id)
		author_perm = user_perm.check(msg, said_user.user_id)
		if "user" in author_perm :
			if msg.content.startswith("4ears admin"):
				await admin_command(msg,said_user,perm_rank, user_perm, bot)
			elif msg.content.startswith("4ears channel"):
				await channel_system(msg,said_user, perm_rank, author_perm)
			elif msg.content.startswith("사잽아"):
				await general_system(msg,said_user, perm_rank)
			else :
				said_user.general_exp_process(len(msg.content))
	else :
		profile_name = "user_database/"+str(msg.author.id)+".txt"
		if os.path.exists(profile_name) == True:
			os.remove(profile_name)
			log_append(msg.channel.id,msg.author.name+"#"+str(msg.author.discriminator)+" ("+str(msg.author.id)+" ) is bot. remained userdata has been deleted.","system",0)
		if int(msg.author.id) != 423338258055823360 and perm_rank > 0 :
			rand_int = random.randrange(0,100)
			if rand_int < 2:
				log_append(msg.channel.id,"bot msg triggered","system",0)
				await bot.send_message(msg.channel,msg.author.name+"랑만 놀지말고 나랑도 놀아줘!")

bot.run(bot_token)