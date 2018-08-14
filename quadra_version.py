import discord
from quadra_log_module import log_append
from quadra_config import VERSION_INFO
import asyncio

def mention_user(user_id):
	return "<@"+str(user_id)+">"

def help_em_make(flag):
	text = "궁금한게 있으면 \"사잽아 <카테고리 이름> 도와줘\" 라고 다시 물어봐줘!"
	em = discord.Embed(title="여길 누르면 지원채널로 갈 수 있어!",description=text, colour=discord.Colour.blue(), url = "https://discord.gg/nywZ29w")
	em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")
	em.set_footer(text = VERSION_INFO + "\nCopyrightⓒ2017-2018 Katinor. All rights reserved.")
	if flag == "main":
		em = help_main(em)
		text = "이건 \"총괄\" 카테고리의 도움말이야!"
	elif flag == "약관":
		em = help_notice(em)
		text = "이건 \"약관\" 카테고리의 도움말이야!"
	elif flag == "일상대화":
		em = help_life(em)
		text = "이건 \"일상대화\" 카테고리의 도움말이야!"
	elif flag == "사용자":
		em = help_user(em)
		text = "이건 \"사용자\" 카테고리의 도움말이야!"
	elif flag == "게임":
		em = help_game(em)
		text = "이건 \"게임\" 카테고리의 도움말이야!"
	elif flag == "검색":
		em = help_search(em)
		text = "이건 \"검색\" 카테고리의 도움말이야!"
	elif flag == "메모":
		em = help_memo(em)
		text = "이건 \"메모\" 카테고리의 도움말이야!"
	elif flag == "번역":
		em = help_trans(em)
		text = "이건 \"번역\" 카테고리의 도움말이야!"
	elif flag == "기타":
		em = help_etc(em)
		text = "이건 \"기타\" 카테고리의 도움말이야!"
	elif flag == "겔부루":
		em = help_gel(em)
		text = "이건 \"겔부루\" 카테고리의 도움말이야!"
	elif flag == "네코":
		em = help_neko(em)
		text = "이건 \"네코\" 카테고리의 도움말이야!"
	else:
		em = help_main(em) 
		text = "카테고리가 잘못되어있어! \"총괄\" 카테고리를 대신 보여줄께."
	return text, em

def help_main(em):
	text="사잽아 <카테고리> 도와줘, 사잽아 이용약관, 사잽아 누구니, 사잽아 저작권, 사잽아 보고싶어"
	em.add_field(name = "약관", value = text)
	text="사잽아, 사잽아 뭐하니, 사잽아 놀아줘, 사잽아 안녕"
	em.add_field(name = "일상대화", value = text)
	text="사잽아 <문자열> 어때, 사잽아 용돈줘"
	em.add_field(name = "사용자", value = text)
	text="사잽아 <게임이름> 하자, 사잽아 <문자열> 해줘/할래"
	em.add_field(name = "게임", value = text)
	text="사잽아 <문자열> 찾아줘"
	em.add_field(name = "검색", value = text)
	text="사잽아 <문자열> 기억해줘, 사잽아 <문자열> 알려줘, 사잽아 <문자열> 잊어줘"
	em.add_field(name = "메모", value = text)
	text="사잽아 <언어코드>로 <문자열> 번역해줘"
	em.add_field(name = "번역", value = text)
	text="사잽아 네코"
	em.add_field(name = "기타", value = text)
	return em

def help_notice(em):
	#"사잽아 <카테고리> 도와줘, 사잽아 이용약관, 사잽아 누구니, 사잽아 저작권, 사잽아 보고싶어"
	text="해당 카테고리의 도움말을 보여줍니다. <카테고리>가 없으면 기존의 도움말이 나옵니다."
	em.add_field(name = "사잽아 <카테고리> 도와줘", value = text)
	text="사잽이봇의 이용약관을 보여줍니다. 사잽이봇을 사용하시는 동안에는 약관에 동의한 것으로 간주하니 꼭 확인하시기 바랍니다."
	em.add_field(name = "사잽아 이용약관", value = text)
	text="사잽이봇의 저작자와 저작권자를 알려줍니다."
	em.add_field(name = "사잽아 누구니 & 사잽아 저작권", value = text)
	text="사잽이 그림을 보여줍니다."
	em.add_field(name = "사잽아 보고싶어", value = text)
	return em

