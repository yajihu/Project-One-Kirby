#reference:
#https://imgur.com/gallery/vdC7V/comment/448023364
import pygame
import random
import sys
import math
import time
import os

# import the pygame constants (specifically the key codes and event types)
from pygame.locals import *

# constants for accessing the attributes of the mouse
MOUSE_LMB = 0
MOUSE_RMB = 1
MOUSE_X   = 2
MOUSE_Y   = 3

# the resolution of the display window (but please note that the toy runs in fullscreen mode)
window_wid = 1200
window_hgt = 800

# the frame rate is the number of frames per second that will be displayed and although
# we could (and should) measure the amount of time elapsed, for the sake of simplicity
# we will make the (not unreasonable) assumption that this "delta time" is always 1/fps
frame_rate = 60
delta_time = 1 / frame_rate

# these are the colours through which the game objects can be "cycled"
included_images = []
included_images.append(pygame.image.load("Assets/resources/1.png"))
included_images.append(pygame.image.load("Assets/resources/2.png"))
included_images.append(pygame.image.load("Assets/resources/3.png"))
included_images.append(pygame.image.load("Assets/resources/4.png"))
included_images.append(pygame.image.load("Assets/resources/5.png"))
included_images.append(pygame.image.load("Assets/resources/6.png"))
included_images.append(pygame.image.load("Assets/resources/7.png"))
included_images.append(pygame.image.load("Assets/resources/8.png"))
included_images.append(pygame.image.load("Assets/resources/9.png"))
included_images.append(pygame.image.load("Assets/resources/10.png"))
included_images.append(pygame.image.load("Assets/resources/11.png"))
included_images.append(pygame.image.load("Assets/resources/12.png"))
# these are the unique identifiers for the game objects
object_unique_id = 1000

# this is the only game object included in the "toy" - rename it when5 you decide what
# these objects will represent within the "magic circle" of your final game submission
# and feel free to modify it as required, as long as you preserve the core mechanics 
class Object:

	def __init__(self):

		# get the next unique identifier and increment
		global object_unique_id
		self.id = object_unique_id
		object_unique_id += 1
	
		# the radius of the game object is fixed
		self.radius = 15
		
		# the initial colour is randomly selected and the "focus" flag is false
		self.sprite = random.randint(0, len(included_images) - 1)
		self.flag = False
		
		self.RL = random.randint(0, 1)
		# (x, y) / (dx, dy) / (ddx, ddy) is the position / velocity / acceleration
		if self.RL == 0:
			self.x = -self.radius
		else:
			self.x = window_wid + 1
		#self.x = random.randint(self.radius, window_wid - 1 - self.radius)
		self.y = random.randint(self.radius, window_hgt - 200)
		angle = random.randint(0, 359)
		self.dx = math.cos(math.radians(angle)) * 0.5
		self.dy = math.sin(math.radians(angle))	* 0.5	
		self.ddx = 0
		self.ddy = 0
		self.destroy = False
		self.worth = random.randint(0, 20)
		self.health = 1
		
		
class Ship:
	def __init__(self):
		self.ship = {
			"name": "ready_player_one",
			"level": 1,
			"ending": 0,
            "position": [window_wid / 2 -50, 710],
            "velocity": 7,
            "angle": 0,
			"mode": 3,
			"bullets": 5000,
			"bullet_cost": 250,
			"charge": 1,
			"health": 2000,
			"fire": False,
            "entity": pygame.transform.rotozoom(pygame.image.load("Assets/ships/playerShip2_green.png").convert_alpha(), 0, 1),
            "destroy": False,
			"change": True,
			"health_color": (0,255,127),
			"score": 0,
			"resources": 0,
			"size": [112,75],
			"magnitude": 2000,
			"magnitude_recover": 5,
			"bg": pygame.transform.rotozoom(pygame.image.load("Assets/backgrounds/Background-{}.jpg".format(random.randint(0, 3))).convert_alpha(), 0, 1),
			
			"ed1": pygame.transform.scale(pygame.image.load("Assets/backgrounds/1.png"),[1200,800]),
			"ed2": pygame.transform.scale(pygame.image.load("Assets/backgrounds/2.png"),[1200,800]),
			"ed3": pygame.transform.scale(pygame.image.load("Assets/backgrounds/3.png"),[1200,800]),
        }
