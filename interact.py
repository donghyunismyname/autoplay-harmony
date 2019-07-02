import pyautogui
import PIL
import time

TIME_EYE = 1.0
TIME_CLICK1 = 0.5
TIME_CLICK2 = 0.5
TIME_LAST_CLICK = 3.0
TIME_NEXT_STAGE = 4.0


X0 = 15
Y0 = 270
LEN = 550


boardArea = (X0, Y0, X0 + LEN, Y0 + LEN)
eyePosition = ((X0 + LEN) / 2, Y0 + LEN * 1.3)
nextStagePosition = (X0 + LEN*0.5, Y0 + LEN*0.57)
neverRatePosition = (X0 + LEN*0.2, Y0 + LEN*0.57)

def main():
	pyautogui.moveTo((X0, Y0))
	time.sleep(0.2)
	pyautogui.moveTo((X0, Y0+LEN))
	time.sleep(0.2)
	pyautogui.moveTo((X0+LEN, Y0))
	time.sleep(0.2)
	pyautogui.moveTo((X0+LEN, Y0+LEN))
	time.sleep(0.2)
	pyautogui.moveTo((X0, Y0))


def readPuzzle():
	# Capture the board
	boardImg = PIL.ImageGrab.grab(boardArea)

	# Capture the correct color arrangement
	pyautogui.moveTo(eyePosition)
	pyautogui.mouseDown()
	time.sleep(TIME_EYE)
	eyeImg = PIL.ImageGrab.grab(boardArea)
	pyautogui.mouseUp()
	time.sleep(TIME_EYE)

	# Find out N where the board is N by N
	N = 1
	yDot = 10
	while yDot < LEN - 10:
		if eyeImg.getpixel((10, yDot-1)) != eyeImg.getpixel((10, yDot)):
			N += 1
			yDot += 10
		yDot += 1

	blockSize = LEN / N

	# Sample the correct color
	colorDic = {}
	for i in range(N):
		xDot = int(blockSize / 4)
		yDot = int(blockSize * i + blockSize / 4)
		p = eyeImg.getpixel((xDot,yDot))
		colorDic[p] = i

	# Find out cnt and color
	cnt = [[0] * N for _ in range(N)]
	color = [[-1] * N for _ in range(N)]
	for i in range(N):
		for j in range(N):
			x0 = int(blockSize * j + blockSize * 0.15)
			y0 = int(blockSize * i + blockSize * 0.15)
			p = boardImg.getpixel((x0, y0))

			color[i][j] = colorDic[p]

			for xDot in range(x0, int(x0 + blockSize *0.7)):
				for yDot in range(y0, int(y0 + blockSize *0.7)):
					if boardImg.getpixel((xDot,yDot)) != p:
						break
				else:
					continue
				break

			for x in range(xDot - 1, int(x0 + blockSize  * 0.7)):
				cnt[i][j] += boardImg.getpixel((x,yDot)) == p and boardImg.getpixel((x+1,yDot)) != p

	print(N)
	print(colorDic)
	print(cnt)
	print(color)
	assert sum(map(sum, cnt)) % 2 == 0
	for i in range(N):
		for j in range(N):
			assert cnt[i][j] >= 1
	return N, cnt, color


def performMoves(N, moves):
    blockSize = int(LEN / N)
    for ai, aj, bi, bj in moves:
        ax = int(X0 + blockSize * aj + blockSize / 2);
        ay = int(Y0 + blockSize * ai + blockSize / 2);
        bx = int(X0 + blockSize * bj + blockSize / 2);
        by = int(Y0 + blockSize * bi + blockSize / 2);

        pyautogui.click(ax, ay)
        time.sleep(TIME_CLICK1)
        pyautogui.click(bx, by)
        time.sleep(TIME_CLICK2)
    time.sleep(TIME_LAST_CLICK)


def gotoNextStage():
	#Handle rate this app popup
    #pyautogui.click(neverRatePosition)
    #time.sleep(1)
    pyautogui.click(nextStagePosition)
    time.sleep(TIME_NEXT_STAGE)


if __name__ == '__main__':
	main()
