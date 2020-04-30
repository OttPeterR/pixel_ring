import time
import argparse
from pixel_ring import pixel_ring
from gpiozero import LED


parser = argparse.ArgumentParser(description='Light ring demo')
parser.add_argument('--theme', type=str, required=False, default='echo', choices=['echo', 'google', 'mytheme1', '1'])

power = LED(5)
power.on()


theme = parser.parse_args().theme
pixel_ring.change_pattern(theme)
pixel_ring.set_brightness(10)
t = 5
while True:
    try:
        print("wakeup")
        pixel_ring.wakeup()
        time.sleep(t)
        print("listening")
        pixel_ring.listen()
        time.sleep(t)
        print("thinking")
        pixel_ring.think()
        time.sleep(t)
        print("speaking")
        pixel_ring.speak()
        time.sleep(t)
        print("off")
        pixel_ring.off()
        time.sleep(1)
    except KeyboardInterrupt:
        break

pixel_ring.off()
power.off()
time.sleep(1)
