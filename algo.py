import math
import random


class Game:
	def __init__(self, N, cnt, color):
		self.N = N
		self.cnt = cnt
		self.color = color
		self.remainingSwaps = sum(map(sum, cnt)) // 2
		self.cache = set()

		self.miss = 0
		self.bad = 0
		self.good = 0
		self.cool = 0

	def clear(self):
		self.cache.clear()
		self.miss = 0
		self.bad = 0
		self.good = 0
		self.cool = 0

	def __hash__(self):
		val = 0
		for row in self.color:
			for e in row:
				val = e + val * self.N
		for row in self.cnt:
			for e in row:
				val = e + val * self.N
		return val

	def debugPrint(self):
		print('------------------------------current color arrangement----------------')
		#for i in range(self.N):
		#	for j in range(self.N):
		#		print(self.cnt[i][j], end = ' ')
		#	print()
		#print()
		for i in range(self.N):
			for j in range(self.N):
				print(self.color[i][j], end = ' ')
			print()
		print()



	def swapable(self, ai, aj, bi, bj):
		# If cnt has been exhausted, then color must match
		return self.cnt[ai][aj] > 0 and self.cnt[bi][bj] > 0 \
			   and  not (self.cnt[ai][aj] == 1 and self.color[ai][aj] != bi) \
			   and  not (self.cnt[bi][bj] == 1 and self.color[bi][bj] != ai)

	def getHorizontalMoves(self):
		horizontalMoves = []
		for i in range(self.N):
			for j1 in range(self.N):
				for j2 in range(j1+1, self.N):
					if self.swapable(i, j1, i, j2):
						horizontalMoves.append((i, j1, i, j2))
		return horizontalMoves

	def getVerticalMoves(self):
		verticalMoves = []
		for j in range(self.N):
			for i1 in range(self.N):
				for i2 in range(i1+1, self.N):
					if self.swapable(i1, j, i2, j):
						verticalMoves.append((i1, j, i2, j))
		return verticalMoves

	def doSwap(self, s, reverse = False):
		ai, aj, bi, bj = s
		assert ai == bi or aj == bj
		self.cnt[ai][aj] += 1 if reverse else -1
		self.cnt[bi][bj] += 1 if reverse else -1
		self.remainingSwaps += 1 if reverse else -1
		self.cnt[ai][aj], self.cnt[bi][bj] = self.cnt[bi][bj], self.cnt[ai][aj]
		self.color[ai][aj], self.color[bi][bj] = self.color[bi][bj], self.color[ai][aj]

	def numUniqueColorsAtColumn(self, j):
		return len(set([self.color[i][j] for i in range(self.N)]))
	def numPerfectColumns(self):
		return [self.numUniqueColorsAtColumn(j) for j in range(self.N)].count(self.N)
	def numCorrectColorsAtRow(self, i):
		return self.color[i].count(i)
	def numPerfectRows(self):
		return [self.numCorrectColorsAtRow(i) for i in range(self.N)].count(self.N)

	def swapPriority1(self, s):
		ai, aj, bi, bj = s;
		before = self.numUniqueColorsAtColumn(aj) + self.numUniqueColorsAtColumn(bj)
		self.doSwap(s)
		after = self.numUniqueColorsAtColumn(aj) + self.numUniqueColorsAtColumn(bj)
		self.doSwap(s, reverse = True)

		if before < after: return 1
		elif before == after: return 0
		else: return -1

	def swapPriority2(self, s):
		ai, aj, bi, bj = s;
		priority = 1
		#priority += self.cnt[ai][aj] == 1
		#priority += self.cnt[bi][bj] == 1
		#priority += self.color[ai][aj] == bi
		#priority += self.color[bi][bj] == ai
		priority -= self.color[ai][aj] == ai
		priority -= self.color[bi][bj] == bj
		return priority

	def solvePhase3(self):
		# Check and return None if not solvable
		for row in self.cnt:
			if sum(row) % 2 == 1: return None
			if sum(row) - max(row) < max(row): return None

		ans = []
		for i, row in enumerate(self.cnt):
			blocks = list(enumerate(row))
			for _ in range(sum(row)//2):
				# Pick two blocks with largest cnt
				blocks.sort(key = (lambda p: p[1]), reverse = True)
				a, b = blocks[0], blocks[1]
				blocks[0] = (a[0], b[1] - 1)
				blocks[1] = (b[0], a[1] - 1)
				ans.append((i, a[0], i, b[0]))
		return ans



	# Returns None if unsolvable
	# Returns a list containing the moves if solvable
	def search(self, randomSwaps):
		if hash(self) in self.cache: return None
		self.cache.add(hash(self))
		if self.remainingSwaps == 0: return []

		verticalMoves = self.getVerticalMoves()
		horizontalMoves = self.getHorizontalMoves()

		if randomSwaps:
			self.miss += 1
			randomSwaps -= 1
			#p1 = list(filter(lambda s: self.swapPriority1(s) == 1, horizontalMoves))
			#p0 = list(filter(lambda s: self.swapPriority1(s) == 0, horizontalMoves))
			#vv = list(filter(lambda s: self.numUniqueColorsAtColumn(s[1]) < self.N, verticalMoves))
			moves = horizontalMoves + verticalMoves
		elif self.numPerfectColumns() < self.N:
			self.bad += 1
			p1 = list(filter(lambda s: self.swapPriority1(s) == 1, horizontalMoves))
			moves = p1[0:1]
		elif self.numPerfectRows() < self.N:
			self.good += 1
			if verticalMoves == []: return
			minj = min([aj for ai, aj, bi, bj in verticalMoves])
			moves = list(filter(lambda s: s[1] == minj, verticalMoves))
			#moves = list(filter(lambda s: self.swapPriority2(s) >= 0, moves))
		else:
			self.cool += 1
			return self.solvePhase3()

		for s in moves:
			self.doSwap(s)
			sol = self.search(randomSwaps)
			if sol != None: return [s] + sol
			self.doSwap(s, reverse = True)





	def solve(self):
		self.clear()
		sol = self.search(randomSwaps = 0)
		print('cachesize', len(self.cache))
		print('phasecount', self.miss, self.bad, self.good, self.cool)
		if sol: return sol

		self.clear()
		sol = self.search(randomSwaps = 1)
		print('cachesize', len(self.cache))
		print('phasecount', self.miss, self.bad, self.good, self.cool)
		if sol: return sol

		self.clear()
		sol = self.search(randomSwaps = 2)
		print('cachesize', len(self.cache))
		print('phasecount', self.miss, self.bad, self.good, self.cool)
		if sol: return sol

		self.clear()
		sol = self.search(randomSwaps = 3)
		print('cachesize', len(self.cache))
		print('phasecount', self.miss, self.bad, self.good, self.cool)
		if sol: return sol

		self.clear()
		sol = self.search(randomSwaps = 4)
		print('cachesize', len(self.cache))
		print('phasecount', self.miss, self.bad, self.good, self.cool)
		if sol: return sol
