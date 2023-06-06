# Sports book arbitrage (this sample program is NBA games)
#  source url: 
#				betus.com.pa
#  2nd source url: 
#				bovada.lv
############
# by Croo
############


# ver 1.0 notes 
###
#	need to update to pull the decimal values to allow greater accuracy
#	need to add all games currently only pulling the first game from each website & only basketball


#	need to navigate JSON tables more effectively/clean code
###

import re
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime


class nbagame:
	def __init__(self, time, home, away, homebu, awaybu, homebv, awaybv):
		self.time = time
		self.home = home
		self.away = away
		self.homebu = int(homebu)
		self.homebv = int(homebv)
		self.awaybu = int(awaybu)
		self.awaybv = int(awaybv)
		
		
		
		if self.homebu > 0:
			self.homebu = 1 + (self.homebu/100)
		else:
			self.homebu = 1 - (100/self.homebu)
			
		if self.homebv > 0:
			self.homebv = 1 + (self.homebv/100)
		else:
			self.homebv = 1 - (100/self.homebv)
			
		if self.homebu > 0:
			self.awaybu = 1 + (self.awaybu/100)
		else:
			self.awaybu = 1 - (100/self.awaybu)
			
		if self.homebu > 0:
			self.awaybv = 1 + (self.awaybv/100)
		else:
			self.awaybv = 1 - (100/self.awaybv)
		
		self.homebu = round(self.homebu, 2)
		self.homebv = round(self.homebv, 2)
		self.awaybu = round(self.awaybu, 2)
		self.awaybv = round(self.awaybv, 2)
		
	
	def calc_odds(self):
		odds = int((1/self.homebu + 1/self.awaybv) * 100)
		odds2 = int((1/self.homebv + 1/self.awaybu) * 100)
		
		
		if odds < 100:
			print("Game time: ", self.time, " Betus Home: ", self.homebu, " & ", "Bovada Away ", self.awaybv, " Arbitrage: ", odds)
			
		if odds2 < 100:
			print("Game time: ", self.time, " Bovada Home: ", self.homebv, " & ", "Betus Away ", self.awaybu, " Arbitrage: ", odds)

#if __name__ == '__main__':			
	
betus_url = requests.get("https://www.betus.com.pa/sportsbook/nba-basketball-odds.aspx")
bovada_url_data = requests.get("https://www.bovada.lv/services/sports/event/v2/events/A/description/basketball/nba")

betus_soup = BeautifulSoup(betus_url.content, 'lxml')
bovada_soup = BeautifulSoup(bovada_url_data.content, 'lxml')
bv_soup = bovada_soup.body.p.get_text()
bv_json = json.loads(bv_soup)

date_1 = (betus_soup.find_all("span", attrs={"class":"date font-weight-normal"})[0]).get_text()
#date_1 = (betus_soup.find_all("span", attrs={"class":"date font-weight-normal"})[1]).get_text()

date_1 = str(date_1)
date_1 = date_1.replace('\xa0', ' ')
date_1 = date_1.replace(' EST', '')
date_1 = datetime.strptime(date_1, '%a, %b %d, %Y')
game1 = [] * 5
game1.append(date_1)




placeholder = (betus_soup.find_all("span", attrs={"id":"homeName"})[0]).get_text()
placeholder = placeholder.replace('\n', '')
game1.append(placeholder)

placeholder = (betus_soup.find_all("span", attrs={"id": re.compile('.*HomeMoneyLine.*')})[0]).get_text()
placeholder = placeholder.replace('+', '')
game1.append(placeholder)

placeholder = (betus_soup.find_all("span", attrs={"id":"awayName"})[0]).get_text()
placeholder = placeholder.replace('\n', '')
game1.append(placeholder)

placeholder = (betus_soup.find_all("span", attrs={"id": re.compile('.*VisitorMoneyLine.*')})[0]).get_text()
placeholder = placeholder.replace('+', '')
game1.append(placeholder)



path = bv_json[0]
events = path['events'][0]
bv_time = (events['link'][44], events['link'][45], events['link'][46], events['link'][47], events['link'][48],events['link'][49],events['link'][50],events['link'][51])
bv_time = ''.join(bv_time)
bv_date = datetime.strptime(bv_time, '%Y%m%d')
display = events['displayGroups'][0]
markets = display['markets'][0]
outcomes = markets['outcomes'][0]
homebv = markets['outcomes'][1]
description = outcomes['description'] #this is the away team in game 1 aka the first listed game equivalent to game1[3]
									  # to verify home or away check outcome -> type should be 'A' or 'H'
price = outcomes['price']['american'] 
price = price.replace('+', '')

homebv_desc = homebv['description']
homeprice = homebv['price']['american']
homeprice = homeprice.replace('+', '')

if game1[0] == bv_date:
	gamedate = game1[0]
	
if game1[3] == description:
	gameteamaway = game1[3]
	
if game1[1] == homebv_desc:
	gameteamhome = game1[1]
	
	
game_1 = nbagame(gamedate, gameteamhome, gameteamaway, game1[2], game1[4], homeprice, price)
game_1.calc_odds()		
