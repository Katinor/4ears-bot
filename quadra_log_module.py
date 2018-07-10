import time, os, glob

def log_append(_chat_id, _text, _type, _subtype):
	_now = time.localtime()
	if _subtype!=0 : what_type = _type +'_' +_subtype
	else : what_type = _type
	target = "[%04d-%02d-%02d %02d:%02d:%02d] trgd [%10s] from [%15s] : %s" % (_now.tm_year, _now.tm_mon, _now.tm_mday, _now.tm_hour, _now.tm_min, _now.tm_sec, what_type,str(_chat_id),_text)	
	fp = open("log/quadra_bot_log.txt", 'a')
	if os.path.getsize("log/quadra_bot_log.txt") >= 102400:
		fp.close()
		filelist = glob.glob("log/*.*")
		filenum = len(filelist)
		filename = "log/quadra_bot_log_"+str(filenum)+".txt"
		os.rename("log/quadra_bot_log.txt",filename)
		fp = open("log/quadra_bot_log.txt", 'a')
	print(target)
	fp.write(target+"\n")
	fp.close()
	return _now