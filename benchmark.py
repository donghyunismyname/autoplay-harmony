import algo
import time

dir = 'stage/'
hard = [385, 405, 415, 425, 455]
medium = [381]
easy = [104, 105, 275, 277, 280, 281, 282, 283, 284, 285, 383, 375, 370, 360, 310, 305, 276, 286, 297]

hard = map(str, hard)
medium = map(str, medium)
easy = map(str, easy)

files = hard
for filename in files:
	puzzleStr = open(dir + filename, 'r').read()
	puzzleInfo = list(map(int, puzzleStr.split()))
	N = puzzleInfo[0]
	cnt = [[puzzleInfo[1+i*N+j] for j in range(N)] for i in range(N)]
	color = [[puzzleInfo[N*N+1+i*N+j] for j in range(N)] for i in range(N)]



	startTime = time.time()
	sol = algo.Game(N, cnt, color).solve()
	elapsedTime = time.time() - startTime

	assert sol
	print('\t\t\t\t', filename, '\t', elapsedTime)
