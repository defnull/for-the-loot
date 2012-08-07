import pyglet, random, os
from pyglet.gl import *

from ftl.entity import Player

from pyglet.window import key

from ftl.world import World


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

        self.window_offset = (0, 0, 0.0)

        pyglet.clock.schedule_interval(self.on_tick, 1.0/60)
        self.center_screen()

        self.world = World('./ftl/resources/world.json')


    def start(self):
        self.setup()
        pyglet.app.run()

    def on_draw(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        w,h = self.window.width, self.window.height
        glTranslatef(*map(int,self.window_offset))
        #glScalef(self.zoom, self.zoom, 1.0)
        #glTranslatef(-t.x, -t.y, 0.0)

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
        if self.keys[key.RIGHT]: dx += self.player.speed
        if self.keys[key.LEFT]:  dx -= self.player.speed
        if self.keys[key.UP]:    dy += self.player.speed
        if self.keys[key.DOWN]:  dy -= self.player.speed
        if self.keys[key.D]:
            import pdb; pdb.set_trace()

        if dx and dy:
            dx *= 0.7071067811865476 #(.5**.5)
            dy *= 0.7071067811865476

        self.player.move(dx*dt, dy*dt)

        if dx or dy:
            self.center_screen()

    def center_screen(self):
        ''' Change window offset so the player sprite is in the middle of
            the visible screen. '''
        h, w = self.window.height, self.window.width
        wx, wy = self.window_offset[:2]
        px, py = self.player.position

        # World position in center of screen
        cx, cy = -wx+w/2, -wy+h/2

        # Desired world position in center of screen
        cx = px - max(-30, min(30, px-cx))
        cy = py - max(-30, min(30, py-cy))

        self.window_offset = -cx+w/2, -cy+h/2, 0.0

    def debug(self, *a):
        self.debug_label.text = ', '.join(map(repr, a))

def main():
    Game().start()

if __name__ == '__main__':
    main()


