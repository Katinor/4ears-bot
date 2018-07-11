import os
import random
import quadra_config
import time
from quadra_log_module import log_append

class server_permission:
	"""server_permission class is called to check specific channel's permission.
Basically, 4ears_bot needs to get permission of channel to respond user's command.

parameter:
 server_id : (string) targeted server's id number.
 allow_channel : (string[]) list of channel's id that 4ears_bot can say. each server has their own list.
 allow_nsfw : (string[]) list of channel's id that 4ears_bot can do some erotical things. each server has their own list.
	"""
	server_id = ""
	allow_channel = []
	allow_nsfw = []

	def __init__(self,_server_id):
		self.server_id = str(_server_id)
		self.allow_channel = []
		self.allow_nsfw = []
		profile_name = "server_allow/"+str(_server_id)+".txt"
		if os.path.exists(profile_name) == False:
			fp = open(profile_name, 'w')
			fp.write("\n")
			fp.close()
		fp = open(profile_name,'r')
		server_raw = fp.readlines()
		fp.close()
		profile_name = "server_nsfw/"+str(_server_id)+".txt"
		if os.path.exists(profile_name) == False:
			fp = open(profile_name, 'w')
			fp.write("\n")
			fp.close()
		fp = open(profile_name,'r')
		nsfw_raw = fp.readlines()
		fp.close()
		for i in server_raw:
			self.allow_channel.append((i.split('\n'))[0])
		while(True) :
			try : self.allow_channel.remove("")
			except Exception : break
		for i in nsfw_raw:
			self.allow_nsfw.append((i.split('\n'))[0])
		while(True) :
			try : self.allow_nsfw.remove("")
			except Exception : break

	def basic_save(self):
		profile_name = "server_allow/"+str(self.server_id)+".txt"
		fp = open(profile_name, 'w')
		if len(self.allow_channel) == 0: fp.write("\n")
		else:
			for i in self.allow_channel:
				fp.write(str(i)+"\n")
		fp.close()
		
	def nsfw_save(self):
		profile_name = "server_nsfw/"+str(self.server_id)+".txt"
		fp = open(profile_name, 'w')
		if len(self.allow_nsfw) == 0: fp.write("\n")
		else:
			for i in self.allow_nsfw:
				fp.write(str(i)+"\n")
		fp.close()
	
	def perm_check(self,type,argument):
		if type == "basic":
			if argument in self.allow_channel: return True
			elif len(self.allow_channel) == 0 : return True
			else: return False
		if type == "nsfw":
			if argument in self.allow_nsfw: return True
			elif len(self.allow_nsfw) == 0 : return False
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
			while(True) :
				try : self.allow_channel.remove("")
				except Exception as ex: break
			self.basic_save()
		if type == "nsfw":
			self.allow_nsfw.append(str(argument))
			while(True) :
				try : self.allow_nsfw.remove("")
				except Exception as ex: break
			self.nsfw_save()

	def delete(self, type, argument):
		if type == "basic":
			self.allow_channel.remove(str(argument))
			while(True) :
				try : self.allow_channel.remove("")
				except Exception as ex: break
			self.basic_save()
		if type == "nsfw":
			self.allow_nsfw.remove(str(argument))
			while(True) :
				try : self.allow_nsfw.remove("")
				except Exception as ex: break
			self.nsfw_save()
	
	def delete_all(self, type):
		if type == "basic":
			profile_name = "server_allow/"+str(self.server_id)+".txt"
			fp = open(profile_name, 'w')
			fp.write("\n")
			fp.close()
			self.allow_channel = []
		if type == "nsfw":
			profile_name = "server_nsfw/"+str(self.server_id)+".txt"
			fp = open(profile_name, 'w')
			fp.write("\n")
			fp.close()
			self.allow_nsfw = []