class Menu:
	def __init__(self):
		self.menu = {
		"bg": pygame.transform.rotozoom(pygame.image.load("Assets/main_menu/space.png").convert_alpha(), 0, 1),
		"title": pygame.transform.scale(pygame.image.load("Assets/main_menu/title.png"),[1470,69]),
		"start": pygame.transform.scale(pygame.image.load("Assets/main_menu/start.png"),[490,85]),
		"start2": pygame.transform.scale(pygame.image.load("Assets/main_menu/start2.png"),[490,85]),
		"exit": pygame.transform.scale(pygame.image.load("Assets/main_menu/exit.png"),[490,85]),
		"exit2": pygame.transform.scale(pygame.image.load("Assets/main_menu/exit2.png"),[490,85]),
		"next": pygame.transform.scale(pygame.image.load("Assets/main_menu/exit.png"),[490,85]),
		
		"1": pygame.transform.rotozoom(pygame.image.load("Assets/tutorial/1.png").convert_alpha(), 0, 1),
		"2": pygame.transform.rotozoom(pygame.image.load("Assets/tutorial/2.png").convert_alpha(), 0, 1),
		"3": pygame.transform.rotozoom(pygame.image.load("Assets/tutorial/3.png").convert_alpha(), 0, 1),
		"4": pygame.transform.rotozoom(pygame.image.load("Assets/tutorial/4.png").convert_alpha(), 0, 1),
		"5": pygame.transform.rotozoom(pygame.image.load("Assets/tutorial/5.png").convert_alpha(), 0, 1),
		"6": pygame.transform.rotozoom(pygame.image.load("Assets/tutorial/6.png").convert_alpha(), 0, 1),
		
		"is_start": False,
		"is_exit": False,
		"is_menu": True,
		"is_end": False,
		}
		
class Bullet:
	def __init__(self, x ,y):
		self.bullet = {
            "position": [x, y],
            "velocity": None,
			"damage": 10,
			"fire": True,
            "entity": pygame.transform.scale(pygame.image.load("Assets/cannonball/laser.png"),[40,55]),
            "destroy": False,
			"exists": False,
        }

class EnemyBoss:
	def __init__(self):
		self.boss = {
            "position": [window_wid / 2 -150, -10],
            "health_color": (255,215,0),
            "angle": 0,
			"health": 1000,
			"fire": False,
            "entity": pygame.transform.scale(pygame.image.load("Assets/ships/boss.png"), [226,172]),
            "destroy": False,
			"size": [226,172],
			
        }
		

class BossLaser:
	def __init__(self):
		self.laser = {
			"position": [window_wid / 2 -50 , 50],
			"velocity": None,
			"damage": 100,
			"entity": pygame.transform.scale(pygame.image.load("Assets/cannonball/laser4.png"),[50,50]),
			"size": [50,50],
			"destroy": False,
			"exists": False,
			"angle": 0,
			"speed": 4,
			"ult": 0,
		}

class EnemyShip:
	def __init__(self):
		self.enemy = {
            "position": [random.randint(100, 1100), 0],
			"velocity": None,
            "health_color": (255,215,0),
			"health": 100,
            "entity": pygame.transform.scale(pygame.image.load("Assets/ships/cannon_{}.png".format(random.randint(1, 4))), [104,84]),
            "destroy": False,
			"size": [104,84],
			"damage": 50,
			"worth": random.randint(700, 1000)

        }



def get_all_inputs():

	# get the state of the mouse (i.e., button states and pointer position)
	mouse_dict = {}
	(mouse_dict[MOUSE_LMB], _, mouse_dict[MOUSE_RMB]) = pygame.mouse.get_pressed()
	(mouse_dict[MOUSE_X], mouse_dict[MOUSE_Y]) = pygame.mouse.get_pos()

	# get the state of the keyboard
	keybd_tupl = pygame.key.get_pressed()
		
	# look in the event queue for the quit event
	quit_ocrd = False
	for evnt in pygame.event.get():
		if evnt.type == QUIT:
			quit_ocrd = True

	# return all possible inputs
	return mouse_dict, keybd_tupl, quit_ocrd
	
	
