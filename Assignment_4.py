'''
+-----------------------------+
|     CPSC 231                |
|     Assignment # 4          |
|     Flappy Turtle           |
|     Spencer A. Manzon       |
|     Student ID: 10129731    |
+-----------------------------+
'''

#XXX MAIN() TODO:
#XXX-DONE: The game should have a title screen. (1 mark)
#XXX-DONE: Pressing q or Q must exit the game. Use the game engine to get the input. (1 mark)
#XXX-DONE: The ``flappy turtle'' must be drawn and fall unless the space bar is pressed, in which case the ``flappy turtle'' flies upwards briefly. Use the game engine for the ``flappy turtle'' and the input. (1 mark)
#XXX-DONE: When the game is over, pressing the space bar should cause the game to restart. Use the game engine to get the input. (1 mark)
#XXX-DONE: Using the game engine, add ``pipes'' that scroll across the bottom of the screen at regular intervals. The pipe's height should be randomly chosen. (1 mark)
#XXX-DONE: Using the game engine, add ``pipes'' that scroll across the top of the screen at regular intervals, each positioned above a bottom pipe, leaving enough of a gap for the ``flappy bird'' to fly through. (1 mark) 
#XXX-DONE:The score should be kept, with one point gained every time the gap between pipes is successfully cleared. Note that the score does not have to be continuously displayed and updated; it may only be shown once the game is over. (1 mark)
#XXX-DONE: End the game if the ``flappy bird'' falls or flaps outside the screen. (1 mark)
#XXX-DONE: End the game if the ``flappy bird'' collides with one of the pipes. (1 mark)

#import stuff
import engine
import random
import math
import turtle
import time

#+-------------------------------------+
#| variables - changes game parameters |
#+-------------------------------------+
#screen properties		#window size
WIDTH = 1100			#minimum recommended: 630 (title text may not be shown if lower than this)
HEIGHT = 600			#minimum recommended: 550 (game over text may not be shown if lower than this)
GAMECOLOR = '#79DEFF'		#the game background color
SCORECOLOR = 'red'		#score number color
ENDCOLOR = 'brown'		#game over screen text color
#title properties		#title text to be displayed
TITLETEXT1 = "FLAPPIN' MUTANT"	#top text on title screen
TITLETEXT2 = 'NINJA TURTLE'	#bottom text on titles screen
#turtle properties		#the look and feel of the turtle
turtle.register_shape('TURTLEREX', (
			(-2,0),(-20,-8),(-30,-2.5),(-32,-10),(-40,-14),(-42,-14),(-36,-7),(-34,2),(-26,4.5),(-24,10),(-20,12),(-22,6),(-12,10),(-10,15),(-6,16),(-8,10),(0,0)
		))		#dino-turtle shape, named TURTLEREX (because it was intended to be a turtle but looked more like a dinosaur)
