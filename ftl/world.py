#-*- coding: utf-8 -*-
import pyglet
from ftl.util import pixelate
import json
from math import floor

from ftl.physics import grid_walk
from random import random as rand


class World(object):

    tilesize = 32

    def __init__(self, game, world_file):
        """ Build a new tileset from an image file """
        self.game = game
        self.world_file  = world_file
        self.floor_batch = game.floor_batch
        self.wall_batch  = game.wall_batch
        self.lightmap = LightMap()
        self.tiles = {}
        self.load_world()
        self.load_tileset()
        self.player_light = self.lightmap.add_light(0,0,15)

    def load_world(self):
        with open(self.world_file, 'r') as fp:
            self.mapdata = json.load(fp)
            self.mapdata['map'] = self.mapdata['map'][::-1]

    def load_tileset(self):
        pyglet.resource.reindex()
        img = self.game.load_image(self.mapdata['tileset'])
        pixelate(img)
        scale = float(self.tilesize) / img.width * 16
        grid = pyglet.image.ImageGrid(img, 16, 16)
        map(pixelate, grid)
        self.tileset = [grid[(15-row)*16 + col] for row in range(16) for col in range(16)]

        for row, cols in enumerate(self.mapdata['map']):
            for col, value in enumerate(cols):
                tile = self.tiles[row, col] = Tile(self, row, col, value)
                if tile.is_wall:
                    self.lightmap.set_wall(col, row)

    def wall_walk(self, x, y, dx, dy):
        f = 1.0/self.tilesize
        for gx, gy, t, hv in grid_walk(x*f, y*f, (x+dx)*f, (y+dy)*f):
            try:
                yield self.tiles[gy, gx], x+dx*t, y+dy*t
            except KeyError:
                return

    def wall_clip(self, x, y, dx, dy):
        f = 1.0/self.tilesize
        for gx, gy, t, hv in grid_walk(x*f, y*f, (x+dx)*f, (y+dy)*f):
            try:
                if self.tiles[gy, gx].is_wall:
                    return True
            except KeyError:
                return True
        return False

    def draw(self):
        self.sprite_batch.draw()

    def light(self, x, y):
        self.player_light = self.lightmap.change_light(self.player_light, float(x)/32, float(y)/32, 6)
        for tile in self.tiles.values():
            tx, ty = float(tile.col), float(tile.row)
            lv = (self.lightmap.compute(tx+.25, ty+.75),
                  self.lightmap.compute(tx+.75, ty+.75),
                  self.lightmap.compute(tx+.75, ty+.25),
                  self.lightmap.compute(tx+.25, ty+.25))
            lv = [int(15+sum(lv)/4*250)]*4
            tile.shade(*lv)


class LightMap(object):
    def __init__(self):
        self.walls = set()
        self.lights = set()
        self.light_values = {}

    def set_wall(self, x, y):
        self.walls.add((x,y))

    def set_floor(self, x, y):
        self.walls.discard((x,y))

    def add_light(self, x, y, value):
        light = (x,y,value)
        self.lights.add(light)
        return light

    def change_light(self, orig, x, y, value):
        light = (x,y,value)
        self.lights.discard(orig)
        self.lights.add(light)
        return light

    def remove_light(self, x, y, value):
        light = (x,y,value)
        self.lights.remove(light)

    def compute(self, x, y):
        light = 0.0
        def hits_wall(x, y):
            for gx, gy, t, hv in grid_walk(x, y, lx, ly):
                if t and (gx, gy) in self.walls:
                    return True

        for lx, ly, lv in self.lights:
            d = ((x-lx)**2 + (y-ly)**2) ** .5
            if d>lv: continue

            lv = 1-d/lv
            if lv < light: continue
            if hits_wall(x, y): continue

            if lv > light: light = lv
            if light >= 0.95: return 1.0
        return light




class Tile(object):
    def __init__(self, world, row, col, value):
        self.world = world
        self.col = col
        self.row = row
        self.value = value
        self.image = self.world.tileset[self.value]
        self.sprite = pyglet.sprite.Sprite(
            self.world.tileset[self.value],
            x = self.col*self.world.tilesize,
            y = self.row*self.world.tilesize)
        self.sprite.scale = float(self.world.tilesize) / self.image.width

        self.is_wall = 16 <= value < 32
        self.sprite.batch = self.world.wall_batch if self.is_wall else self.world.floor_batch

    def shade(self, tl, tr, br, bl):
        for index, shade in enumerate((tl, tr, br, bl)):
            self.sprite._vertex_list.colors[index*4:index*4+3] = [shade, shade, shade]


