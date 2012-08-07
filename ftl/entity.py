import pyglet, random, math
from ftl.util import pixelate, center_image
from pyglet.image import Animation

class Entity(object):
    """A thing."""
    def __init__(self, game):
        self.game = game

    def draw(self):
        pass


class Fireball(object):
    def __init__(self, game, pos, vec, livetime):
        self.game = game
        self.pos = pos
        self.vec = vec
        self.livetime = livetime
        img  = pyglet.resource.image('firebolt.png')
        grid = pyglet.image.ImageGrid(img, 1, 5)
        map(center_image, grid)
        ani  = Animation.from_image_sequence(grid, 0.05)

        img  = pyglet.resource.image('smoke.png')
        grid = pyglet.image.ImageGrid(img, 1, 8)
        map(center_image, grid)
        self.smoke  = Animation.from_image_sequence(grid, 0.1, loop=False)
        
        self.sprite = pyglet.sprite.Sprite(ani)
        self.sprite.position = pos
        self.sprite.rotation = 90 + math.atan2(vec[0], vec[1]) * 180 / math.pi
        self.sprite.scale = 2
        self.sprite.batch = game.effect_batch
        game.tick_callbacks.append(self.on_tick)

    def on_tick(self, dt):
        self.sprite.x += dt*self.vec[0]
        self.sprite.y += dt*self.vec[1]
        self.livetime -= dt
        if self.livetime <= 0 and self.smoke:
            self.sprite.image = self.smoke
            self.sprite.rotation = 0
            self.vec = self.vec[0]*.2,  30
            self.smoke = False
        if self.livetime <= -1:
            self.sprite.delete()
            self.game.tick_callbacks.remove(self.on_tick)

            

        


class Player(Entity):
    """The player sprite"""

    speed = 100

    def __init__(self, game):
        Entity.__init__(self, game)
        self.position  = [16,16]
        self.last_move = [0,0]
        self.face      = 'down'
        self.moving    = False
        self.load_textures()

    def load_textures(self):
        img = pyglet.resource.image('player.png')
        grid = pyglet.image.ImageGrid(img, 4, 4)
        for img in grid:
            pixelate(img)
            img.width  *= 2
            img.height *= 2
            center_image(img, 0.5, 0.3)

        self.ani_running = {}
        self.ani_standing = {}
        for row, name in enumerate(('up','right','left','down')):
            ani_run   = [grid[row*4+col] for col in (2,3,2,1)]
            img_stand = grid[row*4+0]
            self.ani_running[name] = Animation.from_image_sequence(ani_run, 0.15)
            self.ani_standing[name] = img_stand

        self.sprite = pyglet.sprite.Sprite(self.ani_standing['down'])
        self.sprite.position = self.position
        self.moves = False

    def move(self, dx, dy):
        if dx or dy:
            self.position[0] += dx
            self.position[1] += dy
            absdy = abs(dy)
            if dx > absdy:     face = 'right'
            elif -dx > absdy:  face = 'left'
            elif dy > 0:       face = 'up'
            elif dy < 0:       face = 'down'
            if face != self.face:
                self.sprite.image = self.ani_running[face]
                self.face = face
            self.sprite.position = map(int, self.position)
            self.last_move = [dx,dy]
            self.moving = True
        else:
            if self.moving:
                self.sprite.image = self.ani_standing[self.face]
                self.moving = False

    def draw(self):
        self.sprite.draw()