TURTLESHAPE = 'TURTLEREX'	#the shape of the turtle
TURTLECOLOR = '#0000FF'		#the color of the turtle
INIT_POSX = -WIDTH/4		#starting place of player in the x-axis
INIT_POSY = 100			#starting place of player in the y-axis
BOUND_SIZEX = 42 		#limits of the turtle in the x-axis
BOUND_SIZEY = 15		#limits of the turtle in the y-axis
BLASTRADIUS = 100		#radius of explosion when turtle dies
#pipe properties		#the look, feel, and madness of the pipes
PIPEPACE = 2			#speed of the pipe at a given PIPEINTERVAL. positive number, already corrected for in the classes
PIPECOLOR = '#006600'		#the color of the pipe
PIPEWIDTH = 40			#the width of the pipe
PIPESTART = WIDTH/2		#the starting of the pipe, usually the right edge of the screen
PIPEINTERVAL = 150		#the frequency of the pipes showing up at a given PIPEPACE. higher number = slower. determined by the "game time modulus PIPEINTERVAL == 0"
GAPDISTANCE = 120		#the distance in the y-axis of the two pipes
#top pipe dimensions		#pipe dimensions are in reference to the origin, it will be moved by the pipe_making_engine by its randomized y coordinates
ULX_T = 0			#upper left x coordinate of top pipe
ULY_T = HEIGHT			#upper left y coordinate of top pipe
LRX_T = PIPEWIDTH		#lower right x coordinate of top pipe
LRY_T = 0			#lower right y coordinate of top pipe
#bottom pipes dimension		#pipe dimensions are in reference to the origin, it will be moved by the pipe_making_engine by its randomized y coordinates
ULX_B = 0			#upper left x coordinate of bottom pipe
ULY_B = 0			#upper left y coordinate of bottom pipe
LRX_B = PIPEWIDTH		#upper left x coordinate of bottom pipe
LRY_B = -HEIGHT			#lower left y coordinate of bottom pipe
#game variables			#in game stuff
GAME_RUN = True			#flag variable for the game running in engine.engine()
GRAVITY = 0.11 			#positive number, already accounted for in the Turtle class, recommended maximum: 0.12
#hidden variables
#SCORE - in the Turtle class
#PASSED - in the PipeTop class

'''
CLASSES
List of Classes: 
Turtle - the class that the user controls. calls pipe_making_engine(). stored in a variable Player
Boom - explosion animation when the Player dies. this was sourced from the demo.py example. 
	isoob() = False because if the Turtle isoob() == True, then the Boom should not be deleted because it will be also be isoob() == True too
PipeTop, PipeBottom - the pipe classes. the reason why they are separate [e.g. PipeTop and PipeBottom] is because of the different way 
			each type of pipe is drawn. the PipeTop class has the tests and properties required by the scoring system to maintain score
'''
class Turtle(engine.GameObject):
	SCORE = 0 #initialized when an instance is created
	def __init__(self, x, y):
		'''
		setting delta x to some number [e.g. 1, or -1] would give TURTLEREX some realistic movement but would continuously
		move the turtle forward. the object would also overshoot the set boundaries of TURTLEREX
		'''
		super().__init__(x, y, 0, 0, TURTLESHAPE, TURTLECOLOR)

	#POSITIONAL FUNCTIONS
	def get_x(self):
		return self.x
	def get_y(self):
		return self.y
	def get_front(self):
		return self.x + BOUND_SIZEX
	def get_back(self):
		'''		
		method is still used for future figures where the leftmost of the image is not the x-coordinate like TURTLEREX.
		this is because the collision detection system uses a system of conditions that test the bounds of the object as
		long as one sets it properly. one could just uncomment the "- BOUND_SIZEX" to use it
		'''
		return self.x #- BOUND_SIZEX
	def get_top(self):
		return self.y + BOUND_SIZEY
	def get_bottom(self):
		return self.y - BOUND_SIZEY

	#PROPERTIES FUNCTIONS
	def delete(self):
		'''
		the Class Turtle is designed to blow up when it is deleted from the game engine [e.g. Player leaves off-screen, bump the pipes, etc]
		'''
		engine.add_obj(Boom(self.x, self.y, BLASTRADIUS))
		super().delete()
		end_game() #connects the Player to the conditional statement for GAME_RUN and execute accordingly
	def step(self): 
		'''
		pipes are made when player exists. interval determined by the variable PIPEINTERVAL		
		adding something to engine.GameEngine default step function for a gravity influenced free fall
		'''
		if (self.age % PIPEINTERVAL) == 0:
			pipe_making_engine()
		self.deltay = self.deltay - GRAVITY
		super().step()
	def reset_gravity(self):
		self.deltay = 0 #a positive value will give the illusion of flapping bird

	#SCORE MANAGING FUNCTIONS
	def get_score(self):
		return self.SCORE
	def increment(self):
		self.SCORE = self.SCORE + 1

