
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
        self.img = pyglet.image.load('kitten.png')
        self.sprite = pyglet.sprite.Sprite(self.img)

    def draw(self):
        self.sprite.draw()
