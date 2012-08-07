#-*- coding: utf-8 -*-
import pyglet
from ftl.util import pixelate
import json
from math import floor


class World(object):
    tilesize = 32

    def __init__(self, world_file):
        """ Build a new tileset from an image file """
        self.world_file = world_file
        self.load_world()

    def load_world(self):
        self.sprite_batch = pyglet.graphics.Batch()
        self.sprites = []
        self.tiles = []
        with open(self.world_file, 'rb') as fp:
            self.mapdata = json.load(fp)
            self.mapdata['map'] = self.mapdata['map'][::-1]
        self.load_tiles()

    def load_tiles(self):
        tileset = self.mapdata['tileset']
        grid = pyglet.image.ImageGrid(pyglet.resource.image(tileset), 16, 16)
        for row in range(16):
            for col in range(16):
                tile = grid[(15-row)*16 + col]
                tile.width = tile.height = self.tilesize
                self.tiles.append(tile)
                pixelate(grid[(15-row)*16 + col])

        for row, cols in enumerate(self.mapdata['map']):
            for col, value in enumerate(cols):
                sprite = pyglet.sprite.Sprite(self.tiles[value],
                                              x = col*self.tilesize,
                                              y = row*self.tilesize,
                                              batch=self.sprite_batch)
                self.sprites.append(sprite)

    def get_tile_at(self, x, y):
        tx = int(floor(x/self.tilesize))
        ty = int(floor(y/self.tilesize))
        return self.mapdata['map'][ty][tx]

    def __getitem__(self, n):
        return self.tiles[n[0]*16+n[1]]

    def draw(self):
        self.sprite_batch.draw()

