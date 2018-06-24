import os
import random
import quadra_config
import time
import glob

LOVE_DELAY = 3
EXP_DELAY = 3
LOVE_GRADE = [-100,-70,-20,30,90,210,270,300]
REQ_EXP = [10]



MAX_LOVE = LOVE_GRADE[len(LOVE_GRADE)-1]
MIN_LOVE = LOVE_GRADE[0]

love_1 = ["무슨 낯짝으로 내 앞에 서있는건지 모르겠는데?","저리 가. 별로 보고싶지 않으니까.","굳이 내 앞에 서 있는 이유가 뭐야?"]
love_2 = ["참을 인도 쓰다보면 팔이 아프단것만 알아둬.","어.. 너구나. 안녕.","글쎄.. 굳이 표정을 찡그려줘야해?"]
love_3 = ["글쎄.. 어떨까나?","서로 알아갈 시간이 더 필요할거같아.","굳이 말하자면, 좋지도 싫지도 않은 정도?"]
love_4 = ["조금은 더 알아가고 싶은 사람, 정도로 괜찮을까?","적어도 밉지는 않아."]
love_5 = ["친구 정도로 생각하고 있어.","더 친해져보고 싶은사람!","음.. 문자 정도는 주고받을 수 있는 사이?"]
love_6 = ["너 정도면 믿음직한 친구지.","친구, 오늘은 어떻게 나와 놀아줄거야?","쫑긋! 너 정도면 좋은 친구지!"]
love_7 = ["쫑긋! ..헤헤","..부끄러워! 너무 가까이 오진 마..","넌 최고의 친구 중 한명이야!"]
love_cap = ["정말 싫어","조금 별로","그저 그래","아는 지인","친구","친한 친구","정말 좋아"]

supply_text = ["... 더 주기 싫으니까 빨리 받고 가.","...굳이 많이 필요없잖아? 이정도만 가져가.","자. 오늘의 지원금이야!","돈이 필요해? 아껴쓰라구!","오늘도 지원금이야! 많이는 못줘서 미안해~","최대한 주고싶은데, 이정도가 한계야.. 헤헤...","최대한 주고싶은데, 이정도가 한계야.. 헤헤..."]

for i in range(1,40,1):
	REQ_EXP.append(int((i+2)**(2))+REQ_EXP[i-1])
for i in range(40,70,1):
	REQ_EXP.append(int(REQ_EXP[i-1]*1.1))
for i in range(70,80,1):
	REQ_EXP.append(int(REQ_EXP[i-1]*1.15))
for i in range(80,90,1):
	REQ_EXP.append(int(REQ_EXP[i-1]*1.2))
for i in range(90,100,1):
	REQ_EXP.append(int(REQ_EXP[i-1]*1.3))

CASH_SOFTCAP = 1000000
EXP_HARDCAP = REQ_EXP[99] * 100

fp = open("quadra_level_require.txt",'w')
for i in REQ_EXP:
	fp.write(str(i)+"\n")
fp.close()
	
for i in range(1,len(REQ_EXP),1):
	REQ_EXP[i] = REQ_EXP[i]+REQ_EXP[i-1]

fp = open("quadra_level_total.txt",'w')
for i in REQ_EXP:
	fp.write(str(i)+"\n")
fp.close()

MAX_LEVEL = len(REQ_EXP)

