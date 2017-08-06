import badge
import ugfx
from random import randint
import time
import sys


class Game:

    def __init__(self, started,border):
        self.started = started
        self.pointx = 10
        self.pointy = 10
        self.direction = "RIGHT"
        self.steps = 0
        self.speed = 20000
        self.length = 25
        self.render_targets = []
        self.can_hit_target = True
        self.score = 0
        self.set_random_target()
        self.border = border
        self.game_state = "INIT"

    def should_render(self):
        return self.steps % self.speed == 0 
    def increment(self):
        self.steps +=1 
    
    def hits_target(self):
        
        abspointx = abs(self.pointx)
        abstargetx = abs(self.targetx)
        abspointy = abs(self.pointy)
        abstargety = abs(self.targety)
        absxdiff =  abs(abspointx - abstargetx)
        absydiff = abs(abspointy - abstargety)
        return absxdiff < 5 and absydiff < 5

    def create_target(self,targetx,targety):
        self.render_square(targetx,targety)
        return targetx,targety

    def set_random_target(self):
        x,y = randint(0,275),randint(0,110)
        self.targetx = x
        self.targety = y
        self.render_square(x,y)

    def render_square(self,pointx,pointy):
        ugfx.fill_polygon(pointx, pointy, [[10,5],[10,10],[5,10],[5,5]], ugfx.BLACK)


    def clear_square(self,pointx,pointy):
        ugfx.fill_polygon(pointx, pointy, [[10,5],[10,10],[5,10],[5,5]], ugfx.WHITE)


    def render_snake(self):
        # checkif the move buffer is above the length of the snake
        if(len(self.render_targets) > self.length):
            difference = len(self.render_targets) - self.length
            render_targets_to_remove = self.render_targets[:difference]
            # render the tail as white and remove from snake pos list
            for i,j in render_targets_to_remove:
                self.clear_square(i,j)
                self.render_targets.pop(0)
        self.render_targets.append([self.pointx,self.pointy])
        self.render_square(self.pointx,self.pointy) 

    def hits_border(self):
        foul_left = self.pointx <= 0
        foul_right = self.pointx >= self.border[1]
        foul_top = self.pointy <= 0
        foul_bottom = self.pointy >= self.border[0] 

        return foul_left or foul_right or foul_top or foul_bottom

    def hits_self(self):
        # checks whether the next step would hit the existing area
        for x,y in self.render_targets:
            abspointx = abs(self.pointx)
            abstargetx = abs(x)
            abspointy = abs(self.pointy)
            abstargety = abs(y)
            absxdiff =  abs(abspointx - abstargetx)
            absydiff = abs(abspointy - abstargety)
            hits = (absxdiff == 0) and (absydiff == 0)
            if(hits == True):
                return True
        return False


    def do_game(self):
        
        if(self.hits_self() or self.hits_border()):
            self.game_state = "FAIL"
            return
        if(self.hits_target() and self.can_hit_target == True):
            self.length +=10
            self.speed -= 500
            self.clear_square(self.targetx,self.targety)
            self.set_random_target()
            self.can_hit_target = False
            self.score += 1
            print("Target Hit!!!!")
        if(self.hits_target() == True and self.can_hit_target == False):
            self.render_snake()
        else:
            self.can_hit_target = True
            self.render_snake()


def up(pressed,this_game):
    if(pressed == True):
        this_game.direction = "UP"

def down(pressed,this_game):
    if(pressed == True):
        this_game.direction = "DOWN"

def left(pressed, this_game):
    if(pressed == True):
        this_game.direction = "LEFT"

def right(pressed,this_game):
    if(pressed == True):
        this_game.direction = "RIGHT"

def FailGame(this_game):
    ugfx.clear(ugfx.WHITE)
    ugfx.string(20,50,"Game Over - Score: {}".format(this_game.score),"PermanentMarker22",ugfx.BLACK)
    time.sleep(5)
    sys.exit(0)

def Step(this_game,step_size):
    this_game.increment()
    if(this_game.started == True and this_game.should_render()):
        if(this_game.direction == "LEFT"):
            this_game.pointx = this_game.pointx -step_size
        if(this_game.direction == "RIGHT"):
            this_game.pointx = this_game.pointx +step_size
        if(this_game.direction == "UP"):
            this_game.pointy = this_game.pointy -step_size
        if(this_game.direction == "DOWN"):
            this_game.pointy = this_game.pointy +step_size
        this_game.do_game()



def run_game():

    badge.eink_init()
    ugfx.init()
    ugfx.clear(ugfx.WHITE)
    ugfx.flush()

    badge.init()

    ugfx.clear(ugfx.WHITE)

    ugfx.input_init()

    ugfx.input_attach(ugfx.JOY_UP, lambda pressed: up(pressed,this_game))
    ugfx.input_attach(ugfx.JOY_DOWN, lambda pressed: down(pressed,this_game))
    ugfx.input_attach(ugfx.JOY_LEFT, lambda pressed: left(pressed,this_game))
    ugfx.input_attach(ugfx.JOY_RIGHT, lambda pressed: right(pressed,this_game))
    # ugfx.input_attach(ugfx.BTN_A, lambda pressed: start(pressed,this_game))

    ugfx.string(50,50,"Snake Game","PermanentMarker22",ugfx.BLACK)
    time.sleep(5)
    ugfx.clear(ugfx.WHITE)

    this_game = Game(True,[128,294]) 

    ugfx.box(5, 5, 287, 120, ugfx.BLACK)

    print("Start Log")




    while True:
        if(this_game.game_state == "FAIL"):
            FailGame(this_game)
        Step(this_game,2)

run_game()