class user_permission:
	owner = []
	admin = []
	blocked = []

	def __init__(self):
		self.owner = [quadra_config.OWNER]
		self.admin = []
		self.blocked = []
		fp = open('quadra_admin.txt','r')
		target = fp.readlines()
		for i in range(0,len(target)-1,1):
			self.admin.append((target[i].split('\n'))[0])
		fp.close()
		fp = open('quadra_block.txt','r')
		target = fp.readlines()
		for i in range(0,len(target)-1,1):
			self.blocked.append((target[i].split('\n'))[0])
		fp.close()
		
	def admin_add(self, user):
		user_id = str(user.id)
		if user_id in self.admin:
			temp_text = user.name+"#"+user.discriminator+" : "+user.id
			log_append("perm_module","already admin - "+temp_text, "adm","add")
			return 1
		elif user.bot:
			temp_text = user.name+"#"+user.discriminator+" : "+user.id
			log_append("perm_module","you cannot add bot to admin group - "+temp_text, "adm","add")
			return 2
		else:
			self.admin.append(user_id)
			temp_text = user.name+"#"+user.discriminator+" : "+user.id
			log_append("perm_module","success to append - "+temp_text, "adm","add")
			return 0

	def admin_del(self, user):
		user_id = str(user.id)
		if user.bot:
			temp_text = user.name+"#"+user.discriminator+" : "+user.id
			log_append("perm_module","you cannot check bot - "+temp_text, "adm","del")
			return 2	
		elif user_id in self.admin:
			self.admin.remove(user_id)
			temp_text = user.name+"#"+user.discriminator+" : "+user.id
			log_append("perm_module","success to delete - "+temp_text, "adm","del")		
			return 0
		else:
			temp_text = user.name+"#"+user.discriminator+" : "+user.id
			log_append("perm_module","not admin - "+temp_text, "adm","del")
			return 1

	def admin_save(self):
		fp = open('quadra_admin.txt','w')
		for i in self.admin:
			fp.write(i+"\n")
		fp.close()

	def block(self, user, perm):
		user_id = str(user.id)
		if user_id in self.blocked:
			temp_text = user.name+"#"+user.discriminator+" : "+user.id
			log_append("perm_module","already blocked - "+temp_text, "bl","add")
			return 1
		elif user.bot:
			temp_text = user.name+"#"+user.discriminator+" : "+user.id
			log_append("perm_module","you cannot check bot - "+temp_text, "bl","add")
			return 2
		elif user_id in self.admin:
			if "owner" in perm:
				self.admin_del(user_id)
				self.admin_save()
				self.blocked.append(user_id)
				temp_text = user.name+"#"+user.discriminator+" : "+user.id
				log_append("perm_module","success to delete admin and block - "+temp_text, "bl","add")
				return 4
			temp_text = user.name+"#"+user.discriminator+" : "+user.id
			log_append("perm_module","you cannot block admin - "+temp_text, "bl","add")
			return 3
		else:
			self.blocked.append(user_id)
			temp_text = user.name+"#"+user.discriminator+" : "+user.id
			log_append("perm_module","success to block - "+temp_text, "bl","add")
			return 0

	def unblock(self, user, perm):
		user_id = str(user.id)
		if user.bot:
			temp_text = user.name+"#"+user.discriminator+" : "+user.id
			log_append("perm_module","you cannot check bot - "+temp_text, "bl","del")
			return 2	
		elif user_id in self.blocked:
			self.blocked.remove(user_id)
			temp_text = user.name+"#"+user.discriminator+" : "+user.id
			log_append("perm_module","success to unblock - "+temp_text, "bl","del")		
			return 0
		else:
			temp_text = user.name+"#"+user.discriminator+" : "+user.id
			log_append("perm_module","not blocked - "+temp_text, "bl","del")
			return 1

	def block_save(self):
		fp = open('quadra_blocked.txt','w')
		for i in self.blocked:
			fp.write(i+"\n")
		fp.close()

	def check(self, msg, user_id):
		perm = []
		if user_id in self.blocked: perm = []
		else: perm.append("user") 
		if user_id in self.owner:
			perm.append("owner")
			perm.append("admin")
		elif user_id in self.admin:
			perm.append("admin")
		if (msg.channel.permissions_for(msg.author)).administrator : perm.append("ch_admin")
		return perm
		