def help_life(em):
	#"사잽아, 사잽아 뭐하니, 사잽아 놀아줘, 사잽아 안녕"
	text ="사잽아, 사잽아 뭐하니, 사잽아 놀아줘, 사잽아 안녕\n"
	text+="전부 사잽이의 일상을 듣는 명령어입니다.\n"
	text+="너무 잦은 대화는 사잽이가 싫어해요!"
	em.add_field(name = "일상대화", value = text)
	return em
	
def help_user(em):
	#"사잽아 <문자열> 어때, 사잽아 용돈줘
	text ="<문자열>의 내용에 따라 다른 결과를 냅니다.\n"
	text+="\"나\"일 경우 당신의 프로필을 보여줍니다.\n"
	text+="다른 사람을 언급한 경우 그 사람의 프로필을 보여줍니다.\n"
	text+="이상한걸 물으면 거기에 따른 대가를 받게 됩니다."
	em.add_field(name = "사잽아 <문자열> 어때", value = text)
	text="하루에 한 번만 사용가능합니다. 지원금을 받습니다."
	em.add_field(name = "사잽아 용돈줘", value = text)
	return em
	
def help_game(em):
	#"사잽아 <게임이름> 하자, 사잽아 <문자열> 해줘/할래"
	text ="야구게임, 업다운, 로또(판당 1000원)"
	em.add_field(name = "제공되는 게임들", value = text)
	text ="해당 게임을 시작합니다."
	em.add_field(name = "사잽아 <게임이름> 하자", value = text)
	text ="이 명령어를 요구하는 게임일 경우 거기에 맞은 결과를 줍니다.\n게임을 시작할 때의 도움말을 잘 읽어보세요!"
	em.add_field(name = "사잽아 <문자열> 해줘/할래", value = text)
	return em

def help_search(em):
	#"사잽아 <문자열> 찾아줘"
	text="지금은 기능이 완전하지 않습니다. 제대로 검색기능이라 보기도 좀 그렇네요. 죄송합니다."
	em.add_field(name = "면책조항", value = text)	
	text="사잽아 <엔진>에서 <문자열> 찾아줘\n이 명령을 통해 무언가를 찾을 수 있습니다. 찾아줘와 찾을 대상 사이에는 띄어써야 합니다!"
	em.add_field(name = "기능", value = text)
	text="\"<엔진>에서\"부분이 없다면 (즉, \"사잽아 <문자열> 찾아줘\" 형태면) 구글에서 찾습니다. 엔진이 아는 곳이라면 그 엔진에서 찾습니다.\n"
	text+="찾는 문자열이 등록된 사이트의 이름일경우 그 사이트로 가는 링크를 줍니다."
	em.add_field(name = "작동원리", value = text)
	text="구글, 네이버, 나무위키, 리브레위키, 위키백과, 구스위키, 백괴사전"
	em.add_field(name = "지원엔진", value = text)
	text="스팀 : 사잽이에게 등록된 게임이라면 그 게임의 정보를 줍니다.\n겔부루 : \"사잽아 겔부루 도와줘\"로 확인해주세요."
	em.add_field(name = "특수엔진", value = text)
	return em

def help_memo(em):
	#"사잽아 <문자열> 기억해줘, 사잽아 <문자열> 알려줘, 사잽아 <문자열> 잊어줘"
	text="메모는 한 사람 당 5개, 한 메모에 100자 이하만, 이스케이프 문자 (\\같은거) 사용금지."
	em.add_field(name = "메모 제한", value = text)
	text="해당 문자열을 빈 메모공간에 순서대로 기억합니다."
	em.add_field(name = "사잽아 <문자열> 기억해줘", value = text)
	text="해당 번호의 메모를 확인합니다. \"전부\"라고 쓰면 전부 보여줍니다."
	em.add_field(name = "사잽아 <문자열> 알려줘", value = text)
	text="해당 번호의 메모를 지웁니다. \"전부\"라고 쓰면 전부 지웁니다. 지운 메모는 공란으로 남는게 아니라, 다음 공간에 있는 메모를 당겨옵니다."
	em.add_field(name = "사잽아 <문자열> 잊어줘", value = text)
	return em

