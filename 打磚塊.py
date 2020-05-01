from tkinter import *
from random import *
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s : %(message)s')


class Ball:
    def __init__(self, canvas, color, winW, winH, racket, bricks):
        logging.debug('初始化ball')
        self.canvas = canvas
        self.racket = racket
        self.bricks = bricks
        self.bricksPosDict = [
            {pos: canvas.coords(pos) for pos in self.bricks.r_list}]
        self.ball_id = canvas.create_oval(0, 0, 10, 10, fill=color)
        self.canvas.move(self.ball_id, winW/2, winH/2)
        startPos = [-4, -3, -2, -1, 1, 2, 3, 4]
        shuffle(startPos)
        self.x = startPos[0]
        self.y = -step
        self.notTouchBottom = True

    def hitRacket(self, ballPos):
        racketPos = self.canvas.coords(self.racket.racket_id)
        if ballPos[2] >= racketPos[0] and ballPos[0] <= racketPos[2]:
            if ballPos[3] >= racketPos[1] and ballPos[3] <= racketPos[3]:
                return True
        return False

    def ballMove(self):
        self.canvas.move(self.ball_id, self.x, self.y)
        self.ballPos = self.canvas.coords(self.ball_id)

        if self.ballPos[0] <= 0:
            self.x = step
        if self.ballPos[1] <= 0:
            self.y = step
        if self.ballPos[2] >= winW:
            self.x = -step
        if self.ballPos[3] >= winH:
            self.y = -step
        if self.hitRacket(self.ballPos) == True:
            self.y = -step
        if self.ballPos[3] >= winH:
            self.notTouchBottom = False

    def hitBricks(self, ballPos):
        for row in self.bricksPosDict:
            for bricksPos in row.items():
                if ballPos[1] <= bricksPos[1][3] and ballPos[1] >= bricksPos[1][1]:
                    if ballPos[2] >= bricksPos[1][0] and ballPos[0] <= bricksPos[1][2]:
                        self.y = step
                        self.bricks.delBricks(bricksPos[0])
                        del self.bricksPosDict[0][bricksPos[0]]
                        #logging.debug('接觸1 球上磚塊下')
                        break
                if ballPos[3] >= bricksPos[1][1] and ballPos[3] <= bricksPos[1][3]:
                    if ballPos[2] >= bricksPos[1][0] and ballPos[0] <= bricksPos[1][2]:
                        self.y = -step
                        self.bricks.delBricks(bricksPos[0])
                        del self.bricksPosDict[0][bricksPos[0]]
                        #logging.debug('接觸2 球下磚塊上')
                        break
            
class Racket:
    def __init__(self, canvas, color):
        logging.debug('初始化Racket')
        self.canvas = canvas
        self.racket_id = canvas.create_rectangle(0, 0, 100, 15, fill=color)
        self.canvas.move(self.racket_id, 270, 400)
        self.x = 0
        self.canvas.bind_all('<KeyPress-Right>', self.moveRight)
        self.canvas.bind_all('<KeyPress-Left>', self.moveLeft)

    def racketMove(self):
        self.canvas.move(self.racket_id, self.x, 0)
        racketPos = self.canvas.coords(self.racket_id)
        if racketPos[0] <= 0:
            self.x = 0
        elif racketPos[2] >= winW:
            self.x = 0

    def moveLeft(self, event):
        self.x = -3

    def moveRight(self, event):
        self.x = 3


class Bricks:
    def __init__(self, canvas):
        logging.debug('初始化Bricks')
        self.canvas = canvas
        self.createBricks()

    def createBricks(self):
        self.r_list = []
        x = 50
        y = 20
        for i in range(1, 6):
            if i != 1:
                y += 20
                x = 50
            for j in range(1, 17):
                self.bricks_id = canvas.create_rectangle(
                    20, 20, 40, 30, fill='blue')
                canvas.move(self.bricks_id, x, y)
                x += 30
                self.r_list.append(self.bricks_id)

    def delBricks(self, bricksPos):
        self.canvas.delete(bricksPos)


winW = 640
winH = 480
step = 2
speed = 0.01

tk = Tk()
tk.title('Bouncing Ball')
tk.wm_attributes('-topmost', 1)
canvas = Canvas(tk, width=winW, height=winH)
canvas.pack()
tk.update()

bricks = Bricks(canvas)
racket = Racket(canvas, 'purple')
ball = Ball(canvas, 'yellow', winW, winH, racket, bricks)

while ball.notTouchBottom:
    try:
        ball.ballMove()
        ball.hitBricks(ball.ballPos)
    except Exception as e:
        print(e)
        print("按關閉紐終止")
        break

    racket.racketMove()
    tk.update()
    time.sleep(speed)

tk.mainloop()
