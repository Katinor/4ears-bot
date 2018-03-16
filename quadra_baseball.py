import os
import random

def enable(user_id):
	profile_name = "baseball_database/"+str(user_id)+".txt"
	if os.path.exists(profile_name):
		return True
	else:
		return False

def start(user_id):
	profile_name = "baseball_database/"+str(user_id)+".txt"
	if enable(user_id):
		return -1
	else:
		answer = [10,10,10]
		for i in range(0,3,1):
			swt = True
			while(swt):
				temp = random.randrange(0,10)
				if temp in answer:
					continue
				else:
					answer[i] = temp
					swt = False
		answer = answer[0]*100+answer[1]*10+answer[2]
		fp = open(profile_name, 'a')		
		fp.write(str(answer))
		fp.write("\n")
		fp.write("0")
		fp.close()
		return answer

def gameManager(target,answer):
	alpha = [target//100,(target%100)//10,target%10]
	beta = [answer//100,(answer%100)//10,answer%10]
	strike = 0
	ball = 0
	for i in range(0,3,1):
		for j in range(0,3,1):
			if alpha[i] == beta[j]:
				if i == j: strike += 1
				else: ball += 1
	return [strike,ball]

def check(user_id):
	profile_name = "baseball_database/"+str(user_id)+".txt"
	if enable(user_id):
		fp = open(profile_name,'r')
		target = fp.readlines()
		target[1] = int(target[1])
		fp.close()
		return target

def check_equal(target):
	alpha = [target//100,(target%100)//10,target%10]
	for i in range(0,2,1):
		for j in range(i+1,3,1):
			if alpha[i] == alpha[j] : return False
	return True

def lose(user_id):
	profile_name = "baseball_database/"+str(user_id)+".txt"
	temp = check(user_id)
	temp[1] += 1
	fp = open(profile_name,'w')
	fp.write(str(temp[0])+str(temp[1]))
	fp.close()

def end(user_id):
	profile_name = "baseball_database/"+str(user_id)+".txt"
	os.remove(profile_name)