def help_trans(em):
	text="\"사잽아 <문자열> 번역해줘\"를 통해 다른 언어의 문장을 한글로 번역합니다.\n"
	text+="\"사잽아 <언어코드>로 <문자열> 번역해줘\"를 통해 결과물의 언어를 지정할 수 있습니다.\n"
	text+="제대로 번역이 안된다고 한다면, 길이를 줄이면서 하는 것도 좋은 방법입니다."
	em.add_field(name = "기본", value = text)
	text = "**한국어/한글, 일본어/일어, 중국어, 대만어, 영어**는 언어코드 대신 사용할 수 있습니다. 다른 경우에는 대부분 ISO 639-1 체계에 따릅니다.\n"
	text+= "아래 주소에서 언어코드를 확인하세요.\nhttps://cloud.google.com/translate/docs/languages"
	em.add_field(name = "언어코드", value = text)
	return em

def help_etc(em):
	text="\"사잽아 네코 도와줘\" 에서 확인하세요."
	em.add_field(name = "사잽아 네코", value = text)
	return em

def help_gel(em):
	text="사잽아 겔부루에서 <문자열> 찾아줘"
	em.add_field(name = "개요", value = text)
	text="문자열에 다음 단어들이 들어가면 그런 등급을 가진 그림을 무작위로 들고옵니다.\n채널이 사잽이에게 NSFW로 등록되지 않았을 경우 아무거나 태크가 안야한거로 인식되며, 야한거 태그는 무시됩니다."
	em.add_field(name = "아무거나, 야한거, 안야한거", value = text)
	text="띄어 쓴 태그 사이에는 +가 있는걸로 칩니다. +<태그>는 추가, -<태그>는 제외입니다."
	em.add_field(name = "태그 쓰는 방법", value = text)
	return em

def help_neko(em):
	text ="This bot use nekos.life API.\n"
	text+=" - https://discord.services/api/"
	em.add_field(name = "Copyright Notice", value = text)
	text="사잽아 네코 - 무작위 고양이소녀짤을 가져옵니다.\n사잽아 야한네코 - 무작위 야릇한 고양이소녀짤을 가져옵니다. 당연히 NSFW 전용입니다."
	em.add_field(name = "개요", value = text)
	text="\"사잽아 <태그> 네코\" 든 \"사잽아 네코 <태그>\" 든 어느쪽이던간에 태그를 입력하면 해당 태그에 맞는 짤을 가져옵니다.\n"
	text+="<태그>에 태그라고 쓰면 현재 채널에서 사용가능한 태그를 보여줍니다.\n"
	text+="\"사잽아 아무거나 네코\"라고 쓰면 일반적인 태그들 중 무작위 하나의 짤을 보여줍니다.\n"
	text+="\"사잽아 아무거나 야한네코\"라고 쓰면 위험한 태그들 중 무작위 하나의 짤을 보여줍니다.\n"
	em.add_field(name = "태그", value = text)
	return em

async def version(msg,user,flag,bot):
	chat_id = msg.channel.id
	log_append(chat_id, str(msg.content), "help",0)
	text, em = help_em_make(flag)
	user.mody(love = 1, love_time = True, exp = 5, exp_time = True)
	await bot.send_message(msg.channel,mention_user(user.user_id)+" "+"너에게 직접 보낼거야! 확인해봐!")
	await bot.send_message(msg.author,text,embed=em)

