import os
import random
import time

MAX_MEMO_NUM = 5
MAX_MEMO_CAP = 100
FORBIDDEN_STRING = ["\n","\r","\t","\f","\a","\b","\000"]

class quadra_memo:
	user_id = ""
	memo_num = 0
	memo_str = []

	def __init__(self,_user_id):
		self.user_id = str(_user_id)
		self.memo_num = 0
		self.memo_str = []
		profile_name = "memo_database/"+str(_user_id)+".txt"
		if os.path.exists(profile_name) == True:
			fp = open(profile_name,'r')
			target = fp.readlines()
			fp.close()
			for i in range(0,len(target),1):
				target[i] = (target[i].split('\n'))[0]
			for i in target: self.memo_str.append(i)
			self.memo_num = len(self.memo_str)

	#resultcode:
	# 0 : Success
	# 1 : string stack overflow
	# 2 : capacity stack overflow
	# 3 : forbidden string included
	def append(self, target):
		profile_name = "memo_database/"+self.user_id+".txt"
		if len(target) > MAX_MEMO_CAP: return 1
		elif self.memo_num >= MAX_MEMO_NUM: return 2
		else:
			for i in FORBIDDEN_STRING:
				if i in target : return 3
			self.memo_str.append(target)
			fp = open(profile_name,'w')
			for i in range(0,len(self.memo_str),1):
				fp.write(self.memo_str[i]+"\n")		
			fp.close()
			return 0

	#resultcode:
	# 0 : Success
	# 1 : capacity stack overflow
	# 2 : num must be at least 1
	def delete(self, num):
		profile_name = "memo_database/"+self.user_id+".txt"
		if num <= 0 : return 2
		elif num > self.memo_num : return 1
		elif self.memo_num == 1:
			os.remove(profile_name)
			return 0
		else :
			fp = open(profile_name,'w')
			for i in range(0,len(self.memo_str),1):
				if i == num-1 : continue
				fp.write(self.memo_str[i]+"\n")
			fp.close()
			return 0

	#resultcode:
	# str : Success
	# 1 : capacity stack overflow
	# 2 : num must be at least 1
	def check(self, num):
		if num <= 0 : return 2
		elif num > self.memo_num : return 1
		else : return self.memo_str[num-1]

	def purge(self):
		profile_name = "memo_database/"+self.user_id+".txt"
		if os.path.exists(profile_name) == True:
			os.remove(profile_name)
			return 0
		else: return 1