#### ====================================================================================================================== ####
#############											UPDATE													#############
#### ====================================================================================================================== ####
		
	
def update_all_ship_objects(ship_object, bullet_object, game_objects, mouse_dict):
	ship = ship_object.ship
	bullet = bullet_object.bullet
	

	# visit all the game objects...
	ship['score']+=1
	if ship["magnitude"] < 2000:
		ship["magnitude"]+=ship["magnitude_recover"]
	for object in game_objects:
	
		# reset the flags
		object.flag = False
		
		# if the game object is beneath the mouse...
		if ((ship["position"][0]+50 - mouse_dict[MOUSE_X]) ** 2 + (ship["position"][1] - mouse_dict[MOUSE_Y]) ** 2) < (84 ** 2):
	
			# ...then set the flag on that one
			object.flag = True
			
			# if the left button is clicked, change the colour
			if mouse_dict[MOUSE_LMB] and ship["change"]:
				if ship["mode"] == 1:
					ship["entity"] = pygame.transform.rotozoom(pygame.image.load("Assets/ships/playerShip2_blue.png").convert_alpha(), 0, 1)
					ship["change"] = False
					ship["mode"] = 2
				elif ship["mode"] == 2:
					ship["entity"] = pygame.transform.rotozoom(pygame.image.load("Assets/ships/playerShip2_green.png").convert_alpha(), 0, 1)
					ship["change"] = False
					ship["mode"] = 3
				elif ship["mode"] == 3:
					ship["entity"] = pygame.transform.rotozoom(pygame.image.load("Assets/ships/playerShip2_red.png").convert_alpha(), 0, 1)
					ship["change"] = False
					ship["mode"] = 1
			# if the right button is clicked, attract all other objects of the same colour
			elif mouse_dict[MOUSE_RMB]:

				if ship["mode"] == 1:#fire
					ship["fire"] = True
					bullet["exists"] = True
					
				elif ship["mode"] == 2:#loading
					ship["fire"] = False
					if(ship["bullets"] < 5000):
						ship["bullets"] += ship["charge"]

				elif ship["mode"] == 3:#collecting
					ship["fire"] = False
					if ship["magnitude"] > 0:
						ship["magnitude"]-=1
						#print(ship["magnitude"])
						for another in game_objects:
							
							delta_x = ship['position'][0] + (ship['size'][0] * 1/2) - another.x
							delta_y = ship['position'][1] + (ship['size'][0] * 1/2) - another.y
							magnitude = math.sqrt(delta_x ** 2 + delta_y ** 2)*30
							if another.dx < 8 and another.dx > -8 and another.dy < 8 and another.dy > -8:
								another.dx = another.dx + (delta_x / magnitude) / 2
								another.dy = another.dy + (delta_y / magnitude) / 2
							if object.x + object.dx > ship['position'][0] and object.x + object.dx < ship['position'][0]+ship['size'][0] and object.y + object.dy > ship['position'][1]:
								object.destroy = True
								ship["resources"] += object.worth
								if ship["health"] < 2000:
									ship["health"] += object.health
				
				else:
					angle = random.randint(0, 359)
					another.dx = math.cos(math.radians(angle)) * 0.5
					another.dy = math.sin(math.radians(angle))	* 0.5	
				
		# update the positions
		
		if object.x + object.dx > -object.radius and object.x + object.dx < window_wid + 1:
			object.x += object.dx 
		else:
			object.dx = object.dx * -1
			
		if object.y + object.dy > object.radius and object.y + object.dy< window_hgt - 1 - object.radius:
			object.y += object.dy
		else:
			object.dy = object.dy * -1
		
		

	return game_objects

	

