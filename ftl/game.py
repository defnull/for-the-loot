import pyglet, random, os
from pyglet.gl import *

from ftl.entity import Player

from pyglet.window import key

class Game(object):
    def __init__(self):
        pass

    def setup(self):
        pyglet.resource.path = [os.path.join(os.path.dirname(__file__), 'resources')]
        pyglet.resource.reindex()
        self.window = pyglet.window.Window(800, 600)
        self.window.set_handler('on_draw', self.on_draw)
        self.window.set_vsync(True)

        self.debug_label = pyglet.text.Label('debug', font_name='sans', font_size=8, x=10, y=10)

        self.keys = pyglet.window.key.KeyStateHandler()
        self.window.push_handlers(self.keys)

        self.fps_display  = pyglet.clock.ClockDisplay()

        self.player = Player(self)

        self.backgr_batch = pyglet.graphics.Batch()
        self.object_batch = pyglet.graphics.Batch()
        self.effect_batch = pyglet.graphics.Batch()
        self.window_batch = pyglet.graphics.Batch()
        self.debug_label.batch = self.window_batch

        self.window_offset = (0,0,0.0)

        from ftl.tiles import World
        self.world = World((
            (0,0,0,0,0),
            (0,1,2,1,0),
            (0,2,3,2,0),
            (0,1,2,1,0),
            (0,0,0,0,0),
        ))

        pyglet.clock.schedule_interval(self.on_tick, 1.0/60)

    def start(self):
        self.setup()
        pyglet.app.run()

    def on_draw(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        w,h = self.window.width, self.window.height
        x,y = self.player.position
        glTranslatef(int(-x+w/2), int(-y+h/2), 0.0)
        #glScalef(self.zoom, self.zoom, 1.0)
        #glTranslatef(-t.x, -t.y, 0.0)

        self.debug(x, y, self.player.moves)

        self.window.clear()
        self.world.draw()
        self.backgr_batch.draw()
        self.object_batch.draw()
        self.player.draw()
        self.effect_batch.draw()
        glLoadIdentity()
        self.window_batch.draw()
        self.fps_display.draw()

    def on_tick(self, dt):
        dx, dy = 0.0, 0.0
        if self.keys[key.RIGHT]:      dx += dt*100
        if self.keys[key.LEFT]:       dx -= dt*100
        if self.keys[key.UP]:         dy += dt*100
        if self.keys[key.DOWN]:       dy -= dt*100
        self.player.move(dx, dy)

    def debug(self, *a):
        self.debug_label.text = ', '.join(map(repr, a))

def main():
    Game().start()

if __name__ == '__main__':
    main()


