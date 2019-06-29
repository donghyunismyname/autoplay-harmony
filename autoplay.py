import algo
import interact
import time

TIMEOUT = 1e18

def main():
	logfile = open('log.txt', 'a')
	input("Hi! We're going to autoplay Har-mo-ny")

	while True:
		N, cnt, color = interact.readPuzzle()

		start = time.time()
		sol = algo.Game(cnt, color).solve()
		timeElapsed = time.time() - start
		assert sol

		print(timeElapsed)
		#logfile.write('timeElapsed %f \n' % timeElapsed)
		#logfile.flush()

		if timeElapsed > TIMEOUT:
			print('Too Much Time Taken')
			exit(0)

		interact.performMoves(N, sol)
		interact.gotoNextStage()


if __name__ == "__main__":
	main()
else:
	print('This module has been imported, which should not be')
	assert False
