from random import randint, shuffle
from math import sqrt

def generate_teams():
	teams = []
	for i in range(16):
		teams.append(i+1)
	return teams
	
def generate_points(teams):
	points = []
	for i in teams:
		points.append([i,0])
	return points
		
def generate_first_day(teams):
	first_day = []
	teamList = teams.copy()
	for i in range(int(len(teamList)/2)):
		away = randint(1,len(teamList)-1)
		first_day.append([teamList[0],teamList[away]])
		teamList.pop(away)
		teamList.pop(0)
	return first_day
	
def generate_schedule(teams, first_day):
	schedule = []
	for i in range(len(teams)-1):
		for j in range(i+1,len(teams)):
			schedule.append([teams[i],teams[j]])
	for i in first_day:
		schedule.remove(i)
	shuffle(schedule)
	return schedule
		
def winner(a, b):
	total = a+b+1
	outcome = randint(1,total)
	if outcome <= a:
		return a
	elif outcome <= a+b:
		return b
	else:
		return 0
	
def get_next_game(team, schedule):
	sched = schedule.copy()
	for i in sched:
		if i[0] == team or i[1] == team:
			schedule.remove(i)
			return i
	
def sort_points():
	points.sort(key=lambda x: (-x[1], -x[0]) )
	
def allocate_points(a,b):
	games_played[a-1] += 1
	games_played[b-1] += 1
	aIndex = 999
	bIndex = 999
	for i in points:
		if i[0] == a:
			aIndex = points.index(i)
		if i[0] == b:
			bIndex = points.index(i)
	win = winner(a,b)
	if win == 0:
		points[aIndex][1] += 1
		points[bIndex][1] += 1
	else:
		if win == a:
			points[aIndex][1] += 2
		else:
			points[bIndex][1] += 2
			
def get_possible_points():
	pointsGained = 0
	for i in teams:
		for j in points:
			if j[0] == i:
				pointsGained = j[1]
		gamesLeft = 15 - games_played[i-1]
		possible_points[i-1] = pointsGained + gamesLeft*2
		
def winner_found():
	top_points = points[0][1]
	won = True
	for i in range(len(possible_points)):
		if i != points[0][0]-1 and possible_points[i] >= top_points:
			won = False
	return won
	
def tie_found():
	top_points = points[0][1]
	next_points = points[1][1]
	if top_points != next_points:
		return False
	won = True
	for i in range(len(possible_points)):
		if i != points[0][0]-1 and i != points[1][0]-1 and possible_points[i] >= top_points:
			won = False
	return won
				
def get_next_player():
	pointsLeft = possible_points.copy()
	pointsLeft.reverse()
	player = len(pointsLeft) - pointsLeft.index(max(pointsLeft))
	while games_played[player-1] == 15:
		pointsLeft[pointsLeft.index(max(pointsLeft))] = 0
		player = len(pointsLeft) - pointsLeft.index(max(pointsLeft))
	return player
	
eachTotal = []
winFound = 0
tieFound = 0
	
for index in range(1000):
	totalGames = 0
	teams = generate_teams()
	games_played = [0] * len(teams)
	possible_points = [30] * len(teams)
	points = generate_points(teams)
	first_day = generate_first_day(teams)
	schedule = generate_schedule(teams, first_day)

	for i in first_day:
		allocate_points(i[0],i[1])
	totalGames += 8
	sort_points()

	while not winner_found() and not tie_found() and totalGames < 120:
		nextGame = get_next_game(get_next_player(), schedule)
		allocate_points(nextGame[0],nextGame[1])
		get_possible_points()
		totalGames += 1
		sort_points()
		if (winner_found()):
			winFound +=1
		if (tie_found()):
			tieFound += 1
	eachTotal.append(totalGames)
	
eachTotal.sort()
print("Median number of games: " + str(eachTotal[500]))