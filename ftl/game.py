import pyglet, random, os
from pyglet.gl import *

from ftl.entity import Player, Fireball, Enemy

from pyglet.window import key

from ftl.world import World
from ftl.util import normvec


class Game(object):
    def __init__(self):
        self.tick_callbacks = []
        self.camera_position = [0, 0, -512]

    def start(self):
        self.window = pyglet.window.Window(800, 600)
        self.window.set_vsync(True)

        self.floor_batch  = pyglet.graphics.Batch()
        self.object_batch = pyglet.graphics.Batch()
        self.effect_batch = pyglet.graphics.Batch()
        self.window_batch = pyglet.graphics.Batch()
        self.status_label = pyglet.text.Label('Loading...', font_name='sans',
                                              font_size=8, x=10, y=10,
                                              batch=self.window_batch)

        self.fps_display  = pyglet.clock.ClockDisplay()
        self.fps_display.label.batch = self.window_batch
        self.window.set_handler('on_draw', self.on_draw)

        pyglet.clock.schedule_once(self.setup_resources, 0)
        pyglet.clock.schedule_once(self.setup_controls, 0)
        pyglet.clock.schedule_once(self.setup_world, 0)
        pyglet.clock.schedule_once(self.setup_player, 0)
        pyglet.clock.schedule_once(self.setup_gameloop, 0)
        pyglet.app.run()

    def setup_resources(self, dt):
        self.notice('Indexing resources...')
        self.loader = pyglet.resource.Loader(
            path = ['./resources'],
            script_home=os.path.abspath(os.path.dirname(__file__)))
        self.load_image = self.loader.image
        self.loader.reindex()

    def setup_controls(self, dt):
        self.notice('Initializing controls...')
        self.keys = pyglet.window.key.KeyStateHandler()
        self.window.push_handlers(self.keys)

    def setup_world(self, dt):
        self.notice('Loading world...')
        self.world = World(self, './ftl/resources/world.json')

    def setup_player(self, dt):
        self.notice('Loading player...')
        self.player = Player(self)
        self.center_screen()

    def setup_gameloop(self, dt):
        self.notice('Loading game state...')
        pyglet.clock.schedule_interval(self.on_tick, 1.0/60)

    def notice(self, msg):
        self.status_label.text = msg

    def on_draw(self):
        self.window.clear()
        w,h = self.window.width, self.window.height

        # Move camera above character
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(*map(int, self.camera_position))

        # Enable perspective projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, float(w)/h, 0.1, 100000)

        self.floor_batch.draw()

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-w/2, w/2, -h/2, h/2, -10000, 10000)

        self.object_batch.draw()
        self.effect_batch.draw()

        glLoadIdentity()
        self.window_batch.draw()

    def on_tick(self, dt):
        dx, dy = 0.0, 0.0
        if self.keys[key.RIGHT]: dx += self.player.speed
        if self.keys[key.LEFT]:  dx -= self.player.speed
        if self.keys[key.UP]:    dy += self.player.speed
        if self.keys[key.DOWN]:  dy -= self.player.speed
        if self.keys[key.PLUS]:
            self.camera_position[2] += 1
        if self.keys[key.MINUS]:
            self.camera_position[2] -= 1

        if self.keys[key.E]:
            e = Enemy(self)
        if self.keys[key.D]:
            import pdb; pdb.set_trace()

        if dx and dy:
            dx *= 0.7071067811865476 #(.5**.5)
            dy *= 0.7071067811865476

        self.player.move(dx*dt, dy*dt)

        if self.keys[key.SPACE]:
            bx, by = self.player.last_move
            if bx or by:
                bx, by = normvec((bx, by), 200)
                bx += (0.5 - random.random()) * 100
                by += (0.5 - random.random()) * 100
                x, y = self.player.position
                if self.player.face == 'up':     y += 10
                if self.player.face == 'down':   y -= 10
                if self.player.face == 'right':  x += 15
                if self.player.face == 'left':   x -= 15
                bullet = Fireball(self, (x,y+10), (bx, by), 1.5)

        if dx or dy:
            self.center_screen()

        for callback in self.tick_callbacks:
            callback(dt)

    def center_screen(self):
        ''' Change window offset so the player sprite is in the middle of
            the visible screen. '''
        h, w = self.window.height, self.window.width
        wx, wy, wz = self.camera_position
        px, py = self.player.position

        # World position in center of screen
        cx, cy = -wx, -wy

        # Desired world position in center of screen
        cx = px - max(-30, min(30, px-cx))
        cy = py - max(-30, min(30, py-cy))

        self.camera_position = [-cx, -cy, wz]

def main():
    Game().start()

if __name__ == '__main__':
    main()


