import time, os, glob


LOG_PATH = "log/quadra_bot_log"

def log_append(chat_id, text, maintype, subtype):
	"""Print logs on terminal and append it on file.

Set LOG_PATH on top of this page to change the file's name. DO NOT ADD ".txt"
All arguments excluding _chat_id must be string. _chat_id can be either string or integer.

Log message will be shown as

[(time)] trgd [<maintype>\_<subtype>] from [<chat\_id>] : <text>

If there are no subtype, make sure subtype is integer "0". this is only exception subtype can get to know there are only maintype.
	"""
	_now = time.localtime()
	if subtype!=0 : what_type = maintype +'_' +subtype
	else : what_type = maintype
	target = "[%04d-%02d-%02d %02d:%02d:%02d] trgd [%10s] from [%15s] : %s" % (_now.tm_year, _now.tm_mon, _now.tm_mday, _now.tm_hour, _now.tm_min, _now.tm_sec, what_type,str(chat_id),text)	
	fp = open(LOG_PATH+".txt", 'a')
	if os.path.getsize(LOG_PATH+".txt") >= 102400:
		fp.close()
		filelist = glob.glob("log/*.*")
		filenum = len(filelist)
		filename = LOG_PATH+"_"+str(filenum)+".txt"
		os.rename(LOG_PATH+".txt",filename)
		fp = open(LOG_PATH+".txt", 'a')
	print(target)
	fp.write(target+"\n")
	fp.close()
	return _now