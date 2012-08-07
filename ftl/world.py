#-*- coding: utf-8 -*-
import pyglet
from ftl.util import pixelate
import json
from math import floor


class World(object):

    tilesize = 32

    def __init__(self, game, world_file):
        """ Build a new tileset from an image file """
        self.game = game
        self.world_file = world_file
        self.sprite_batch = game.floor_batch
        self.sprites = {}
        self.load_world()
        self.load_tileset()

    def load_world(self):
        with open(self.world_file, 'rb') as fp:
            self.mapdata = json.load(fp)
            self.mapdata['map'] = self.mapdata['map'][::-1]

    def load_tileset(self):
        pyglet.resource.reindex()
        img = self.game.load_image(self.mapdata['tileset'])
        scale = float(self.tilesize) / img.width * 16
        grid = pyglet.image.ImageGrid(img, 16, 16)
        map(pixelate, grid)
        self.tileset = [grid[(15-row)*16 + col] for row in range(16) for col in range(16)]

        for row, cols in enumerate(self.mapdata['map']):
            for col, value in enumerate(cols):
                tile_image = self.tileset[value]
                if (row, col) in self.sprites:
                    self.sprites[row, col].image = tile_image
                else:
                    self.sprites[row, col] = pyglet.sprite.Sprite(
                                              tile_image,
                                              x = col*self.tilesize,
                                              y = row*self.tilesize,
                                              batch=self.sprite_batch)
                self.sprites[row, col].scale = scale

    def get_tile_at(self, x, y):
        tx = int(floor(x/self.tilesize))
        ty = int(floor(y/self.tilesize))
        return self.mapdata['map'][ty][tx]

    def draw(self):
        self.sprite_batch.draw()

