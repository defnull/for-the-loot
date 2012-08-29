import pyglet, random, math
from ftl.util import pixelate, center_image, lazy_attribute, cached_property
from pyglet.image import Animation




class Fireball(object):
    def __init__(self, game, pos, vec, livetime):
        self.game = game
        self.pos = pos
        self.vec = vec
        self.livetime = livetime

        self.sprite.position = pos
        self.sprite.rotation = math.atan2(vec[0], vec[1]) * 180 / math.pi - 90
        self.sprite.batch = game.effect_batch
        self.game.tick_callbacks.append(self.tick_fireball)

    @cached_property
    def ani_fireball(self):
        img  = self.game.load_image('firebolt.png')
        grid = list(pyglet.image.ImageGrid(img, 1, 5))
        [(pixelate(g), center_image(g)) for g in grid]
        return Animation.from_image_sequence(grid, 0.05)

    @cached_property
    def ani_smoke(self):
        img  = self.game.load_image('smoke.png')
        grid = list(pyglet.image.ImageGrid(img, 1, 8))
        [(pixelate(g), center_image(g)) for g in grid]
        return Animation.from_image_sequence(grid, 0.1, loop=False)

    @cached_property
    def sprite(self):
        sprite = pyglet.sprite.Sprite(self.ani_fireball, batch=self.game.effect_batch)
        sprite.scale = 2
        return sprite

    def tick_fireball(self, dt):
        self.livetime -= dt
        x,y = self.sprite.position
        dx, dy = self.vec
        dx *= dt
        dy *= dt

        if self.livetime <= 0 or self.game.world.wall_clip(x,y,dx,dy):
            self.livetime = 0.0
            self.sprite.image = self.ani_smoke
            self.sprite.rotation = 0
            self.vec = self.vec[0]*.2, 30
            self.game.tick_callbacks.remove(self.tick_fireball)
            self.game.tick_callbacks.append(self.tick_smoke)
        else:
            self.sprite.x += dx
            self.sprite.y += dy

    def tick_smoke(self, dt):
        self.livetime -= dt
        if self.livetime <= -1:
            self.game.tick_callbacks.remove(self.tick_smoke)
            self.sprite.delete()




class Entity(object):
    """A thing."""
    def __init__(self, game):
        self.game = game


class Enemy(Entity):
    speed = 80
    def __init__(self, game):
        Entity.__init__(self, game)
        self.position  = [16,16]

        img = self.game.load_image('player.png')
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

        self.sprite = pyglet.sprite.Sprite(self.ani_standing['down'], batch=self.game.object_batch)
        self.sprite.position = self.position
        self.moves = False
        self.game.tick_callbacks.append(self.on_tick)

    def on_tick(self, dt):
        x,y = self.position
        self.position = (x+(0.5-random.random())*self.speed*dt,
                         y+(0.5-random.random())*self.speed*dt)
        self.sprite.position = self.position



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
        img = self.game.load_image('player.png')
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

        self.sprite = pyglet.sprite.Sprite(self.ani_standing['down'], batch=self.game.object_batch)
        self.sprite.position = self.position
        self.moves = False

    def move(self, dx, dy):
        if dx or dy:
            absdy = abs(dy)
            if dx > absdy:     face = 'right'
            elif -dx > absdy:  face = 'left'
            elif dy > 0:       face = 'up'
            elif dy < 0:       face = 'down'

            x,y = self.position
            s = 10
            for cx, cy in ((s,s),(-s,s),(s,-s),(-s,-s)):
                if self.game.world.wall_clip(x+cx,y+cy,dx,dy):
                    if self.moving:
                        self.sprite.image = self.ani_standing[self.face]
                        self.face = face
                        self.moving = False
                    return

            if face != self.face or not self.moving:
                self.sprite.image = self.ani_running[face]
                self.face = face

            self.moving = True
            self.position[0] += dx
            self.position[1] += dy
            self.sprite.position = map(int, self.position)
            self.last_move = [dx,dy]
        else:
            if self.moving:
                self.sprite.image = self.ani_standing[self.face]
                self.moving = False


