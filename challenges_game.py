from tkinter import *
import random
import time

tk = Tk()
canvas = Canvas(tk, width=500, height=500)
canvas.pack()

class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False
    
    speed = 1

    def draw(self):
        self.canvas.move(self.id, self.x, self.y * self.speed)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3
        if self.hit_paddle(pos):
            self.y = -3
            self.speed += 0.5

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind('<KeyPress-Left>', self.turn_left)
        self.canvas.bind('<KeyPress-Right>', self.turn_right)
        self.canvas.bind('<KeyRelease-Left>', self.stop)
        self.canvas.bind('<KeyRelease-Right>', self.stop)
        self.canvas.focus_set()

    def turn_left(self, evt):
        self.x = -2

    def turn_right(self, evt):
        self.x = 2

    def stop(self, evt):
        self.x = 0

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

class Scoreboard:
    def __init__(self, canvas):
        self.canvas = canvas
        self.score_id = None
        self.scoreboard_id = None
        self.current_score = 0
    
    def delete(self):
        if self.scoreboard_id:
            self.canvas.delete(self.scoreboard_id)
        
        if self.score_id:
            self.canvas.delete(self.score_id)
    
    def draw(self):
        # Draw the rectangle for the scoreboard.
        if not self.scoreboard_id:
            self.scoreboard_id = canvas.create_rectangle(400, 10, 499, 100, outline="")

        # Draw the numbers on the score board.
        if self.score_id:
            self.canvas.delete(self.score_id)

        self.score_id = canvas.create_text(450, 450, text='%s' % (self.current_score), font=('Times', 12))

def countdown(number):
    current_number = number
    for x in range(1, number + 1):
        print('%s!' % (current_number))
        id = canvas.create_text(250, 250, text='%s' % (current_number),
        font=('Times', 22))
        tk.update()
        time.sleep(1)
        canvas.delete(id)
        tk.update()
        current_number = current_number - 1
    if current_number == 0:
        print('GO!!!')
        id = canvas.create_text(250, 250, text='GO!!!',
        font=('Times', 22))
        tk.update()
        time.sleep(1)
        canvas.delete(id)
        tk.update()

def game_over():
    print('Oh no! You lost!')
    time.sleep(1)
    canvas.create_text(250, 250, text='Game Over!!!',
    font=('Times', 22))



# Game Loop
tk.title("Game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
tk.update()

countdown(5)

paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle, 'red')
scoreboard = Scoreboard(canvas)

while ball.hit_bottom == False:
    if scoreboard.current_score > 0:
        scoreboard.draw()

    pos = ball.canvas.coords(ball.id)
    
    if ball.hit_paddle(pos):
        scoreboard.current_score += 1
        ball.y = -3
    
    ball.draw()
    paddle.draw()
    tk.update_idletasks()
    tk.update()


if ball.hit_bottom == True:
    game_over()
    

tk.mainloop()