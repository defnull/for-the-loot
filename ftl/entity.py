import pyglet, random, math
from ftl.util import pixelate, center_image, lazy_attribute, cached_property
from ftl.physics import point_near_line
from pyglet.image import Animation
from ftl.util import normvec

class Entity(object):
    ''' Subclasses should implement tick()'''

    game = None

    def __init__(self, game):
        self.game = game
        self.age = 0.0

    def __hash__(self): return id(self)

    def destroy(self):
        ''' Calls self.game.remove_entity(self) '''
        self.game.remove_entity(self)
    
    def tick(self, dt):
        self.age += dt
        self.on_tick(dt)

    def on_setup(self, *a, **ka):
        ''' Called on entity creation. '''
    
    def on_tick(self, dt):
        ''' Called on every tick as long as the entity belongs to a game. '''

    def on_remove(self):
        ''' Called when the entity is removed from a game. '''




class Fireball(Entity):
    maxage = 2
    hitsize = 1

    def on_setup(self, x, y, dx, dy):
        self.position = [x, y]
        self.speed = 100 + 100 * random.random()
        self.direction = [dx, dy]
        self.movement = normvec((dx, dy), self.speed)
        self.rotation = math.atan2(dx, dy) * 180 / math.pi - 90
        self.sprite = self.make_sprite()

    def on_remove(self):
        self.sprite.delete()

    def on_tick(self, dt):
        x, y = self.position
        dx, dy = self.movement
        dx *= dt
        dy *= dt
        self.position[0] += dx
        self.position[1] += dy
        self.sprite.position = map(int, self.position)

        if self.age > self.maxage:
            self.explode()
            return

        # Fireball mode
        for tile, cx, cy in self.game.world.wall_walk(x,y,dx,dy):
            if tile.is_wall:
                self.position = [cx, cy]
                self.sprite.position = map(int, self.position)
                self.explode()
                return

        nearest = None
        distance = 9999999
        for enemy in self.game.enemies:
            cx, cy, dist = point_near_line(x, y, x+dx, y+dy, *enemy.position)
            if dist < distance and dist < enemy.hitsize+self.hitsize:
                nearest = enemy
                distance = dist
                self.position = [cx, cy]
        if nearest:
            self.sprite.position = map(int, self.position)
            self.explode()
            return

    def make_sprite(self):
        img  = self.game.load_image('firebolt.png')
        grid = list(pyglet.image.ImageGrid(img, 1, 5))
        [(pixelate(g), center_image(g)) for g in grid]
        ani = Animation.from_image_sequence(grid, 0.05)
        sprite = pyglet.sprite.Sprite(ani, batch=self.game.effect_batch)
        sprite.position = map(int, self.position)
        sprite.rotation = self.rotation
        sprite.scale = 2
        return sprite

    def explode(self):
        x,y = self.position
        kill = []
        for enemy in self.game.enemies:
            ex, ey = enemy.position
            dist = ((ex-x)**2 + (ey-y)**2) ** 0.5
            if dist < enemy.hitsize+self.hitsize:
                kill.append(enemy)
        for e in kill:
            e.kill()

        self.game.create_entity(Smoke, *self.position)
        self.destroy()



class Smoke(Entity):

    def on_setup(self, x, y):
        self.position = [x, y]
        self.age = 0.0
        self.sprite = self.make_sprite()

    def on_remove(self):
        self.sprite.delete()

    def make_sprite(self):
        img  = self.game.load_image('smoke.png')
        grid = list(pyglet.image.ImageGrid(img, 1, 8))
        [(pixelate(g), center_image(g)) for g in grid]
        ani = Animation.from_image_sequence(grid, 0.1, loop=False)
        sprite = pyglet.sprite.Sprite(ani, batch=self.game.effect_batch)
        sprite.position = map(int, self.position)
        sprite.scale = 2
        return sprite

    def on_tick(self, dt):
        if self.age > 0.9:
            self.destroy()
            return

        self.position[1] += dt*5
        self.sprite.position = map(int, self.position)




class Enemy(Entity):
    hitsize = 10
    speed = 80
    dead = False

    def on_setup(self, x, y):
        self.position  = [x, y]

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

    def on_tick(self, dt):
        x,y = self.position
        self.position = (x+(0.5-random.random())*self.speed*dt,
                         y+(0.5-random.random())*self.speed*dt)
        self.sprite.position = map(int, self.position)
        if self.dead:
            self.sprite.rotation += dt * 90
            if self.age > self.maxage:
                self.destroy()

    def on_remove(self):
        self.game.enemies.remove(self)
        self.sprite.delete()

    def kill(self):
        self.dead = True
        self.hitsize = 0
        self.maxage = self.age + 1


class Player(Entity):
    """The player sprite"""

    speed = 100

    def on_setup(self):
        self.position  = [16.0,16.0]
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
            ani_run   = [grid[row*4+col] for col in (1,2,3,2)]
            img_stand = grid[row*4+0]
            self.ani_running[name] = Animation.from_image_sequence(ani_run, 0.15)
            self.ani_standing[name] = img_stand

        self.sprite = pyglet.sprite.Sprite(self.ani_standing['down'], batch=self.game.object_batch)
        self.sprite.position = self.position
        self.moves = False

    def move(self, dx, dy):
        if dx or dy:
            dx *= self.speed
            dy *= self.speed
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

    def on_remove(self):
        self.sprite.delete()
