import pyglet, random, os
from pyglet.gl import *

from ftl.entity import Player, Fireball, Enemy

from pyglet.window import key

from ftl.world import World
from ftl.util import normvec


class LazySet(set):
    ''' Like set(), but the add() and remove() actions are deferred until
        sync() is called or an iterator is created. This allows modification
        during iteration. Useful for callback lists where callbacks remove
        temselve or add new callbacks. '''

    def __init__(self):
        self.__remove = set()
        self.__add = set()
        self.remove = self.__remove.add
        self.add    = self.__add.add

    def __iter__(self):
        self.sync()
        removed = self.__remove
        for x in set.__iter__(self):
            if x not in removed:
                yield x
   
    def sync(self):
        self.update(self.__add)
        self -= self.__remove
        self.__add.clear()
        self.__remove.clear()
        return set.__iter__(self)



class Game(object):
    def __init__(self):
        self.camera_position = [0, 0, -512]
        self.enemies  = LazySet()
        self.entities = LazySet()
        self.tick_callbacks = LazySet()

    def create_entity(self, klass, *a, **ka):
        entity = klass(self) 
        entity.on_setup(*a, **ka)
        self.entities.add(entity)
        return entity

    def remove_entity(self, e):
        self.entities.remove(e)
        e.on_remove()






    def start(self):
        self.window = pyglet.window.Window(800, 600)
        self.window.set_vsync(True)

        self.floor_batch  = pyglet.graphics.Batch()
        self.object_batch = pyglet.graphics.Batch()
        self.effect_batch = pyglet.graphics.Batch()
        self.wall_batch  = pyglet.graphics.Batch()
        self.window_batch = pyglet.graphics.Batch()
        self.status_label = pyglet.text.Label('Loading...', font_name='sans',
                                              font_size=8, x=10, y=10,
                                              batch=self.window_batch)

        self.fps_display  = pyglet.clock.ClockDisplay()
        self.fps_display.label.batch = self.window_batch

        self.window.set_handler('on_draw', self.on_draw)
        self.window.set_handler('on_resize', self.on_resize)

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
        self.player = self.create_entity(Player)
        self.center_camera()

    def setup_gameloop(self, dt):
        self.notice('Loading game state...')
        pyglet.clock.schedule_interval(self.on_tick, 1.0/60)

    def notice(self, msg):
        self.status_label.text = msg

    def on_resize(self, w, h):
        print "on resize", w, h
        self.window_size = w, h

    def on_draw(self):
        self.window.clear()
        w, h = self.window_size

        # Setup perspective
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-w/2, w/2, -h/2, h/2, -10000, 10000)

        # Move camera above character
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(*map(int, self.camera_position))

        # Draw everything but HUD
        self.floor_batch.draw()
        self.wall_batch.draw()
        self.object_batch.draw()
        self.effect_batch.draw()

        # Draw HUD
        glLoadIdentity()
        glTranslatef(-w/2, -h/2, -100)
        self.window_batch.draw()

    def on_tick(self, dt):
        self.handle_player_movement(dt)
        self.handle_input(dt)

        for entity in self.entities:
            entity.tick(dt)

        for callback in self.tick_callbacks:
            callback(dt)


    def handle_player_movement(self, dt):
        dx = 0.0
        dy = 0.0

        if self.keys[key.RIGHT]: dx += 1
        if self.keys[key.LEFT]:  dx -= 1
        if self.keys[key.UP]:    dy += 1
        if self.keys[key.DOWN]:  dy -= 1

        if dx and dy:
            # Length of vector is always sqrt(2), so we devide it by sqrt(2)
            # to get a uniform vector. Works only for diagonal movement.
            dx *= 0.7071067811865476 # 1/sqrt(2)
            dy *= 0.7071067811865476

        if dx or dy:
            self.player.move(dx*dt, dy*dt)
            self.center_camera()
        else:
            self.player.move(0.0, 0.0) # Tell the player to stop

    def handle_input(self, dt):
        if self.keys[key.E]:
            self.enemies.add(self.create_entity(Enemy, *self.player.position))
        if self.keys[key.D]:
            import pdb; pdb.set_trace()

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
                bullet = self.create_entity(Fireball, x, y+10, bx, by)

    def center_camera(self):
        ''' Move the camera above the player, but only if the player leaves a
            save area. '''
        wx, wy, wz = self.camera_position
        px, py = self.player.position

        # Desired world position in center of screen
        wx = max(-30, min(30, px+wx)) - px
        wy = max(-30, min(30, py+wy)) - py

        self.camera_position = [wx, wy, wz]

game = Game()

def main():
    game.start()

if __name__ == '__main__':
    main()


