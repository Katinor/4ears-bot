import random

timer_0 = ["쿠울..쿨..zzZ","으으..깨우지마아...zzZ","헤헤..민트초코오..zzZ","새근새근.."]
timer_1 = ["흐아암.. 아침은 힘들어어...","오늘도 좋은아침..zzZ","끄아아~ 아침이다아~!"]
timer_2 = ["아침먹을 준비! 헤헤..","아침을 든든하게 먹어야 하루가 든든한거야!","당연히 식사준비지! 오늘 아침은 뭐야~?","기운나는 아침의 표효! 꺄아아아아앙!"]
timer_3 = ["독서는 아침을 깨워준다구","오늘도 모든 세계에 축복이 가득하게 해주세요..","모닝민초 한잔은 최고의 휴식이지!","그것보다 너야말로 일할 시간 아냐? 어디서 땡땡이야!"]
timer_4 = ["헤헤.. 나에게 더 맛있는 식사를 대접해달라구!","점심은 무얼 먹어볼까나~","여~ 식사는 했어?"]
timer_5 = ["역시 낮에는 낮잠이지..zzZ","우리 같이 노래부를래? 헤헤..","오늘도 행복하게 마무리짓자구!"]
timer_6 = ["오늘 저녁은 뭐야~? 헤헤...","역시 하루의 마지막은 풍성하게 먹어야지!","흐아암~ 이제야 쉬겠는걸?"]
timer_7 = ["하루가 끝나가면 쉬어야지. 게임이라던가?","배부르니까 한숨 더 자볼까나~","오늘을 마무리하는데에는 역시 콜라 한잔이지!"]
timer_8 = ["오늘 하루도 수고했어. 그렇게 내일도 더 멋지게 살아보자.","잘자! 내일도 행복하자구","오늘도 이렇게 지나가는구나...","오늘도 행복한 하루!"]

def checkSwitch(now):
	if 0 <= now.tm_hour < 6:
		return random.choice(timer_0)
	elif 6 <= now.tm_hour < 7:
		return random.choice(timer_1)
	elif 7 <= now.tm_hour < 8:
		return random.choice(timer_2)
	elif 8 <= now.tm_hour < 12:
		return random.choice(timer_3)
	elif 12 <= now.tm_hour < 13:
		return random.choice(timer_4)
	elif 13 <= now.tm_hour < 18:
		return random.choice(timer_5)
	elif 18 <= now.tm_hour < 19:
		return random.choice(timer_6)
	elif 19 <= now.tm_hour < 22:
		return random.choice(timer_7)
	elif now.tm_hour >= 22:
		return random.choice(timer_8)
	else:
		return "오늘도 행복한 하루!"