def update_bullet(ship_object, bullet_object,boss_object,laser_object, enemy_objects, window):

	ship = ship_object.ship
	bullet = bullet_object.bullet
	boss = boss_object.boss
	laser = laser_object.laser
	enemy = enemy_objects
	
	#enemy ships
	for enemyship in enemy:
		window.blit(enemyship.enemy["entity"], enemyship.enemy["position"])
		if enemyship.enemy['destroy'] == True:
			enemyship.enemy['position'][0] = random.randint(100, 1100)
			enemyship.enemy['position'][1] = 0
			enemyship.enemy['velocity'] = None 
			enemyship.enemy['destroy'] = False
			enemyship.enemy['exists'] = False
		
		if enemyship.enemy['velocity'] == None:	

			enemyship.enemy['velocity'] = random.randint(2, 6)
				
		else:
			
			if enemyship.enemy['position'][1] + enemyship.enemy['velocity'] > 0 and enemyship.enemy['position'][1] + enemyship.enemy['velocity'] < 800:
				enemyship.enemy['position'][1] = enemyship.enemy['position'][1] + enemyship.enemy['velocity']
			else:
				enemyship.enemy['destroy'] = True
			
			if enemyship.enemy['position'][1] + enemyship.enemy['velocity'] > ship['position'][1]-ship['size'][1] and enemyship.enemy['position'][0]+ship['size'][0]-10 > ship['position'][0] and enemyship.enemy['position'][0] < ship['position'][0]+ship['size'][0] :
				enemyship.enemy['destroy'] = True
				ship['health'] = ship['health'] - enemyship.enemy['damage']
			
	
	#ship bullet
	if ship['fire'] and bullet["exists"] and ship['bullets'] > 249:
		window.blit(bullet["entity"], bullet["position"])
		if bullet['destroy'] == True:
			ship['bullets'] = ship['bullets'] - ship['bullet_cost']
			bullet['position'][0] = ship['position'][0] + 36
			bullet['position'][1] = ship['position'][1] - 17
			bullet['velocity'] = None 
			bullet['destroy'] = False
			bullet['exists'] = False

		if bullet['velocity'] == None:
			bullet['velocity'] = 25

		else:
			
			if bullet['position'][1] + bullet['velocity'] > 0 and bullet['position'][1] + bullet['velocity'] < 800:
				bullet['position'][1] = bullet['position'][1] - bullet['velocity']
			else:
				bullet['destroy'] = True
				
			#hit boss	
			if bullet['position'][1] + bullet['velocity'] < boss['position'][1]+boss['size'][1] and bullet['position'][0] > boss['position'][0] and bullet['position'][0] < boss['position'][0]+boss['size'][0] :
				bullet['destroy'] = True
				boss['health'] = boss['health'] - bullet['damage']
				
			for enemyship in enemy:
				if bullet['position'][1] + bullet['velocity'] < enemyship.enemy['position'][1]+enemyship.enemy['size'][1] and bullet['position'][0] > enemyship.enemy['position'][0] and bullet['position'][0] < enemyship.enemy['position'][0]+enemyship.enemy['size'][0] :
					bullet['destroy'] = True
					enemyship.enemy['destroy'] = True
					ship['score']+=enemyship.enemy['worth']
			
	else:
		bullet['position'][0] = ship['position'][0] + 36
		bullet['position'][1] = ship['position'][1] - 17
		
	#boss laser
	
	if laser['destroy'] == True:
		laser['position'][0] = 550
		laser['position'][1] = 50
		laser['velocity'] = None 
		laser['destroy'] = False
		laser['exists'] = False
	else:
		window.blit(laser["entity"], laser["position"])
		
	if laser['velocity'] == None:	

		laser['angle'] = math.atan2(boss['position'][1] - ship["position"][1], boss['position'][0] - ship["position"][0])
		laser['velocity'] = [-math.cos(laser['angle'])*laser['speed'], -math.sin(laser['angle'])*laser['speed']]
			
	else:
		
		if laser['position'][0] + laser['velocity'][0] > 0 or laser['position'][0] + laser['velocity'][0] < 1200:
			laser['position'][0] = laser['position'][0] + laser['velocity'][0]
		else:
			laser['destroy'] = True

		if laser['position'][1] + laser['velocity'][1] > 0 and laser['position'][1] + laser['velocity'][1] < 800:
			laser['position'][1] = laser['position'][1] + laser['velocity'][1]
		else:
			laser['destroy'] = True
		
	if laser['position'][1] + laser['velocity'][1] > ship['position'][1] and laser['position'][0] > ship['position'][0] and laser['position'][0] < ship['position'][0]+ship['size'][0] :	
		ship['health'] = ship['health'] - laser['damage']
		laser['destroy'] = True

		
#update the battle data with boss, and boss rotation		
def update_boss(ship_object, boss_object):
	ship = ship_object.ship
	boss = boss_object.boss
	#boss['angle'] = math.atan2(window_hgt - ship['position'][1], window_wid - ship['position'][0])
	boss['angle'] = - (math.atan2(boss["position"][1] - ship['position'][1], boss["position"][0] - ship['position'][0])) * 180/math.pi + 270
	if ship["health"] < 1000:
		ship["health_color"] = (255, 140, 0)
	else:
		ship["health_color"] = (0,255,127)
	if boss["health"] < 300:
		boss["health_color"] = (255, 0, 0)

		
