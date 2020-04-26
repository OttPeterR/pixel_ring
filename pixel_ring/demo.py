import time
import argparse
from apa102_pixel_ring import PixelRing

parser = argparse.ArgumentParser(description='Light ring demo')
parser.add_argument('--theme', type=str, required=False, default='echo', choices=['echo', 'google'])

theme = parser.parse_args().theme
pixel_ring = PixelRing(pattern=theme)
pixel_ring.set_brightness(10)
while True:
    try:
        print("wakeup")
        pixel_ring.wakeup()
        time.sleep(3)
        print("thinking")
        pixel_ring.think()
        time.sleep(3)
        print("speaking")
        pixel_ring.speak()
        time.sleep(6)
        print("listening")
        pixel_ring.listen()
        time.sleep(3)
        print("off")
        pixel_ring.off()
        time.sleep(3)
    except KeyboardInterrupt:
        break

pixel_ring.off()
time.sleep(1)