class Boom(engine.GameObject): #SOURCE: demo.py
	def __init__(self, x, y, maxdiameter):
		self.maxdiameter = maxdiameter
		self.diameter = 0
		super().__init__(x, y, 0, 0, 'circle', 'orange')

	def draw(self):
		oldmode = turtle.resizemode()
		turtle.shapesize(outline=self.diameter)
		id = super().draw()
		turtle.resizemode(oldmode)
		return id

	def isoob(self):
		return False
	
	def step(self):
		newsize = abs(math.sin(math.radians(self.age) + 180))
		if newsize < 0.05:
			engine.del_obj(self)
			return
		self.diameter = newsize * (self.maxdiameter * 2)
		super().step()		

class PipeTop(engine.GameObject):
	'''
	REDESIGNED. things are drawn differently when deltax or deltay varies.
	the class where the score keeper flag is kept
	'''
	n_pipes = 0
	def __init__(self, x, y):
		name = 'PipeTop.%d' % PipeTop.n_pipes #SOURCE: demo.py
		PipeTop.n_pipes = PipeTop.n_pipes + 1

		'''
		still treat ulx, uly, lrx, and lry as respective coordinated for a rectangle. the math will do the job.

		the MATHS are very strong here... took about 6-7 hours to figure out.
		(ULY, -ULX), (ULY, -LRX), (LRY, -LRX), (LRY, -ULX) #(drawing on the positive x,y-axes when deltax is negative)
		(-ULY, ULX), (-ULY, LRX), (-LRY, LRX), (-LRY, ULX) #(drawing on the positive x,y-axes when deltax is positive)
		'''

		turtle.register_shape(name, (
			(ULY_T, -ULX_T), (ULY_T, -LRX_T), (LRY_T, -LRX_T), (LRY_T, -ULX_T)
		))

		'''
		super().__init__'s x and y variables are where the pipes are based
		'''

		super().__init__(x, y, -PIPEPACE, 0, name, PIPECOLOR)

		self.PASSED = False
		'''
		initialed when new instances of pipes are made. this variable is unique to every PipeTop instance
		which is then checked to account for the score system logic
		'''

	def isstatic(self): #when game ends, pipe will not move
		if GAME_RUN:
			return False
		else:
			return True

	def istop(self): #one function know the type of pipe [top or bottom pipe?]
		return True
	def get_x(self):
		return self.x
	def get_y(self):
		return self.y
	def get_edge(self): #XXX NO EDGE.
		return self.x + PIPEWIDTH

	def didpass(self): #top pipe is the scoring basis
		return self.PASSED
	def okpass(self):
		self.PASSED = True


class PipeBottom(engine.GameObject): #redesigned.. things are drawn differently when deltax or deltay varies 
	'''
	REDESIGNED. things are drawn differently when deltax or deltay varies.
	'''
	n_pipes = 0
	def __init__(self, x, y):
		name = 'PipeBottom.%d' % PipeBottom.n_pipes #SOURCE: demo.py
		PipeBottom.n_pipes = PipeBottom.n_pipes + 1

		'''
		still treat ulx, uly, lrx, and lry as respective coordinated for a rectangle. the math will do the job.

		the MATHS are very strong here... took about 6-7 hours to figure out.
		(ULY, -ULX), (ULY, -LRX), (LRY, -LRX), (LRY, -ULX) #(drawing on the negative x,y-axes when deltax is negative)
		(-ULY, ULX), (-ULY, LRX), (-LRY, LRX), (-LRY, ULX) #(drawing on the negative x,y-axes when deltax is positive) [UNTESTED!]
		'''

		turtle.register_shape(name, (
			(ULY_B, -ULX_B), (ULY_B, -LRX_B), (LRY_B, -LRX_B), (LRY_B, -ULX_B)
		))

		'''
		super().__init__'s x and y variables are where the pipes are based
		'''

		super().__init__(x, y, -PIPEPACE, 0, name, PIPECOLOR)

	def isstatic(self): #when game ends, pipe will not move
		if GAME_RUN:
			return False
		else:
			return True

	def istop(self): #one function to know the type of pipe [top or bottom pipe?]
		return False
	def get_x(self):
		return self.x
	def get_y(self):
		return self.y
	def get_edge(self): #XXX NO EDGE.
		return self.x + PIPEWIDTH

