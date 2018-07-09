import random
from quadra_config import LIFETIME_TIMER, LIFETIME_DUP_TIMER


d_timer_0 = ["그만해. 자는데 방해하지 말고.",
"급한일도 아닌데 왜 깨워..",
".. 괜히 깨우지 말아줘..",
"급한일이 아니면, 아침에 불러줄래?",
"미안해. 지금은 너무 피곤해.. 나중에 불러줘...",
"미안해. 지금은 너무 피곤해.. 조금만 더 자게 해줘.",
"지금은 새벽이라구.. 조금만 더 잘게 ㅠㅠ"]
d_timer_1 = ["흐아암.. 아침은 힘들어어...","오늘도 좋은아침..zzZ","끄아아~ 아침이다아~!"]
d_timer_2 = ["아침먹을 준비! 헤헤..","아침을 든든하게 먹어야 하루가 든든한거야!","당연히 식사준비지! 오늘 아침은 뭐야~?","기운나는 아침의 표효! 꺄아아아아앙!"]
d_timer_3 = ["독서는 아침을 깨워준다구","오늘도 모든 세계에 축복이 가득하게 해주세요..","모닝민초 한잔은 최고의 휴식이지!","그것보다 너야말로 일할 시간 아냐? 어디서 땡땡이야!"]
d_timer_4 = ["헤헤.. 나에게 더 맛있는 식사를 대접해달라구!","점심은 무얼 먹어볼까나~","여~ 식사는 했어?"]
d_timer_5 = ["역시 낮에는 낮잠이지..zzZ","우리 같이 노래부를래? 헤헤..","오늘도 행복하게 마무리짓자구!"]
d_timer_6 = ["오늘 저녁은 뭐야~? 헤헤...","역시 하루의 마지막은 풍성하게 먹어야지!","흐아암~ 이제야 쉬겠는걸?"]
d_timer_7 = ["하루가 끝나가면 쉬어야지. 게임이라던가?","배부르니까 한숨 더 자볼까나~","오늘을 마무리하는데에는 역시 콜라 한잔이지!"]
d_timer_8 = ["오늘 하루도 수고했어. 그렇게 내일도 더 멋지게 살아보자.","잘자! 내일도 행복하자구","오늘도 이렇게 지나가는구나...","오늘도 행복한 하루!"]

def checkSwitch(now):
	if 0 <= now.tm_hour < 6:
		return random.choice(LIFETIME_TIMER["timer_0"])
	elif 6 <= now.tm_hour < 7:
		return random.choice(LIFETIME_TIMER["timer_1"])
	elif 7 <= now.tm_hour < 8:
		return random.choice(LIFETIME_TIMER["timer_2"])
	elif 8 <= now.tm_hour < 12:
		return random.choice(LIFETIME_TIMER["timer_3"])
	elif 12 <= now.tm_hour < 13:
		return random.choice(LIFETIME_TIMER["timer_4"])
	elif 13 <= now.tm_hour < 18:
		return random.choice(LIFETIME_TIMER["timer_5"])
	elif 18 <= now.tm_hour < 19:
		return random.choice(LIFETIME_TIMER["timer_6"])
	elif 19 <= now.tm_hour < 22:
		return random.choice(LIFETIME_TIMER["timer_7"])
	elif now.tm_hour >= 22:
		return random.choice(LIFETIME_TIMER["timer_8"])
	else:
		return "오늘도 행복한 하루!"

def checkSwitch2(now, level):
	if 0 <= now.tm_hour < 6:
		return LIFETIME_DUP_TIMER["timer_0"][level-1]
	elif 6 <= now.tm_hour < 7:
		return LIFETIME_DUP_TIMER["timer_1"][level-1]
	elif 7 <= now.tm_hour < 8:
		return LIFETIME_DUP_TIMER["timer_2"][level-1]
	elif 8 <= now.tm_hour < 12:
		return LIFETIME_DUP_TIMER["timer_3"][level-1]
	elif 12 <= now.tm_hour < 13:
		return LIFETIME_DUP_TIMER["timer_4"][level-1]
	elif 13 <= now.tm_hour < 18:
		return LIFETIME_DUP_TIMER["timer_5"][level-1]
	elif 18 <= now.tm_hour < 19:
		return LIFETIME_DUP_TIMER["timer_6"][level-1]
	elif 19 <= now.tm_hour < 22:
		return LIFETIME_DUP_TIMER["timer_7"][level-1]
	elif now.tm_hour >= 22:
		return LIFETIME_DUP_TIMER["timer_8"][level-1]
	else:
		return "귀찮게 하지 말아줘.."