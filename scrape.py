# I  was with Canopy before. And here I am now.
# With Anaconda.
# Don't worry though. I'm not cheating.
# <3 <3

import requests
from bs4 import BeautifulSoup
import pandas as pd

url_to_scrape = 'http://www.espncricinfo.com/india-v-south-africa-2015-16/engine/match/903587.html'

r = requests.get(url_to_scrape)

soup = BeautifulSoup(r.text, 'lxml')

batting_table = soup.find(class_='batting-table innings')

player_names = []
runs = []
balls_taken = []
fours = []
sixes = []
strikeRate = []

for table_row in batting_table.find_all('tr')[1:]:
	table_cell = table_row.find_all('td')
	#print 'here i am'
	playerName = table_row.find(class_='playerName')
	if playerName != None:
		player = playerName.string.strip()
		player_names.append(player.encode('ascii'))
		runs_scored = table_cell[3].text.strip()
		runs.append(runs_scored.encode('ascii'))
		balls = table_cell[5].text.strip()
		balls_taken.append(balls.encode('ascii'))
		fours_scored = table_cell[6].text.strip()
		fours.append(fours_scored.encode('ascii'))
		sixes_scored = table_cell[7].text.strip()
		sixes.append(sixes_scored.encode('ascii'))
		SR = table_cell[8].text.strip()
		strikeRate.append(SR.encode('ascii'))

battingTable = {'Player':player_names,
		'Runs Scored':runs, 
		'Balls taken':balls_taken, 
		'4s':fours, 
		'6s':sixes,
		'Strike rate':strikeRate}

recTable = pd.DataFrame(battingTable, columns = ['Player',
						 'Runs Scored', 
						 'Balls taken', 
						 '4s', 
						 '6s', 
						 'Strike rate'])

print recTable
