import interact
import json

DIR = 'stage/'

def main():
	while True:
		print('Save current stage into ' + DIR + ' with filename: ', end = '')
		filename = input()
		if filename == '':
			print('[ERROR] Please enter a filename')
			continue

		N, cnt, color = interact.readPuzzle()
		stage = {'dots':cnt, 'color':color}
		with open(DIR+filename, 'w') as f:
			json.dump(stage, f)


if __name__ == "__main__":
	main()
else:
	assert False, 'This moduls is not intended to be imported'