def render_all(window, clock, ship_object, bullet_object, boss_object):
	ship = ship_object.ship
	bullet = bullet_object.bullet
	boss = boss_object.boss
	
	#ship health bar
	pygame.draw.rect(window, ship["health_color"], (10,10,ship["health"]/10,10))
	pygame.draw.rect(window, Color(255,255,255), (10,10,200,10),3)
	
	#boss health bar
	pygame.draw.rect(window, boss["health_color"], (690,10,boss["health"]/2,12))
	pygame.draw.rect(window, Color(255,255,255), (690,10,500,12),3)
	
	window.blit(ship["entity"], ship["position"])
	
	#boss image
	bossImage = pygame.transform.rotate(boss["entity"], boss["angle"])
	window.blit(bossImage, boss["position"])
	
	#ship bullet bar
	pygame.draw.rect(window, Color(255,173,201), (10,30,ship["bullets"]/25,10))
		
	for x in range(0, 21):	
		pygame.draw.rect(window, Color(255,255,255), (10,30,10*x,10),3)
	
	pygame.draw.rect(window, Color(135, 206, 250), (10,50,ship["magnitude"]/10,10))
	pygame.draw.rect(window, Color(255,255,255), (10,50,200,10),3)
	
	
	font = pygame.font.SysFont('Comic Sans MS', 18)
	
	text = font.render('Levels:', False, (255, 255, 255))
	window.blit(text,(10,65))
	text = font.render(str(ship['level']), False, (255, 255, 255))
	window.blit(text,(75,65))
	'''
	text = font.render('Commander:', False, (255, 255, 255))
	window.blit(text,(10,65))
	text = font.render(str(ship['name']), False, (255, 255, 255))
	window.blit(text,(115,65))
	'''
	text = font.render('Resources:', False, (255, 255, 255))
	window.blit(text,(10,90))
	text = font.render(str(ship['resources']).zfill(5), False, (255, 255, 255))
	window.blit(text,(105,90))
	
	text = font.render('Scores:', False, (255, 255, 255))
	window.blit(text,(10,115))
	text = font.render(str(ship['score']).zfill(8), False, (255, 255, 255))
	window.blit(text,(80,115))
	
	

def main_menu(window, menu_object):
	menu = menu_object.menu
	events = pygame.event.get()
	mouse = pygame.mouse.get_pos()
	
	if menu["is_menu"]:
		window.blit(menu["bg"], (0,0))
		window.blit(menu["title"], (265,100))
		
		if mouse[0] > 480 and mouse[0] < 680 and mouse[1] > 415 and mouse[1] < 464:
			window.blit(menu["start2"], (480,400))
		else:
			window.blit(menu["start"], (480,400))
		
		if mouse[0] > 500 and mouse[0] < 650 and mouse[1] > 560 and mouse[1] < 615:
			window.blit(menu["exit2"], (500,550))
		else:
			window.blit(menu["exit"], (500,550))
			
		for event in events:
			if event.type == pygame.MOUSEBUTTONUP:
				
				if mouse[0] > 480 and mouse[0] < 680 and mouse[1] > 415 and mouse[1] < 464:
					menu['is_start'] = True
					menu["is_menu"] = False

				elif mouse[0] > 500 and mouse[0] < 650 and mouse[1] > 560 and mouse[1] < 615:
					menu['is_exit'] = True
					menu["is_menu"] = False


#upgrade ship ability base by resources
def upgrade(ship_object, bullet_object,boss_object,laser_object):					
	ship = ship_object.ship
	bullet = bullet_object.bullet
	boss = boss_object.boss
	laser = laser_object.laser
	if ship['resources'] > 25000:
		ship["velocity"] = 17
		bullet['damage'] = 30
		laser['damage'] = 150
		laser['speed'] = 10
		ship["charge"] = 2
		ship['level'] = 3
	elif ship['resources'] > 10000:
		ship["velocity"] = 12
		bullet['damage'] = 20
		laser['speed'] = 7
		ship['level'] = 2

def update_ending(ship_object, boss_object, menu_object):
	ship = ship_object.ship
	boss = boss_object.boss
	menu = menu_object.menu

	if ship['health'] < 1:
		ship['ending'] = 2
		menu['is_end'] = True
	if boss['health'] < 1:
		if ship['resources'] > 25000:
			ship['ending'] = 1
			menu['is_end'] = True
		else:
			ship['ending'] = 3
			menu['is_end'] = True


	
