import badge
import ugfx
from random import randrange
import time
import sys


class Food:

    def __init__(self,x,y):
        self.pos_x = x
        self.pos_y = y

    def create_random_food(snake):
        x,y = randrange(10,270,5),randrange(10,110,5) # not in extreme corners
        if(Food.hits_snake(snake,x,y)):
            create_random_food(snake)
        food = Food(x,y)
        ugfx.fill_polygon(x, y, [[10,5],[10,10],[5,10],[5,5]], ugfx.BLACK)
        return food

    def hits_snake(snake,x,y):
        for i,j in snake.snake_body:
            if(x == i and y == j):
                return True
        return False

class Border:

    def __init__(self,min_x=0,min_y=0,max_x=294,max_y=128):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y 
        self.draw_border()

    def draw_border(self):
        ugfx.box(5, 5, 287, 120, ugfx.BLACK)

class Game:

    def __init__(self,snake,border,food):
        self.snake = snake
        self.border = border
        self.steps = 0
        self.food = food
        self.game_state = "INIT"

    def increment(self):
        self.steps +=1
    
    def do_game(self):
        
        if(self.snake.hits_self() or self.snake.hits_border(self.border)):
            self.game_state = "FAIL"
            return
        if(self.snake.can_hit_target == True):
            for i in self.food:
                if(self.snake.hits_food(i)):
                    self.snake.length +=2
                    self.snake.increase_speed()
                    self.snake.renderer.clear_square(i.pos_x,i.pos_y)
                    self.food.remove(i)
                    self.food.append(Food.create_random_food(self.snake))
                    self.snake.can_hit_target = False
                    self.snake.score += 1
                    print("Target Hit!!!!")
            
        if(self.snake.hits_any_food(self.food) == True and self.snake.can_hit_target == False):
            self.snake.render_snake()
        else:
            self.snake.can_hit_target = True
            self.snake.render_snake()
    
    def run_step(self,step_size):
        self.increment()
        if(self.snake.started == True and self.snake.should_render(self.steps)):
            self.snake.move(step_size)
            self.do_game()
            ugfx.flush()


class Renderer:

    def render_square(self,pointx,pointy):
        ugfx.fill_polygon(pointx, pointy, [[10,5],[10,10],[5,10],[5,5]], ugfx.BLACK)

    def clear_square(self,pointx,pointy):
        ugfx.fill_polygon(pointx, pointy, [[10,5],[10,10],[5,10],[5,5]], ugfx.WHITE)


class Snake:

    def __init__(self, started,renderer):
        self.started = started
        self.pointx = 10
        self.pointy = 10
        self.direction = "RIGHT"
        self.speed = 1000
        self.length = 5
        self.snake_body = []
        self.can_hit_target = True
        self.score = 0
        self.renderer = renderer

    def should_render(self,steps):
        return steps % self.speed == 0 


    def hits_food(self,food):

        abspointx = abs(self.pointx)
        abspointy = abs(self.pointy)

        absfoodx = abs(food.pos_x)
        absfoody = abs(food.pos_y) 

        abs_x_diff = abs(abspointx - absfoodx)
        abs_y_diff = abs(abspointy - absfoody)

        return abs_x_diff < 5 and abs_y_diff < 5

    def hits_any_food(self,food_iter):
        for i in food_iter:
            if(self.hits_food(i)):
                return True
        return False
    def move(self,move_size):
        if(self.direction == "LEFT"):
            self.pointx -= move_size
        if(self.direction == "RIGHT"):
            self.pointx += move_size
        if(self.direction == "UP"):
            self.pointy -= move_size
        if(self.direction == "DOWN"):
            self.pointy += move_size        
   
    def increase_speed(self):
        if(self.speed <= 10):
            self.speed = 10
        else:
            self.speed -= 10

   
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

    def hits_border(self,border):
        foul_left = self.pointx <= border.min_x
        foul_right = self.pointx >= border.max_x
        foul_top = self.pointy <= border.min_y
        foul_bottom = self.pointy >= border.max_y 

        hits =  foul_left or foul_right or foul_top or foul_bottom
        # print(hits)
        return hits

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
    


def up(pressed,this_game):
    if(pressed == True):
        this_game.snake.direction = "UP"

def down(pressed,this_game):
    if(pressed == True):
        this_game.snake.direction = "DOWN"

def left(pressed, this_game):
    if(pressed == True):
        this_game.snake.direction = "LEFT"

def right(pressed,this_game):
    if(pressed == True):
        this_game.snake.direction = "RIGHT"

def exit_game(pressed,this_game):
    if(pressed == True):
        sys.exit(0)


def FailGame(this_game):
    ugfx.clear(ugfx.WHITE)
    ugfx.string(20,50,"Game Over - Score: {}".format(this_game.snake.score),"PermanentMarker22",ugfx.BLACK)
    ugfx.flush()
    time.sleep(5)
    sys.exit(0)

def Step(this_game,step_size):
    this_game.run_step(step_size)

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

    snake = Snake(True,Renderer())
    this_game = Game(snake,Border(),[Food.create_random_food(snake)]) 

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