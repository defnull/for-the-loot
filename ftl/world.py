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
        self.tiles = {}
        self.load_world()
        self.load_tileset()

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
                self.tiles[row, col] = Tile(self, row, col, value)

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


