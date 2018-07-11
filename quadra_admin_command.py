import asyncio, discord, re, quadra_user_module
from quadra_log_module import log_append
from quadra_user_module import quadra_user
from quadra_memo_module import quadra_memo

def mention_user(user_id):
	return "<@"+str(user_id)+">"

def admin_help(flag,user,user_perm):
	if "owner" in user_perm: out_text = mention_user(user.user_id)+", 너는 내 주인님이야!"
	elif "admin" in user_perm: out_text = mention_user(user.user_id)+", 너는 권한을 가지고 있어!"
	elif "ch_admin" in user_perm: out_text = mention_user(user.user_id)+", 너는 이 채널의 관리자야!"
	else: out_text = mention_user(user.user_id)+", 너는 따로 권한을 가지고 있지 않아!"
	
	if flag == "main":
		out_embed = "start with \"4ears admin \"\n"
		out_embed+= "stats : show how many server use this bot.\n"
		out_embed+= "4ears admin help admin to show commands about permission.\n"
		out_embed+= "4ears admin help block to show commands about blocking user.\n"
		out_embed+= "4ears admin help user to show commands about user data."
	elif flag == "admin":
		out_embed = "start with \"4ears admin \"\n"
		out_embed+= "add : append user to admin list. Owner only.\n"
		out_embed+= "del : remove user from admin list. Owner only."
	elif flag == "block":
		out_embed = "start with \"4ears admin \"\n"
		out_embed+= "block : block user.\n"
		out_embed+= "unblock : unblock user."
	elif flag == "user":
		out_embed = "start with \"4ears admin \"\n"
		out_embed+= "check commands can used by admin, change commands only available to Owner\n"
		out_embed+= "check commands with -server option to show it directly on channel you said\n"
		out_embed+= "change commands with -add or -del option to change it as a delta\n"
		out_embed+= "love : check user's popularity of this bot.\n"
		out_embed+= "lovcng : change user's popularity of this bot.\n"
		out_embed+= "levcng : change user's level of this bot.\n"
		out_embed+= "expcng : change user's experiance point of this bot.\n"
		out_embed+= "cashcng : change user's cash of this bot.\n"
		out_embed+= "memo : check user's memo. (can be also used by server admin!)"
	em = discord.Embed(title="QuadraEarsBot admin manual - "+flag,description=out_embed, colour=discord.Colour.blue())
	em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
	return [out_text, em]