class quadra_user:
	user_id = ""
	cash = 0
	cash_time = 0
	love = 0
	love_time = 0
	exp = 0
	exp_time = 0
	level = 0
	def __init__(self,_user_id):
		self.user_id = str(_user_id)
		profile_name = "user_database/"+str(_user_id)+".txt"
		if os.path.exists(profile_name) == False:
			fp = open(profile_name, 'w')
			for i in range(0,8,1):
				fp.write("0\n")
			fp.write("0")
			fp.close()
		fp = open(profile_name,'r')
		target = fp.readlines()
		fp.close()
		for i in range(0,len(target),1):
			if i < len(target)-1:target[i] = (target[i].split('\n'))[0]
			if i == 3 or i == 5: target[i] = float(target[i])
			else: target[i] = int(float(target[i]))
		self.cash = target[0]
		self.cash_time = target[1]
		self.love = target[2]
		self.love_time = target[3]
		self.exp = target[4]
		self.exp_time = target[5]
		self.level = target[6]
	
	def save(self):
		profile_name = "user_database/"+self.user_id+".txt"
		fp = open(profile_name, 'w')
		fp.write(str(self.cash)+"\n")
		fp.write(str(self.cash_time)+"\n")
		fp.write(str(self.love)+"\n")
		fp.write(str(self.love_time)+"\n")
		fp.write(str(self.exp)+"\n")
		fp.write(str(self.exp_time)+"\n")
		fp.write(str(self.level)+"\n")
		fp.close()
	
	def canSupply(self):
		if self.cash_time != int((time.localtime()).tm_mday): return True
		else: return False
	
	def mody(self, cash=0, cash_time=False, love=0, love_time=False,exp=0,exp_time=False):
		levelup = False
		if cash_time:
			if self.cash_time != int((time.localtime()).tm_mday): 
				self.cash += cash
				self.cash_time = int((time.localtime()).tm_mday)
		else: self.cash += cash
		if love_time:
			if self.love_time + LOVE_DELAY < time.time(): 
				self.love += love
				self.love_time = time.time()
		else: self.love += love
		if self.love > MAX_LOVE: self.love = MAX_LOVE
		if self.love < MIN_LOVE: self.love = MIN_LOVE
		if exp_time:
			if self.exp_time + EXP_DELAY < time.time(): 
				self.exp += exp
				self.exp_time = time.time()
		else: self.exp += exp
		if self.exp > EXP_HARDCAP: self.exp = EXP_HARDCAP
		if REQ_EXP[self.level-1] > self.exp:
			for i in range(0,len(REQ_EXP),1):
				if REQ_EXP[i] > self.exp:
					self.level = i
					break
		elif self.level < 100 and REQ_EXP[self.level] <= self.exp:
			levelup = True
			for i in range(0,len(REQ_EXP),1):
				if REQ_EXP[i] > self.exp:
					self.level = i
					break
			if self.level == 100 :
				_now = time.localtime()
				fp = open("quadra_MAX_LEVEL_note","a")
				fp.write("[%04d-%02d-%02d %02d:%02d:%02d][%d] %s\n"% (_now.tm_year, _now.tm_mon, _now.tm_mday, _now.tm_hour, _now.tm_min, _now.tm_sec,self.level,self.user_id))
				fp.close()
		self.save()
		return levelup

	def change(self, cash=None, love=None, exp=None, level=None):
		if cash != None: self.cash = cash
		if love != None: self.love = love
		if exp != None: self.exp = exp
		if self.exp > EXP_HARDCAP: self.exp = EXP_HARDCAP
		if REQ_EXP[self.level-1] > self.exp:
			for i in range(0,len(REQ_EXP),1):
				if REQ_EXP[i] > self.exp:
					self.level = i
					break
		elif REQ_EXP[self.level] <= self.exp:
			for i in range(0,len(REQ_EXP),1):
				if REQ_EXP[i] > self.exp:
					self.level = i
					break
		if level != None:
			self.level = int(level)
			self.exp = REQ_EXP[level-1]
		self.save()
	
	def love_level(self):
		temp = 0
		for i in LOVE_GRADE:
			if self.love < i: return temp
			temp += 1
		return len(LOVE_GRADE)-1
	
	def love_short(self):
		lev = self.love_level()
		return love_cap[lev-1]

	def love_text(self):
		lev = self.love_level()
		if lev == 1:
			return random.choice(love_1)
		elif lev == 2:
			return random.choice(love_2)
		elif lev == 3:
			return random.choice(love_3)
		elif lev == 4:
			return random.choice(love_4)
		elif lev == 5:
			return random.choice(love_5)
		elif lev == 6:
			return random.choice(love_6)
		else:
			return random.choice(love_7)
	
	def supply_text(self):
		lev = self.love_level()
		return supply_text[lev-1]

	def user_rank(self):
		user_list = glob.glob("user_database/*.*")
		user_exp = []
		trg_point = self.exp
		for i in user_list:
			fp = open(i,"r")
			target = fp.readlines()
			user_exp.append(int((target[4].split('\n'))[0]))
		fp.close()
		user_exp.sort()
		user_exp.reverse()
#		fp = open("exp_list.txt","w")
#		for i in user_exp:
#			fp.write(str(i)+"\n")
#		fp.close()
		return (user_exp.index(trg_point)+1,len(user_exp))