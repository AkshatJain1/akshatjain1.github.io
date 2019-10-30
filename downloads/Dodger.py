'''
    Done:   bad guys at diff sizes are falling down at diff speed
            player moves left and right
            score increases when badGuy passes bottom of screen
            scores decreases by 20 when player hits a badGuy

    NeedToDo:   powerups
                    reverse bad guys
                    slowdown bad guys
                    invulnerability

                shooter maybe?

                images?
'''

from tkinter import *
from tkinter.font import Font
import tkinter.messagebox
import time
import random



directions = 'Welcome to Dodger! Try to avoid all the green bad guys that are coming down at you. ' \
             'Hitting them will take off 10 points. Each green guy that goes off the screen grants you ' \
             'a point!. Collect powerups to increase your chances of not getting hit. Purple is a reverse' \
             ',pink is a slow down,turquoise is 50 points, and light green is 5 second invulnerability.\n\n Now, do you dare?\n' \


tkinter.messagebox.showinfo('Directions',directions)



WIDTH = 900
HEIGHT = 700


tk = Tk()
canvas = Canvas(tk,width = WIDTH, height = HEIGHT, bg = "black")
tk.title('Dodger')



canvas.pack()




class GoodGuy:
    def __init__(self):
        self.xpos = WIDTH/2 -25
        self.ypos = HEIGHT-80

        self.invul = False
        self.invulTime = 0

        self.shape = canvas.create_rectangle(self.xpos,self.ypos,self.xpos+30,self.ypos+20,fill ='Blue')
        tk.bind('<Left>', self.left)
        tk.bind('<Right>', self.right)

    def left(self, event):
        canvas.move(self.shape,-10,0)
    def right(self, event):
        canvas.move(self.shape, 10, 0)
    def get_xpos(self):
        return self.xpos
    def get_ypos(self):
        return self.ypos
    def get_shape(self):
        return self.shape
    def check(self,bad,power):
        score = 0

        for x in bad:
            t = canvas.find_overlapping(x.get_pos()[0], x.get_pos()[1], x.get_pos()[2], x.get_pos()[3])
            if  self.shape in t and not self.invul:
                print('Collision')
                bad.remove(x)
                canvas.delete(x.get_shape())
                bad.append(BadGuy())
                score-=10

        for p in power:
            t = canvas.find_overlapping(p.get_pos()[0], p.get_pos()[1], p.get_pos()[2], p.get_pos()[3])
            if self.shape in t:
                print('COLLSISION with Power')
                power.remove(p)
                canvas.delete(p.shape)
                if p.power == 'Invul':
                    self.invul = True
                    self.invulTime = time.time()
                    print(self.invulTime)
                elif p.power == 'Slow':
                    for x in bad:
                        x.set_slowDown((x.gravity-x.slowDown)//2)
                elif p.power == 'Reverse':
                    for x in bad:
                        x.set_slowDown(x.gravity * 2)
                else:
                    score+=50




        if self.invulTime is not 0:
            print(time.time() - self.invulTime)

        if time.time() - self.invulTime > 5 and self.invulTime != 0:
            self.invul = False
            self.invulTime = 0


        return score





class BadGuy:
    def __init__(self):
        self.xpos = random.randrange(0,WIDTH)
        self.ypos = 0
        self.size = random.randrange(5,30)

        self.slowDown = 0
        self.shape = canvas.create_rectangle(self.xpos, self.ypos, self.xpos+self.size, self.ypos+self.size, fill = 'green')


        self.gravity = (random.uniform(2.0,7.0))
    def move(self,badguyList):
        canvas.move(self.shape,0,self.gravity-self.slowDown)

        pos = self.get_pos()

        if pos[1]>=HEIGHT or pos[3]<=0:
            badguyList.remove(self)
            canvas.delete(self.shape)
            badguyList.append(BadGuy())
            return 1
        return 0
    def set_slowDown(self,s):
        self.slowDown = s
    def get_pos(self):
        return canvas.coords(self.shape)
    def get_shape(self):
        return self.shape
    def get_xpos(self):
        return self.xpos
    def get_ypos(self):
        return self.ypos
    def get_size(self):
        return self.size

class PowerUp :
    def __init__(self):
        self.xpos = random.randrange(0, WIDTH)
        self.ypos = 0
        self.size = 25
        self.effect = False
        powers = ["Invul", "Reverse", "Slow","Score"]
        self.power = random.choice(powers)

        if self.power == "Invul":
            self.shape = canvas.create_rectangle(self.xpos, self.ypos, self.xpos + self.size, self.ypos + self.size, fill='lightgreen')
        elif self.power == 'Reverse':
            self.shape = canvas.create_rectangle(self.xpos, self.ypos, self.xpos + self.size, self.ypos + self.size, fill='purple')
        elif self.power == 'Slow':
            self.shape = canvas.create_rectangle(self.xpos, self.ypos, self.xpos + self.size, self.ypos + self.size, fill='pink')
        else:
            self.shape = canvas.create_rectangle(self.xpos, self.ypos, self.xpos + self.size, self.ypos + self.size,
                                                 fill='turquoise')

        self.gravity = 4



    def move(self,powerupList):
        canvas.move(self.shape,0,self.gravity)

        pos = canvas.coords(self.shape)


        if pos[1]>=HEIGHT:
            powerupList.remove(self)
            canvas.delete(self.shape)

        return 0
    def get_pos(self):
        return canvas.coords(self.shape)

    def set_effect(self,b):
        self.effect = b



badGuyList = []
powerupList = []

for x in range(30):
    badGuyList.append(BadGuy())


gg = GoodGuy()
score =0
id = canvas.create_text(110,30,text = 'Score: ' + str(score),fill = "yellow",font = Font(family="Times New Roman", size=40))


time4powerup = canvas.create_text(WIDTH/2,30,text = '',fill = "Red",font = Font(family="Times New Roman", size=50))


while True:
    for bad in badGuyList:
        score += bad.move(badGuyList)

    if random.randrange(0,100) == 2:
        powerupList.append(PowerUp())

    for power in powerupList:
        score+=power.move(powerupList)


    canvas.delete(time4powerup)
    if gg.invul == False:
        time4powerup = canvas.create_text(WIDTH / 2, 30, text= '', fill="Red",font=Font(family="Times New Roman", size=40))
    else:
        time4powerup = canvas.create_text(WIDTH / 2, 30, text = str(5 - int(time.time() - gg.invulTime)), fill="Red",
                                          font=Font(family="Times New Roman", size=50))





    score += gg.check(badGuyList,powerupList)

    canvas.delete(id)
    id = canvas.create_text(110,30,text = 'Score: ' + str(score),fill = "yellow",font = Font(family="Times New Roman", size=30))

    tk.update()

    time.sleep(.02)


tk.mainloop()

