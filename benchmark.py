import algo
import time
import json

DIR = 'stage/'
easy = [104, 105, 275, 277, 280, 281, 282, 283, 284, 285, 383, 375, 370, 360, 310, 305, 276, 286, 297]
hard = [381, 385, 405, 415, 425, 455, 551, 556, 578]

filenames = map(str, easy + hard)

for filename in filenames:
	with open(DIR+filename, 'r') as f:
		stage = json.load(f)
		assert len(stage['dots']) == len(stage['color'])

	startTime = time.time()
	sol = algo.Game(stage['dots'], stage['color']).solve()
	elapsedTime = time.time() - startTime

	assert sol
	print('\t\t\t\t', filename, '\t', elapsedTime)