async def admin_command(msg, user, channel_perm, user_perm, bot):
	author_perm = user_perm.check(msg, user.user_id)
	log_text = msg.author.name+"#"+msg.author.discriminator+" : "+msg.author.id+" ["
	for i in author_perm:
		log_text += i+", "
	log_text += "]"
	log_append(msg.channel.id,"admin panel access : "+log_text, "adm","acc")
	while(True):
		if msg.content == '4ears admin help':
			log_append(msg.channel.id, str(msg.content), "adm","help")
			temp_cont = admin_help("main",user,author_perm)
			await bot.send_message(msg.channel,temp_cont[0],embed=temp_cont[1])
			break
		if msg.content == '4ears admin help admin':
			log_append(msg.channel.id, str(msg.content), "adm","help")
			temp_cont = admin_help("admin",user,author_perm)
			await bot.send_message(msg.channel,temp_cont[0],embed=temp_cont[1])
			break
		if msg.content == '4ears admin help block':
			log_append(msg.channel.id, str(msg.content), "adm","help")
			temp_cont = admin_help("block",user,author_perm)
			await bot.send_message(msg.channel,temp_cont[0],embed=temp_cont[1])
			break
		if msg.content == '4ears admin help user':
			log_append(msg.channel.id, str(msg.content), "adm","help")
			temp_cont = admin_help("user",user,author_perm)
			await bot.send_message(msg.channel,temp_cont[0],embed=temp_cont[1])
			break
		if msg.content.startswith("4ears admin add"):
			log_append(msg.channel.id, str(msg.content), "adm","add")
			if "owner" in author_perm:
				add_list = msg.mentions
				if add_list:
					temp_s1 = 0
					temp_s2 = 0
					temp_s0 = 0
					for i in add_list:
						temp_var = user_perm.admin_add(i)
						if temp_var == 0: temp_s0 += 1
						elif temp_var == 1: temp_s1 += 1
						elif temp_var == 2: temp_s2 += 1
					user_perm.admin_save()
					temp_txt = "권한을 부여했어!"
					if temp_s0 > 0 : temp_txt += "\n"+str(temp_s0)+"명에게 권한을 부여했어!"
					if temp_s1 > 0 : temp_txt += "\n"+str(temp_s1)+"명은 이미 권한이 있어!"
					if temp_s2 > 0 : temp_txt += "\n"+str(temp_s2)+"명은 봇이야!"
					await bot.send_message(msg.channel,mention_user(user.user_id)+", "+temp_txt)
				else: await bot.send_message(msg.channel,mention_user(user.user_id)+", 대상이 잘못된거같은데?")
			else:
				log_text = msg.author.name+"#"+msg.author.discriminator+" : "+msg.author.id
				log_append(msg.channel.id,"access denied - "+log_text, "adm","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 내 주인님이 아냐!")
			break
		if msg.content.startswith("4ears admin del"):
			log_append(msg.channel.id, str(msg.content), "adm","del")
			if "owner" in author_perm:
				add_list = msg.mentions
				if add_list:
					temp_s1 = 0
					temp_s2 = 0
					temp_s0 = 0
					for i in add_list:
						temp_var = user_perm.admin_del(i)
						if temp_var == 0: temp_s0 += 1
						elif temp_var == 1: temp_s1 += 1
						elif temp_var == 2: temp_s2 += 1
					user_perm.admin_save()
					temp_txt = "권한을 회수했어!"
					if temp_s0 > 0 : temp_txt += "\n"+str(temp_s0)+"명의 권한을 회수했어!"
					if temp_s1 > 0 : temp_txt += "\n"+str(temp_s1)+"명은 애초에 권한이 없어!"
					if temp_s2 > 0 : temp_txt += "\n"+str(temp_s2)+"명은 봇이야!"
					await bot.send_message(msg.channel,mention_user(user.user_id)+", "+temp_txt)
				else: await bot.send_message(msg.channel,mention_user(user.user_id)+", 대상이 잘못된거같은데?")
			else:
				log_text = msg.author.name+"#"+msg.author.discriminator+" : "+msg.author.id
				log_append(msg.channel.id,"access denied - "+log_text, "adm","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 내 주인님이 아냐!")
			break
		if msg.content.startswith("4ears admin block"):
			log_append(msg.channel.id, str(msg.content), "bl","add")
			if "admin" in author_perm:
				add_list = msg.mentions
				if add_list:
					temp_s1 = 0
					temp_s2 = 0
					temp_s3 = 0
					temp_s4 = 0
					temp_s0 = 0
					for i in add_list:
						temp_var = user_perm.block(i,author_perm)
						if temp_var == 0: temp_s0 += 1
						elif temp_var == 1: temp_s1 += 1
						elif temp_var == 2: temp_s2 += 1
						elif temp_var == 3: temp_s3 += 1
						elif temp_var == 4: temp_s4 += 1
					user_perm.block_save()
					temp_txt = "차단을 완료했어!"
					if temp_s0 > 0 : temp_txt += "\n"+str(temp_s0)+"명을 무시할께!"
					if temp_s4 > 0 : temp_txt += "\n"+str(temp_s4)+"명은 무시할 겸 관리자도 해고했어!!"
					if temp_s3 > 0 : temp_txt += "\n"+str(temp_s3)+"명은 관리자라서 무시할 수 없어!"
					if temp_s1 > 0 : temp_txt += "\n"+str(temp_s1)+"명은 이미 무시하고있어!"
					if temp_s2 > 0 : temp_txt += "\n"+str(temp_s2)+"명은 봇이야!"
					await bot.send_message(msg.channel,mention_user(user.user_id)+", "+temp_txt)
				else: await bot.send_message(msg.channel,mention_user(user.user_id)+", 대상이 잘못된거같은데?")
			else:
				log_text = msg.author.name+"#"+msg.author.discriminator+" : "+msg.author.id
				log_append(msg.channel.id,"access denied - "+log_text, "bl","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 권한이 없어!")
			break
		if msg.content.startswith("4ears admin unblock"):
			log_append(msg.channel.id, str(msg.content), "bl","del")
			if "admin" in author_perm:
				add_list = msg.mentions
				if add_list:
					temp_s1 = 0
					temp_s2 = 0
					temp_s0 = 0
					for i in add_list:
						temp_var = user_perm.unblock(i)
						if temp_var == 0: temp_s0 += 1
						elif temp_var == 1: temp_s1 += 1
						elif temp_var == 2: temp_s2 += 1
					user_perm.block_save()
					temp_txt = "차단을 해제했어!"
					if temp_s0 > 0 : temp_txt += "\n"+str(temp_s0)+"명의 말을 다시 들을께!"
					if temp_s1 > 0 : temp_txt += "\n"+str(temp_s1)+"명은 듣고 있었어!"
					if temp_s2 > 0 : temp_txt += "\n"+str(temp_s2)+"명은 봇이야!"
					await bot.send_message(msg.channel,mention_user(user.user_id)+", "+temp_txt)
				else: await bot.send_message(msg.channel,mention_user(user.user_id)+", 대상이 잘못된거같은데?")
			else:
				log_text = msg.author.name+"#"+msg.author.discriminator+" : "+msg.author.id
				log_append(msg.channel.id,"access denied - "+log_text, "bl","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 권한이 없어!")
			break
		if msg.content.startswith("4ears admin love"):
			log_append(msg.channel.id, str(msg.content), "adm","love")
			if "admin" in author_perm :
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
				log_append(msg.channel.id,"access denied - "+log_text, "adm","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 가르쳐 줄수 없어!")
			break
		if msg.content.startswith("4ears admin lovcng"):
			log_append(msg.channel.id, str(msg.content), "adm","lovcng")
			if "owner" in author_perm:
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
				log_append(msg.channel.id,"access denied - "+log_text, "adm","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 내 주인님이 아니야!!")
			break
		if msg.content == '4ears admin stats':
			log_append(msg.channel.id, str(msg.content), "adm","stats")
			if "admin" in author_perm:
				fp = open("quadra_server_list.txt","w")
				for i in bot.servers:
					fp.write(i.name+"\n")
				fp.close()
				text = mention_user(user.user_id)+", 현재 "+ str(len(bot.servers))+" 개의 서버에서 사용중이야! "+str(len(set(bot.get_all_members())))+" 명이 날 보고있어!"
				await bot.send_message(msg.channel,text)
			else:
				log_text = msg.author.name+"#"+msg.author.discriminator+" : "+msg.author.id
				log_append(msg.channel.id,"access denied - "+log_text, "adm","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 내가 인정한 사람이 아니야!")
			break
		if msg.content.startswith("4ears admin levcng"):
			log_append(msg.channel.id, str(msg.content), "adm","levcng")
			if "owner" in author_perm:
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
				log_append(msg.channel.id,"access denied - "+log_text, "adm","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 내 주인님이 아니야!!")
			break
		if msg.content.startswith("4ears admin expcng"):
			log_append(msg.channel.id, str(msg.content), "adm","expcng")
			if "owner" in author_perm:
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
				log_append(msg.channel.id,"access denied - "+log_text, "adm","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 내 주인님이 아니야!!")
			break
		if msg.content.startswith("4ears admin cachcng"):
			log_append(msg.channel.id, str(msg.content), "adm","cscng")
			if "owner" in author_perm:
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
				log_append(msg.channel.id,"access denied - "+log_text, "adm","err")
				await bot.send_message(msg.channel,mention_user(user.user_id)+", 너는 내 주인님이 아니야!!")
			break
		if msg.content.startswith("4ears admin memo"):
			log_append(msg.channel.id, str(msg.content), "adm","mm")
			if "admin" in author_perm or "ch_admin" in author_perm :
				trg_list = msg.mentions
				if len(trg_list) == 1:
					text = mention_user(user.user_id)+", "
					trg_id = trg_list[0].id
					memo_status = quadra_memo(trg_id)
					if memo_status.memo_num == 0:
						text += mention_user(trg_id)+"는 메모를 쓴게 없어!"
						log_append(msg.channel.id, "list failed! : no memo", "adm","mm")
						await bot.send_message(msg.channel,text)
					else :
						text += mention_user(trg_id)+"의 메모를 찾았어!"
						log_append(msg.channel.id, "list check!", "adm","mm")
						em = discord.Embed(title="내가 기억하고 있는 것들이야!", colour=discord.Colour.blue())
						temp_int = 1
						for i in memo_status.memo_str:
							em.add_field(name=str(temp_int)+"번", value=i, inline=False)
							log_append(msg.channel.id,str(temp_int)+" : "+i, "mm_ck",0)
							temp_int += 1
						await bot.send_message(msg.channel,text,embed=em)					
			break
		break
