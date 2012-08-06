import pyglet

class Game(object):
    def __init__(self):
        pass

    def setup(self):
        pyglet.resource.path = ['./resources']
        pyglet.resource.reindex()
        self.window = pyglet.window.Window(800, 600)
        self.window.set_handler('on_draw', self.on_draw)
        pyglet.clock.schedule_interval(self.on_tick, 1.0/60)
        self.fps_display = pyglet.clock.ClockDisplay()

    def start(self):
        self.setup()
        pyglet.app.run()

    def on_draw(self):
        print 'x'
        self.window.clear()
        self.fps_display.draw()

    def on_tick(self, dt):
        pass

def main():
    Game().start()

if __name__ == '__main__':
    main()


