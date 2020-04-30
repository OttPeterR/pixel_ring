
import time
import threading
try:
    import queue as Queue
except ImportError:
    import Queue as Queue

from .apa102 import APA102
from .pattern import Echo, GoogleHome, MyTheme1


class PixelRing(object):
    PIXELS_N = 12

    def __init__(self, pattern="1"):
        if pattern == 'echo':
            self.pattern = Echo(show=self.show)
        elif pattern == "mytheme1" or pattern=="1":
            self.pattern = MyTheme1(show=self.show)
        else:
            self.pattern = GoogleHome(show=self.show)

        self.dev = APA102(num_led=self.PIXELS_N)

        self.queue = Queue.Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()
        self.off()

    def set_brightness(self, brightness):
        if brightness > 100:
            brightness = 100

        if brightness > 0:
            self.dev.global_brightness = int(0b11111 * brightness / 100)

    def change_pattern(self, pattern):
        if pattern == 'echo':
            self.pattern = Echo(show=self.show)
        elif pattern == "1" or pattern == "mytheme1":
            self.pattern = MyTheme1(show=self.show)
        else:
            self.pattern = GoogleHome(show=self.show)

    def wakeup(self, direction=0):
        def f():
            self.pattern.wakeup(direction)

        self.put(f)

    def listen(self):
        self.put(self.pattern.listen)

    def think(self):
        self.put(self.pattern.think)

    wait = think

    def speak(self):
        self.put(self.pattern.speak)

    def off(self):
        self.put(self.pattern.off)

    def put(self, func):
        self.pattern.stop = True
        self.queue.put(func)

    def _run(self):
        while True:
            func = self.queue.get()
            self.pattern.stop = False
            func()

    def show(self, data):
        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, int(data[4*i + 1]), int(data[4*i + 2]), int(data[4*i + 3]))

        self.dev.show()

    def set_color(self, rgb=None, r=0, g=0, b=0):
        if rgb:
            r, g, b = (rgb >> 16) & 0xFF, (rgb >> 8) & 0xFF, rgb & 0xFF
        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, r, g, b)

        self.dev.show()