'''
FUNCTIONS
List of Functions: [SEQUENCE DEPENDENCIES]
title_sequence - draws the title screen [turtle, random, time, HEIGHT, TITLETEXT1, TITLETEXT2]
inputkb_cb - callback function for keyboard events 
main_button - activated when called upon by a condition from the keyboard callback function. contains mechanisms essential 
		for running the game and moving the player
pipe_making_engine - the engine that makes the randomization for the height of the pipes following a preset GAPDISTANCE
end_game - a function call to end the game. occurs when the Player dies. calls the gameover_sequence
gameover_sequence - draws the game over screen [ENDCOLOR, Player]
play_sequence - start the game or restarts the game while the engine.engine() is running
score_sequence - draws the score at the top left of the screen. this score is a passed value. [WIDTH, HEIGHT, GAMECOLOR, SCORECOLOR]
score_counter - operations for the score system (changing the PipeTop flag, incrementing SCORE, calling score_sequence). 
			integrated to the collision detection system because one could only score or crash into a pipe
test_collision_x - tests collision in the x-axis by means of the Player's 'back' and 'front' boundaries
test_collision_y - tests collision in the y-axis by means of the Player's 'top' and 'bottom' boundaries
turtle_collision_cb - collision testing nexus --- integrates both x-axis and y-axis collision tests and the scoring system
pipe_collision_cb - reverse of order of variable call of turtle_collision_cb
'''

def title_sequence(): #spiced up title screen
	colors = ['green', 'blue', 'red', 'orange', 'yellow', 'lavender']
	turtle.bgcolor('black')
	t1 = turtle.Turtle()
	t2 = turtle.Turtle()
	t1.ht()
	t2.ht()
	t1.penup()
	t2.penup()
	t1.goto(0, HEIGHT/2)
	t2.goto(0, -HEIGHT/2)
	Proceed = True
	while Proceed:
		t1.color(random.choice(colors))
		t2.color(random.choice(colors))
		t1.write(TITLETEXT1, align='center', font=('Arial', 48, 'italic'))
		t2.write(TITLETEXT2, align='center', font=('Arial', 48, 'italic'))
		t1.goto(0, (t1.ycor() - 12))
		t2.goto(0, (t2.ycor() + 12))
		t1.clear()
		t2.clear()
		if t2.ycor() > t1.ycor(): #collision in the middle
			Proceed = False
	turtle.bgcolor('white') #flash o' white
	time.sleep(0.1)
	turtle.bgcolor('black')
	time.sleep(0.38)
	turtle.penup()
	turtle.goto(-300,0)
	turtle.pendown()
	turtle.color('white')
	turtle.write((TITLETEXT1+'\n'+TITLETEXT2), True, align='left', font=('Arial', 48, 'italic'))
	time.sleep(3)
	turtle.undo()

def inputkb_cb(key):
	if key == 'q' or key == 'Q':
		engine.exit_engine()
	elif key == 'space':
		main_button()

def main_button():
	global Player
	Player.y = Player.y + 42 #answer to life, the universe and everything
	Player.reset_gravity()
	if not GAME_RUN: #reset the game
		play_sequence()

