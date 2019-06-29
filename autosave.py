import interact


def main():
	while True:
		print('Save this stage with filename: ', end = '')
		filename = input()
		if filename == '':
			print('[ERROR] Please enter a filename')
			continue

		N, cnt, color = interact.readPuzzle()
		f = open('stage/' + filename, 'w')

		f.write(str(N) + '\n\n')
		for i in range(N):
			for j in range(N):
				f.write(str(cnt[i][j]) + ' ')
			f.write('\n')
		f.write('\n')
		for i in range(N):
			for j in range(N):
				f.write(str(color[i][j]) + ' ')
			f.write('\n')
		f.write('\n')

		f.flush()
		f.close()


if __name__ == "__main__":
	main()
else:
	print('This module has been imported, which should not be')
	assert False