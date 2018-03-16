import os
import random

def enable(user_id):
	profile_name = "lotto_database/"+str(user_id)+".txt"
	if os.path.exists(profile_name):
		return True
	else:
		return False

def start(user_id):
	profile_name = "lotto_database/"+str(user_id)+".txt"
	if enable(user_id):
		return -1
	else:
		answer = [10,10,10,10,10,10,10]
		for i in range(0,7,1):
			swt = True
			while(swt):
				temp = random.randrange(1,36)
				if temp in answer:
					continue
				else:
					answer[i] = temp
					swt = False
		bonus = answer.pop(6)
		answer.sort()
		fp = open(profile_name, 'a')
		for i in answer:
			fp.write(str(i))
			fp.write("\n")
		fp.write(str(bonus))
		fp.close()
		ret_ans = ""
		for i in answer:
			ret_ans += str(i) + " "
		ret_ans += ":" + str(bonus)
		return ret_ans

def gameManager(target,answer,bonus):
	strike = 0
	for i in target:
		if i in answer:
			strike += 1
	if strike == 6: return 1
	elif strike == 5 and bonus in target: return 2
	else :return 8 - strike

def check(user_id):
	profile_name = "lotto_database/"+str(user_id)+".txt"
	if enable(user_id):
		fp = open(profile_name,'r')
		target = fp.readlines()
		fp.close()
		for i in range(0,len(target),1):
			target[i] = int((target[i].split('\n'))[0])
		bonus = target.pop(6)
		return [target,bonus]
		
def check_input(string):
	temp = string.split(' ')
	target = [0,0,0,0,0,0]
	for i in range(0,len(temp),1):
		target[i] = int(temp[i])
	return target

def check_equal(target):
	for i in target:
		if target.count(i) >= 2 : return False
	return True

def end(user_id):
	profile_name = "lotto_database/"+str(user_id)+".txt"
	os.remove(profile_name)