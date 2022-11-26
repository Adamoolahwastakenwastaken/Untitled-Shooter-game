import pygame
from Settings import *
import pytmx

def collide_with_hit_rect(one,two):
    return one.hit_rect.colliderect(two.rect)
class Map:
    def __init__(self,fileName):
        self.data = []
        with open(fileName, 'rt') as f:
            for line in f:
                self.data.append(line)
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data) 
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
class Camera:
    def __init__(self,width,height):
        self.camera = pygame.Rect(0,0,width,height)
        self.width = width
        self.height = height
    def apply(self,entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self,rect):
        return rect.move(self.camera.topleft)    
    def update(self,target):
        x = -target.rect.centerx + int(WIDTH/2)
        y = -target.rect.centery + int(HEIGHT /2)
        # limit Camera Bounds
        x = min(0,x) # left side
        y = min(0,y) # top side
        x = max(-(self.width - WIDTH),x)
        y = max(-(self.height - HEIGHT),y)
        self.camera = pygame.Rect(x,y,self.width,self.height)
class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pygame.Surface((self.width,self.height))
        self.render(temp_surface)
        return temp_surface
