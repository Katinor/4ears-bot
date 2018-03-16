import os
import random

def enable(user_id):
	profile_name = "updown_database/"+str(user_id)+".txt"
	if os.path.exists(profile_name):
		return True
	else:
		return False

def start(user_id):
	profile_name = "updown_database/"+str(user_id)+".txt"
	if enable(user_id):
		return -1
	else:
		answer = random.randrange(0,100)
		fp = open(profile_name, 'a')		
		fp.write(str(answer))
		fp.write("\n")
		fp.write("0")
		fp.close()
		return answer

def gameManager(target,answer):
	if target > answer : return 1
	elif target < answer : return -1
	else : return 0

def check(user_id):
	profile_name = "updown_database/"+str(user_id)+".txt"
	if enable(user_id):
		fp = open(profile_name,'r')
		target = fp.readlines()
		target[0] = int(target[0])
		target[1] = int(target[1])
		fp.close()
		return target

def lose(user_id):
	profile_name = "updown_database/"+str(user_id)+".txt"
	temp = check(user_id)
	temp[1] += 1
	fp = open(profile_name,'w')
	fp.write(str(temp[0])+"\n"+str(temp[1]))
	fp.close()

def end(user_id):
	profile_name = "updown_database/"+str(user_id)+".txt"
	os.remove(profile_name)