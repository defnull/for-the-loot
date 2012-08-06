import pyglet

class Entity(object):
    """A thing."""
    def __init__(self, game):
        self.game = game

    def draw(self):
        pass


class Player(Entity):
    """The player sprite"""

    def __init__(self, game):
        Entity.__init__(self, game)
        grid = pyglet.image.ImageGrid(pyglet.resource.image('player.png'), 4, 4)
        for img in grid:
            img.height = img.width = 64
            img.anchor_x = img.width/2
            img.anchor_y = img.height/3

        self.sprites = []
        for row in range(4):
            frames = []
            standing = grid[row*4]
            for col in range(4):
                frame = pyglet.image.AnimationFrame(grid[row*4+col], 0.15)
                frames.append(frame)
            anim = pyglet.image.Animation(frames)
            self.sprites.append(map(pyglet.sprite.Sprite, (standing, anim)))
        self.set_sprite('down')
        self.position = [0,0]
        self.sprite.position = self.position
        self.moves = False

    def set_sprite(self, mode, move=False):
        if   mode == 'down':
            self.sprite = self.sprites[3][1 if move else 0]
        elif mode == 'left':
            self.sprite = self.sprites[2][1 if move else 0]
        elif mode == 'right':
            self.sprite = self.sprites[1][1 if move else 0]
        elif mode == 'up':
            self.sprite = self.sprites[0][1 if move else 0]

    def move(self, dx, dy):
        if dx or dy:
            self.position[0] += dx
            self.position[1] += dy
            absdy = abs(dy)
            if dx > absdy:
                self.moves = 'right'
                self.set_sprite('right', True)
            elif -dx > absdy:
                self.moves = 'left'
                self.set_sprite('left', True)
            elif dy > 0:
                self.moves = 'up'
                self.set_sprite('up', True)
            elif dy < 0:
                self.moves = 'down'
                self.set_sprite('down', True)
        else:
            if self.moves:
                self.set_sprite(self.moves, False)
                self.moves = False
        self.sprite.position = map(int, self.position)

    def draw(self):
        self.sprite.draw()

