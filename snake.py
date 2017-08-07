import badge
import ugfx
from random import randint
import time
import sys



class Food:

    def __init__(self,x,y):
        self.pos_x = x
        self.pos_y = y


class Renderer:

    def render_square(self,pointx,pointy):
        ugfx.fill_polygon(pointx, pointy, [[10,5],[10,10],[5,10],[5,5]], ugfx.BLACK)

    def clear_square(self,pointx,pointy):
        ugfx.fill_polygon(pointx, pointy, [[10,5],[10,10],[5,10],[5,5]], ugfx.WHITE)


class Game:

    def __init__(self, started,border,renderer):
        self.started = started
        self.pointx = 10
        self.pointy = 10
        self.direction = "RIGHT"
        self.steps = 0
        self.speed = 5000
        self.length = 5
        self.snake_body = []
        self.can_hit_target = True
        self.score = 0
        self.border = border
        self.game_state = "INIT"
        self.renderer = renderer
        self.set_random_food()

    def should_render(self):
        return self.steps % self.speed == 0 
    def increment(self):
        self.steps +=1 
    

    def hits_food(self,food):

        abspointx = abs(self.pointx)
        abspointy = abs(self.pointy)

        absfoodx = abs(food.pos_x)
        absfoody = abs(food.pos_y) 

        abs_x_diff = abs(abspointx - absfoodx)
        abs_y_diff = abs(abspointy - absfoody)

        return abs_x_diff < 5 and abs_y_diff < 5

    def set_random_food(self):
        x,y = randint(10,270),randint(10,110) # not in extreme corners
        food = Food(x,y)
        self.targetx = food.pos_x
        self.targety = food.pos_y
        self.food = food
        self.renderer.render_square(x,y)

   
    def increase_speed(self):
        if(self.speed <= 200):
            self.speed = 200
        else:
            self.speed -= 200

   
    def render_snake(self):
        # checkif the move buffer is above the length of the snake
        if(len(self.snake_body) > self.length):
            difference = len(self.snake_body) - self.length
            render_targets_to_remove = self.snake_body[:difference]
            # render the tail as white and remove from snake pos list
            for i,j in render_targets_to_remove:
                self.renderer.clear_square(i,j)
                self.snake_body.pop(0)
        self.snake_body.append([self.pointx,self.pointy])
        self.renderer.render_square(self.pointx,self.pointy) 

    def hits_border(self):
        foul_left = self.pointx <= 0
        foul_right = self.pointx >= self.border[1]
        foul_top = self.pointy <= 0
        foul_bottom = self.pointy >= self.border[0] 

        return foul_left or foul_right or foul_top or foul_bottom

    def hits_self(self):
        # checks whether the next step would hit the existing area
        for x,y in self.snake_body:
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
        if(self.hits_food(self.food) and self.can_hit_target == True):
            self.length +=2
            self.increase_speed()
            self.renderer.clear_square(self.targetx,self.targety)
            self.set_random_food()
            self.can_hit_target = False
            self.score += 1
            print("Target Hit!!!!")
        if(self.hits_food(self.food) == True and self.can_hit_target == False):
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

def exit_game(pressed,this_game):
    if(pressed == True):
        sys.exit(0)


def FailGame(this_game):
    ugfx.clear(ugfx.WHITE)
    ugfx.string(20,50,"Game Over - Score: {}".format(this_game.score),"PermanentMarker22",ugfx.BLACK)
    ugfx.flush()
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
        ugfx.flush()



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
    ugfx.input_attach(ugfx.BTN_SELECT, lambda pressed: exit_game(pressed,this_game))

    ugfx.string(50,50,"Snake Game","PermanentMarker22",ugfx.BLACK)
    ugfx.string(50,72,"press SELECT to exit","Roboto_Regular18",ugfx.BLACK)
    ugfx.flush()
    time.sleep(5)
    ugfx.clear(ugfx.WHITE)
    ugfx.flush()


    this_game = Game(True,[128,294],Renderer()) 

    ugfx.box(5, 5, 287, 120, ugfx.BLACK)

    ugfx.flush()

    print("Start Log")

    while True:
        if(this_game.game_state == "FAIL"):
            FailGame(this_game)
        Step(this_game,5)

run_game()

# how to make this run with multiple snakes???? 


# move position of target out of the snake and represent with a diff class
# each round consider the renders, plus look at the buffers to see whether one snake kills another
# how can this be done over a network??? tcp socket??