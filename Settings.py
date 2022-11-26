import pygame
vec = pygame.math.Vector2
# some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106,55,5)

# game settings
WIDTH = 1024   
HEIGHT = 768  
FPS = 60
TITLE = "Untitled Zombie Game"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#player settings
PLAYERSPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_IMAGE = "manBlue_gun.png"
PLAYER_HIT_RECT = pygame.Rect(0,0,35,35)
WALL_IMAGE = "tileGreen_39.png"
BARREL_OFFSET = vec(30,10)
PLAYER_HEALTH = 100

# Gun Settings
BULLET = "Bullet.png"
BULLET_SPEED = 500
BULLET_LIFE = 1000
BULLET_RATE = 300
KICK_BACK = 200
GUN_SPREAD = 5
GUN_DAMAGE = 13

# Mob Settings
MOB_IMAGE = "zoimbie1_hold.png"
MOB_SPEED = 150
MOB_HIT_RECT = pygame.Rect(0,0,35,35)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
# effects
MUZZLE_IMAGES  = ["whitePuff15.png", "whitePuff16.png", "whitePuff17.png", "whitePuff18.png"]
MUZZLE_DURATION = 50

#LAYERS
WALL_LAYER = 1
PLAYER_LAYER =  2 
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4