import pygame
import sys
from Settings import *
from Sprites import*
from os import path
from tilemap import *

# HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500,100)
        self.load_data()
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')
        self.map = TiledMap(path.join(map_folder, 'level1.tmx'))
        self.Map_image = self.map.make_map()
        self.map_rect = self.Map_image.get_rect()
        self.player_image = pygame.image.load(path.join(img_folder, PLAYER_IMAGE)).convert_alpha()
        self.wall_image = pygame.image.load(path.join(img_folder, WALL_IMAGE)).convert_alpha()
        self.wall_image = pg.transform.scale(self.wall_image, (TILESIZE,TILESIZE))
        self.Mob_image = pg.image.load(path.join(img_folder, MOB_IMAGE)).convert_alpha()
        self.Bullet_image = pg.image.load(path.join(img_folder, BULLET)).convert_alpha()
        self.Muzzle_images = []
        for images in MUZZLE_IMAGES:
            self.Muzzle_images.append(pygame.image.load(path.join(img_folder, images)).convert_alpha())

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        # here lies code we dont use anymore :( rip old map system 2022-2022
        #for row, tiles in enumerate(self.map.data):
            #for col, tile in enumerate(tiles):
                #if tile == '1':
                    #Wall(self, col, row)
                #if tile == 'P':
                    #self.player = Player(self,row,col)
                #if tile == 'M':
                    #Mob(self,col,row) 
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'Player':
                self.player = Player(self,tile_object.x,tile_object.y)
            if tile_object.name == 'Zombie':
                Mob(self,tile_object.x,tile_object.y)      
            if tile_object.name == 'wall':
                Obstacle(self,tile_object.x,tile_object.y,tile_object.width
                ,tile_object.height)         
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False      
                    

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_with_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= GUN_DAMAGE
            hit.vel = vec(0, 0)


    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.display, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.display, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.display.blit(self.Map_image,self.camera.apply_rect(self.map_rect))
        #self.display.fill(BGCOLOR)
        #self.display.fill(BGCOLOR)
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.display.blit(sprite.image, self.camera.apply(sprite))
        if self.draw_debug:
                pg.draw.rect(self.display, GREEN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.display, GREEN, self.camera.apply_rect(wall.rect), 1)    
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        # HUD functions
        draw_player_health(self.display, 10, 10, self.player.health / PLAYER_HEALTH)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug        

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()