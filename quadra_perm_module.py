import os
import random
import quadra_config
import time

class server_permission:
	server_id = ""
	allow_channel = []
	allow_nsfw = []
	def __init__(self,_server_id):
		self.server_id = str(_server_id)
		profile_name = "server_allow/"+str(_server_id)+".txt"
		if os.path.exists(profile_name) == False:
			fp = open(profile_name, 'w')
			fp.write("\n")
			fp.close()
		fp = open(profile_name,'r')
		server_raw = fp.readlines()
		fp.close()
		profile_name = "server_nsfwallow/"+str(_server_id)+".txt"
		if os.path.exists(profile_name) == False:
			fp = open(profile_name, 'w')
			fp.write("\n")
			fp.close()
		fp = open(profile_name,'r')
		nsfw_raw = fp.readlines()
		fp.close()
		for i in server_raw:
			self.allow_channel.append((i.split('\n'))[0])
		for i in nsfw_raw:
			self.allow_nsfw.append((i.split('\n'))[0])
		
	def basic_save(self):
		profile_name = "server_allow/"+str(self.server_id)+".txt"
		fp = open(profile_name, 'w')
		if len(self.allow_channel) == 1: fp.write("\n")
		else:
			for i in self.allow_channel:
				fp.write(str(i)+"\n")
		fp.close()
		
	def nsfw_save(self):
		profile_name = "server_nsfw/"+str(self.server_id)+".txt"
		fp = open(profile_name, 'w')
		if len(self.allow_nsfw) == 1: fp.write("\n")
		else:
			for i in self.allow_nsfw:
				fp.write(str(i)+"\n")
		fp.close()
	
	def perm_check(self,type,argument):
		if type == "basic":
			if argument in self.allow_channel: return True
			elif len(self.allow_channel) == 1 : return True
			else: return False
		if type == "nsfw":
			if argument in self.allow_nsfw: return True
			elif len(self.allow_nsfw) == 1 : return False
			else: return False
			
	def perm_check_admin(self,type,argument):
		if type == "basic":
			if argument in self.allow_channel: return True
			else: return False
		if type == "nsfw":
			if argument in self.allow_nsfw: return True
			else: return False
	
	def add(self, type, argument):
		if type == "basic":
			self.allow_channel.append(str(argument))
			self.basic_save()
		if type == "nsfw":
			self.allow_nsfw.append(str(argument))
			self.nsfw_save()

	def delete(self, type, argument):
		if type == "basic":
			self.allow_channel.remove(str(argument))
			self.basic_save()
		if type == "nsfw":
			self.allow_nsfw.remove(str(argument))
			self.nsfw_save()
	
	def delete_all(self, type):
		if type == "basic":
			profile_name = "server_allow/"+str(self.server_id)+".txt"
			fp = open(profile_name, 'w')
			fp.write("\n")
			fp.close()
		if type == "nsfw":
			profile_name = "server_nsfw/"+str(self.server_id)+".txt"
			fp = open(profile_name, 'w')
			fp.write("\n")
			fp.close()