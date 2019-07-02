import math
import random
import queue


class Game:
	def __init__(self, cnt, color):
		self.N = len(color)
		self.cnt = cnt
		self.color = color
		self.remainingSwaps = sum(map(sum, cnt)) // 2
		self.cache = set()
		self.clear()

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
		print('------------------------------current dots arrangement----------------')
		for i in range(self.N):
			for j in range(self.N):
				print(self.cnt[i][j], end = ' ')
			print()
		print()
		print('------------------------------current color arrangement----------------')
		for i in range(self.N):
			for j in range(self.N):
				print(self.color[i][j], end = ' ')
			print()
		print()



	def swapable(self, ai, aj, bi, bj):
		# If cnt has been exhausted, then color must match
		return self.cnt[ai][aj] > 0 and self.cnt[bi][bj] > 0 \
			   and  (not self.cnt[ai][aj] == 1 or self.color[ai][aj] == bi) \
			   and  (not self.cnt[bi][bj] == 1 or self.color[bi][bj] == ai)

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

	def doSwap(self, s, forward=True):
		ai, aj, bi, bj = s
		assert ai == bi or aj == bj
		self.cnt[ai][aj] += -1 if forward else 1
		self.cnt[bi][bj] += -1 if forward else 1
		self.remainingSwaps += -1 if forward else 1
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

	def swapImmediate(self, s):
		ai, aj, bi, bj = s
		return      self.cnt[ai][aj]==1 and self.color[ai][aj] != ai \
				and self.cnt[bi][bj]==1 and self.color[bi][bj] != bi \
				and self.color[ai][aj] == bi \
				and self.color[bi][bj] == ai

	def swapPriority1(self, s):
		ai, aj, bi, bj = s
		before = self.numUniqueColorsAtColumn(aj) + self.numUniqueColorsAtColumn(bj)
		self.doSwap(s)
		after = self.numUniqueColorsAtColumn(aj) + self.numUniqueColorsAtColumn(bj)
		self.doSwap(s, forward=False)

		if before < after: return 1
		elif before == after: return 0
		else: return -1

	def swapPriority2(self, s):
		ai, aj, bi, bj = s
		priority = 0
		priority -= self.cnt[ai][aj] == 1
		priority -= self.cnt[bi][bj] == 1
		priority -= self.color[ai][aj] == bi
		priority -= self.color[bi][bj] == ai
		priority += self.color[ai][aj] == ai
		priority += self.color[bi][bj] == bj
		return priority


	def feasiblePerfectColumn(self):
		def getNontrivialOrbits(perm):
			vis = [False] * len(perm)
			for i in range(len(perm)):
				orbit = []
				while not vis[i]:
					vis[i] = True
					orbit.append(i)
					i = perm[i]
				if len(orbit) >= 2:
					yield orbit

		for j in range(self.N):
			color = [self.color[i][j] for i in range(self.N)]
			cnt   = [self.cnt[i][j] for i in range(self.N)]
			for orbit in getNontrivialOrbits(color):
				# Return None if not solvable
				if sum(cnt[i] for i in orbit) < (len(orbit)-1)*2: return False
		return True


	def solvePhase2(self):
		def getNontrivialOrbits(perm):
			vis = [False] * len(perm)
			for i in range(len(perm)):
				orbit = []
				while not vis[i]:
					vis[i] = True
					orbit.append(i)
					i = perm[i]
				if len(orbit) >= 2:
					yield orbit

		ans = []
		for j in range(self.N):
			color = [self.color[i][j] for i in range(self.N)]
			cnt   = [self.cnt[i][j] for i in range(self.N)]

			for orbit in getNontrivialOrbits(color):
				# Return None if not solvable
				if sum(cnt[i] for i in orbit) < (len(orbit)-1)*2: return None
				for i in orbit:
					assert cnt[i] >= 1

				while len(orbit) >= 2:
					for i in orbit:
						if cnt[i]==1 and cnt[color[i]]>=2:
							break
					ii = color[i]

					del orbit[orbit.index(ii)]
					cnt[i], cnt[ii] = cnt[ii]-1, cnt[i]-1
					color[i], color[ii] = color[ii], color[i]

					ans.append((i, j, ii, j))
		return ans


	def solvePhase3(self):
		# Return None if not solvable
		for row in self.cnt:
			if sum(row) % 2 == 1: return None
			if sum(row) - max(row) < max(row): return None

		ans = []
		for i, row in enumerate(self.cnt):
			pq = queue.PriorityQueue()
			for j, c in enumerate(row):
				pq.put((-c,j))
			for _ in range(sum(row)//2):
				ac, aj = pq.get()
				bc, bj = pq.get()
				ans.append((i, aj, i, bj))
				pq.put((ac+1, bj))
				pq.put((bc+1, aj))
		return ans



	# Return None if solution not found
	# Return a list of moves if a solution is found
	def search(self, randomSwaps):
		if hash(self) in self.cache: return None
		self.cache.add(hash(self))
		if self.remainingSwaps == 0: return []

		verticalMoves = self.getVerticalMoves()
		horizontalMoves = self.getHorizontalMoves()
		immediateMoves = list(filter(self.swapImmediate, verticalMoves))

		random.shuffle(verticalMoves)
		random.shuffle(horizontalMoves)

		if immediateMoves:
			moves = immediateMoves[0:1]
		elif randomSwaps >= 1:
			self.miss += 1
			randomSwaps -= 1
			if randomSwaps%4 == 0:
				moves = horizontalMoves
			else:
				moves = verticalMoves

		elif self.numPerfectColumns() < self.N:
			self.bad += 1

			moves = []
			# for j in range(self.N):
			# 	if self.numUniqueColorsAtColumn(j) == self.N:
			# 		for s in verticalMoves:
			# 			if s[1] == j:
			# 				moves.append(s)
			# moves = moves[:2]

			if len(moves) == 0:
				p1 = list(filter(lambda s: self.swapPriority1(s) >= 1, horizontalMoves))
				moves = p1
			if len(moves) == 0 and randomSwaps >= -1:
				randomSwaps -= 1
				for s in verticalMoves:
					self.doSwap(s)
					mm = list(filter(lambda s: self.swapPriority1(s)>=1, self.getHorizontalMoves()))
					self.doSwap(s, forward=False)
					if mm != []:
						moves.append(s)
			# if len(moves) == 0 and randomSwaps >= -3:
			# 	randomSwaps -= 1
			# 	p0 = list(filter(lambda s: self.swapPriority1(s) >= 0, horizontalMoves))
			# 	moves = p0

			moves = moves[:4]


		# else:
		# 	moves2 = self.solvePhase2()
		# 	if moves2 == None:
		# 		self.good += 1
		# 		return None
		#
		# 	for m in moves2:
		# 		self.doSwap(m)
		# 	#self.debugPrint()
		# 	moves3 = self.solvePhase3()
		# 	for m in reversed(moves2):
		# 		self.doSwap(m, forward=False)
		#
		# 	if moves3 == None:
		# 		self.cool += 1
		# 		return None
		# 	else:
		# 		return moves2 + moves3

		elif self.numPerfectRows() < self.N:
			if not self.feasiblePerfectColumn(): return None
			self.good += 1
			if verticalMoves == []: return
			minj = min([aj for ai, aj, bi, bj in verticalMoves])
			moves = list(filter(lambda s: s[1] == minj, verticalMoves))
			#moves = list(filter(lambda s: self.swapPriority2(s) >= 0, moves))
		else:
			#self.debugPrint()
			self.cool += 1
			return self.solvePhase3()

		for s in moves:
			self.doSwap(s)
			sol = self.search(randomSwaps)
			if sol != None: return [s] + sol
			self.doSwap(s, forward=False)



	def solve(self):
		for n in range(100):
			self.clear()
			sol = self.search(randomSwaps = n)
			print(n, 'cachesize', len(self.cache))
			print(n, 'phasecount', self.miss, self.bad, self.good, self.cool)
			if sol: return sol
