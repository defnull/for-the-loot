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
            img.anchor_x = img.width/2
            img.anchor_y = img.height/3

        self.anims = []
        for row in range(4):
            frames = []
            for col in range(4):
                frame = pyglet.image.AnimationFrame(grid[row*4+col], 0.1)
                frames.append(frame)
            anim = pyglet.image.Animation(frames)
            self.anims.append(pyglet.sprite.Sprite(anim))
        self.sprite = self.anims[0]
        self.position = (0,0)
        self.sprite.position = self.position


    def draw(self):
        self.sprite.draw()