def pipe_making_engine():
	'''
	design is a fixed height pipe (even more stable after figuring out the maths)
	'''
	top_pipe = random.randint((-HEIGHT//4), (HEIGHT//4)) #floor division only! (random.randint may not be happy)
	bottom_pipe = top_pipe - GAPDISTANCE
	engine.add_obj(PipeTop(PIPESTART, top_pipe))
	engine.add_obj(PipeBottom(PIPESTART, bottom_pipe))

#GAME GROUP
def end_game():
	'''
	successor to the game_state() function which was not needed anymore because the Turtle can call it quits when it dies
	PROS: lesser code, lesser load on performance CONS: None so far.
	'''
	global GAME_RUN
	GAME_RUN = False
	gameover_sequence()
	#XXX if only there was a function to stop input for a given time XXX

def gameover_sequence():
	turtle.goto(0,0)
	turtle.color(ENDCOLOR)
	turtle.write('GAME\nOVER', align='center', font=('IMPACT', 80, 'bold'))
	turtle.goto(0,-50)
	turtle.write('Your Score: ' + str(Player.get_score()), align='center', font=('IMPACT', 30, 'bold'))	
	turtle.goto(0,-250)
	turtle.write('Press SPACE to restart \n Press Q to chicken out', align='center', font=('IMPACT', 30, 'bold'))

def play_sequence():
	global GAME_RUN
	global Player
	GAME_RUN = True
	turtle.color(GAMECOLOR) #masking the movement to the initial position
	Player = Turtle(INIT_POSX, INIT_POSY)
	engine.init_engine()
	engine.set_keyboard_handler(inputkb_cb)
	engine.register_collision(Turtle, PipeTop, turtle_collision_cb)
	engine.register_collision(PipeTop, Turtle, pipe_collision_cb)
	engine.register_collision(Turtle, PipeBottom, turtle_collision_cb)
	engine.register_collision(PipeBottom, Turtle, pipe_collision_cb)
	engine.add_obj(Player)

#SCORE GROUP
def score_sequence(score): #referenced from invader.py
	turtle.goto((-WIDTH/2)+50, (HEIGHT/2)-50)
	turtle.dot(70, GAMECOLOR) #matching the game background
	turtle.color(SCORECOLOR)
	turtle.write(score, align='center', font=('Arial', 20, 'bold'))

def score_counter(obj1, obj2):
	obj2.okpass() #changes the flag of the specified pipe (in this version, the TopPipe)
	obj1.increment() #increments the score that the turtle holds
	score_sequence(obj1.get_score()) #prints the score
	
#COLLISION DETECTION GROUP
def test_collision_x(obj1, obj2):
	if obj2.get_x() < obj1.get_front() < obj2.get_edge():
		return True		
	elif obj2.get_x() < obj1.get_back() < obj2.get_edge():
		return True
	return False

def test_collision_y(obj1, obj2):
	if obj2.istop():
		if obj1.get_top() > obj2.get_y():
			return True
	elif not obj2.istop():
		if obj1.get_bottom() < obj2.get_y():
			return True
	return False

def turtle_collision_cb(obj1, obj2): #score function is here.. either one scores or explodes
	if (test_collision_x(obj1, obj2) and test_collision_y(obj1, obj2)):
		engine.del_obj(obj1) #just deleting the Turtle will take care of game over behavior

	elif obj2.istop() and not obj2.didpass(): #checks for if PipeTop object and the pipe did not yet pass the turtle
		if obj2.get_edge() < obj1.get_back():
			score_counter(obj1,obj2)
	
def pipe_collision_cb(obj1, obj2):
	turtle_collision_cb(obj2, obj1)

#main()
if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	title_sequence()
	turtle.bgcolor(GAMECOLOR) #make sure color for the game is set
	play_sequence()
	engine.engine() #GAME START!

'''
BIBLIOGRAPHY:
Aycock, J. Personal Communication, University of Calgary, Calgary, AB April 2014
Sherlock, M.J. Personal Communication, University of Calgary, Calgary, AB April 2014
'''
#version: 04.04.2014 [FINAL_RELEASE] : Fri 04 Apr 2014 02:17:16 PM MDT 