async def credit_view(msg,user,bot,perm = False):
	chat_id = msg.channel.id
	log_append(chat_id, str(msg.content), "credit",0)
	text="4ears_bot Copyright Notice"
	em = discord.Embed(title="여길 누르면 블로그로 갈 수 있어!",description=text, colour=discord.Colour.blue(), url = "https://blog.4ears.net/%EC%82%AC%EC%9E%BD%EC%9D%B4%EB%B4%87/")
	em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")

	text ="ⓒ2017-2018, Katinor, All Right Reserved.\n"
	text+=" - katinor@4ears.net"
	em.add_field(name = "QuadraEarsBot & 4ears_bot", value = text)
	
	text ="ⓒ2017, Muku, All Right Reserved.\n"
	text+=" - https://www.pixiv.net/member.php?id=5882068"
	text+="Katinor who make this bot received the Public Transmission Right of this illustration (that is protected under the Copyright law of Korea)."
	em.add_field(name = "Portrait of Character", value = text)
	
	text ="This bot use nekos.life API.\n"
	text+=" - https://discord.services/api/"
	em.add_field(name = "Etc", value = text)

	text ="This bot is licensed, not sold. This bot's TOU only gives you some rights to use it.\n"
	text+="Katinor reserves all other rights. This means you cannot reverse engineer, decompile or disassemble this bot, or otherwise attempt to derive the source code for the software except, and solely to extent: permitted by applicable law, despite this limitation\n"
	text+="Despite above, you can use this bot's \"Clean Build\" code repository under the AGPLv3.0\n"
	text+=" - https://github.com/Katinor/quadra_ears_bot_discord/"
	em.add_field(name = "Software License Terms", value = text)

	user.mody(love = 1, love_time = True, exp = 5, exp_time = True)
	if perm:
		await bot.send_message(msg.channel,embed=em)
	else:
		await bot.send_message(msg.channel,mention_user(user.user_id)+" "+"너에게 직접 보낼거야! 확인해봐!")
		await bot.send_message(msg.author,embed=em)

async def tou_view(msg,user,bot,perm = False):
	chat_id = msg.channel.id
	log_append(chat_id, str(msg.content), "TOU",0)
	text="사잽이 이용약관"
	em = discord.Embed(title="여길 누르면 지원채널로 갈 수 있어!",description=text, colour=discord.Colour.blue(), url = "https://discord.gg/nywZ29w")
	em.set_thumbnail(url="https://i.imgur.com/pg7K8cQ.png")

	text ="사잽이봇은 서비스 제공을 위해 다음과 같은 정보를 수집합니다.\n"
	text+=" - 사잽이가 반응하는 대화에 포함된 데이터\n"
	text+=" - 채팅이 보내진 시간\n"
	text+=" - 작성자의 고유번호\n"
	text+=" - 작성된 서버의 고유번호\n"
	text+=" - 작성된 서버내의 채널의 고유번호"
	em.add_field(name = "수집하는 정보", value = text)
	
	text ="사잽이봇은 수집되는 정보를 본 용도로만 사용하며, 아래 명시된 용도 외에는 보관 및 사용되지 않습니다.\n"
	text+=" - 반응했을 경우의 디버깅을 위한 로그\n"
	text+=" - 서비스 제공 (호감도, 게임) 등을 위한 데이터베이스 구축"
	em.add_field(name = "수집된 정보의 사용", value = text)

	text ="본 봇과 1:1 대화를 하거나, 본 봇을 그룹에 초대하는 행위를 한다면 본 약관에 동의한 것으로 간주합니다."
	em.add_field(name = "이용약관의 동의", value = text)
	
	text ="사용자가 이용약관에 반대할 경우 언제든지 서비스 받기를 중단할 수 있습니다. 이를 위해서는 그저 사용자가 본 봇과의 1:1 채팅을 그만두거나, 초대한 서버/그룹/채널에서 본 봇을 내보내기만 하면 됩니다. 그러나, 기존 서비스 이용 기록 (위의 정보의 \"보관\")은 삭제되지 않습니다. 특별한 사유가 있다면 카티노르에게 문의해주시기 바랍니다."
	em.add_field(name = "이용계약의 해지", value = text)

	text ="사잽이봇은 국가의 명령이 있을 경우 그 기록을 수사기관에 제공할 수 있습니다. 그러니 애한테 위법적인것좀 시키지 마세요."
	em.add_field(name = "국가기관과의 협조", value = text)
	user.mody(love = 1, love_time = True, exp = 5, exp_time = True)
	if perm:
		await bot.send_message(msg.channel,embed=em)
	else:
		await bot.send_message(msg.channel,mention_user(user.user_id)+" "+"너에게 직접 보낼거야! 확인해봐!")
		await bot.send_message(msg.author,embed=em)