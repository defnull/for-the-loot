import pyglet, random
from pyglet.gl import *

class Game(object):
    def __init__(self):
        pass

    def setup(self):
        pyglet.resource.path = ['./resources']
        pyglet.resource.reindex()
        self.window = pyglet.window.Window(800, 600)
        self.window.set_handler('on_draw', self.on_draw)
        self.window.set_vsync(True)
        self.fps_display = pyglet.clock.ClockDisplay()

        self.backgr_batch = pyglet.graphics.Batch()
        self.object_batch = pyglet.graphics.Batch()
        self.effect_batch = pyglet.graphics.Batch()
        self.window_batch = pyglet.graphics.Batch()

        self.window_offset = (0,0,0.0)

        pyglet.clock.schedule_interval(self.on_tick, 1.0/60)

    def start(self):
        self.setup()
        pyglet.app.run()

    def on_draw(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(*self.window_offset)
        #glScalef(self.zoom, self.zoom, 1.0)
        #glTranslatef(-t.x, -t.y, 0.0)

        self.window.clear()
        self.backgr_batch.draw()
        self.object_batch.draw()
        self.effect_batch.draw()
        self.window_batch.draw()
        self.fps_display.draw()

    def on_tick(self, dt):
        pass

def main():
    Game().start()

if __name__ == '__main__':
    main()


