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
        self.anims = []
        for row in range(4):
            frames = [pyglet.image.AnimationFrame(grid[row*4+col], 0.1) for col in range(4)]
            self.anims.append(pyglet.sprite.Sprite(pyglet.image.Animation(frames)))
        self.sprite = self.anims[0]
        self.position = (0,0)
        self.sprite.position = self.position

    def draw(self):
        self.sprite.draw()