def main():
	
	# initialize pygame
	pygame.init()
	
	pygame.font.init() 
	

	
	# create the window and set the caption of the window
	window_sfc = pygame.display.set_mode( (window_wid, window_hgt) ) #, FULLSCREEN )
	pygame.display.set_caption('Project One: Kirby')
	
	# create a clock
	clock = pygame.time.Clock()
	start_ticks=pygame.time.get_ticks() #starter tick
	timer = pygame.time.get_ticks() #calculate how many seconds
	
	menu = Menu()
	#load BGM
	pygame.mixer.music.load("Assets\sound\Orbital Colossus.mp3")
	pygame.mixer.music.play(-1)
	
	
	
	number_of_objects = 16
	game_objects = []
	for i in range(number_of_objects):
		game_objects.append(Object())
	
	number_of_enemy = 5
	enemy_objects = []
	
	for i in range(number_of_enemy):
		enemy_objects.append(EnemyShip())
		
	ship = Ship()
	bullet = Bullet(ship.ship["position"][0]+36,ship.ship["position"][1]-17)
	boss = EnemyBoss()
	laser = BossLaser()
	
	# the game loop is a postcondition loop controlled using a Boolean flag
	
	closed_flag = False
	
	while not closed_flag:
		#print(pygame.time.get_ticks())
		# get the inputs from the mouse and check if the window has been closed
		#window_sfc.fill(Color(255, 255, 255))
		timer = pygame.time.get_ticks() #calculate how many seconds
		main_menu(window_sfc, menu)

		if menu.menu['is_start']:
			window_sfc.blit(ship.ship["bg"], (0,0))
			main_menu(window_sfc, menu)

			mouse_dict, keybd_tupl, closed_flag = get_all_inputs()
			if keybd_tupl[pygame.K_ESCAPE]:
				closed_flag = True

			if keybd_tupl[pygame.K_a]:
				if ship.ship["position"][0] - ship.ship["velocity"] > 0:
					ship.ship["position"][0] = ship.ship["position"][0] - ship.ship["velocity"]

			if keybd_tupl[pygame.K_d]:
				if ship.ship["position"][0] + ship.ship["velocity"] < 1100:
					ship.ship["position"][0] = ship.ship["position"][0] + ship.ship["velocity"]

			
			# update the positions and velocities of all the game objects in the toy, and ship mode
			game_objects = update_all_ship_objects(ship,bullet, game_objects, mouse_dict)
			
			if ship.ship["change"] == False:
				seconds = (pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
				if seconds > 1: #1 seconds cooldown for changing mode
					ship.ship["change"] = True
					start_ticks = pygame.time.get_ticks()
		
			# main update
			update_boss(ship, boss)
			update_bullet(ship, bullet,boss,laser,enemy_objects, window_sfc)
			upgrade(ship, bullet,boss,laser)
			update_ending(ship, boss, menu)
			
			
			# draw each of the game objects and encircle the one that is flagged
			for object in game_objects:
				window_sfc.blit(included_images[object.sprite],(int(object.x), int(object.y)))
			if len(game_objects) < 5: #reload resources if less than 5
				for i in range(number_of_objects):
					game_objects.append(Object())
			
			for object in game_objects:
				if object.destroy:
					game_objects.remove(object)
					del object
					
			# render the game objects to the display
			render_all(window_sfc, clock, ship, bullet, boss)
			# update the display and enforce the minimum frame rate
			
			if menu.menu["is_end"]:
				menu.menu["is_start"] = False
				if ship.ship['ending'] == 1:
					window_sfc.blit(ship.ship["ed1"], (0,0))
					font = pygame.font.SysFont('Comic Sans MS', 56)
					text = font.render('Your score:', False, (255, 255, 255))
					window_sfc.blit(text,(300,650))
					text = font.render(str(ship.ship['score']), False, (255, 255, 255))
					window_sfc.blit(text,(600,650))
					
				elif ship.ship['ending'] == 2:
					window_sfc.blit(ship.ship["ed2"], (0,0))
					font = pygame.font.SysFont('Comic Sans MS', 56)
					text = font.render('Your score:', False, (255, 255, 255))
					window_sfc.blit(text,(300,650))
					text = font.render(str(ship.ship['score']), False, (255, 255, 255))
					window_sfc.blit(text,(600,650))
					
				elif ship.ship['ending'] == 3:
					window_sfc.blit(ship.ship["ed3"], (0,0))
					font = pygame.font.SysFont('Comic Sans MS', 56)
					text = font.render('Your score:', False, (255, 255, 255))
					window_sfc.blit(text,(300,650))
					text = font.render(str(ship.ship['score']), False, (255, 255, 255))
					window_sfc.blit(text,(600,650))
					
		elif menu.menu["is_exit"]:
			closed_flag = True

		pygame.display.update()
		clock.tick(frame_rate)

		
if __name__ == "__main__":
	main()
