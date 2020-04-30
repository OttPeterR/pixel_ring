"""
LED pattern like Echo
"""

import time


class Echo(object):
    brightness = 24 * 8

    def __init__(self, show, number=12):
        self.pixels_number = number
        self.pixels = [0] * 4 * number

        if not callable(show):
            raise ValueError('show parameter is not callable')

        self.show = show
        self.stop = False

    def wakeup(self, direction=0):
        position = int((direction + 15) / (360 / self.pixels_number)) % self.pixels_number

        pixels = [0, 0, 0, self.brightness] * self.pixels_number
        pixels[position * 4 + 2] = self.brightness

        self.show(pixels)

    def listen(self):
        pixels = [0, 0, 0, self.brightness] * self.pixels_number

        self.show(pixels)

    def think(self):
        half_brightness = int(self.brightness / 2)
        pixels  = [0, 0, half_brightness, half_brightness, 0, 0, 0, self.brightness] * self.pixels_number

        while not self.stop:
            self.show(pixels)
            time.sleep(0.2)
            pixels = pixels[-4:] + pixels[:-4]

    def speak(self):
        step = int(self.brightness / 12)
        position = int(self.brightness / 2)
        while not self.stop:
            pixels  = [0, 0, position, self.brightness - position] * self.pixels_number
            self.show(pixels)
            time.sleep(0.01)
            if position <= 0:
                step = int(self.brightness / 12)
                time.sleep(0.4)
            elif position >= int(self.brightness / 2):
                step = - int(self.brightness / 12)
                time.sleep(0.4)

            position += step

    def off(self):
        self.show([0] * 4 * 12)

class GoogleHome(object):
    def __init__(self, show):
        self.basis = [0] * 4 * 12
        self.basis[0 * 4 + 1] = 8
        self.basis[3 * 4 + 1] = 4
        self.basis[3 * 4 + 2] = 4
        self.basis[6 * 4 + 2] = 8
        self.basis[9 * 4 + 3] = 8

        self.pixels = self.basis

        if not callable(show):
            raise ValueError('show parameter is not callable')

        self.show = show
        self.stop = False

    def wakeup(self, direction=0):
        position = int((direction + 90 + 15) / 30) % 12

        basis = self.basis[position*-4:] + self.basis[:position*-4]
        
        pixels = [v * 25 for v in basis]
        self.show(pixels)
        time.sleep(0.1)

        pixels =  pixels[-4:] + pixels[:-4]
        self.show(pixels)
        time.sleep(0.1)

        for i in range(2):
            new_pixels = pixels[-4:] + pixels[:-4]
            
            self.show([v/2+pixels[index] for index, v in enumerate(new_pixels)])
            pixels = new_pixels
            time.sleep(0.1)

        self.show(pixels)
        self.pixels = pixels

    def listen(self):
        pixels = self.pixels
        for i in range(1, 25):
            self.show([(v * i / 24) for v in pixels])
            time.sleep(0.01)

    def think(self):
        pixels = self.pixels

        while not self.stop:
            pixels = pixels[-4:] + pixels[:-4]
            self.show(pixels)
            time.sleep(0.2)

        t = 0.1
        for i in range(0, 5):
            pixels = pixels[-4:] + pixels[:-4]
            self.show([(v * (4 - i) / 4) for v in pixels])
            time.sleep(t)
            t /= 2

        self.pixels = pixels

    def speak(self):
        pixels = self.pixels
        step = 1
        brightness = 5
        while not self.stop:
            self.show([(v * brightness / 24) for v in pixels])
            time.sleep(0.02)

            if brightness <= 5:
                step = 1
                time.sleep(0.4)
            elif brightness >= 24:
                step = -1
                time.sleep(0.4)

            brightness += step

    def off(self):
        self.show([0] * 4 * 12)

class MyTheme1(object):
    brightness = 24 * 8
    # pixels are ints [r, g, b, brightness] * pixels_numbers

    def __init__(self, show, number=12):
        self.pixels_number = number
        self.default_color_block = [0,0,self.brightness//2,self.brightness]
        self.pixels = [0] * 4 * number

        if not callable(show):
            raise ValueError('show parameter is not callable')

        self.show = show
        self.stop = False

    def wakeup(self, direction=0):
        position = int((direction + 15) / (360 / self.pixels_number)) % self.pixels_number

        # start with all off
        pixels = [0, 0, 0, 0] * self.pixels_number
        self.show(pixels)
        
        # gradually grow the circle
        i=0
        t = 0.25/ self.pixels_number # seconds for entire wakeup animation / pixels
        # wrap around the display illuminating the pixels
        while i < self.pixels_number-1 and not self.stop:
            indx = ((i+position) % self.pixels_number)*4
            pixels[indx:indx+4] = self.default_color_block
            indx = (((i+1)+position) % self.pixels_number)*4
            pixels[indx:indx+4] = [x//10 for x in self.default_color_block]
            indx = (((i+2)+position) % self.pixels_number)*4
            pixels[indx:indx+4] = [x//25 for x in self.default_color_block]
            time.sleep(t)
            self.show(pixels)
            i+=1
        pixels = self.default_color_block * self.pixels_number
        self.show(pixels)

    def listen(self):
        pixels = self.default_color_block * self.pixels_number

        self.show(pixels)

    def think(self):
        pixels  = [0, 0, 0, 0] * (self.pixels_number//2)
        pixels += self.default_color_block * ((self.pixels_number+1)//2)

        t = 0.35 / self.pixels_number
        while not self.stop:
            self.show(pixels)
            time.sleep(t)
            pixels = pixels[-4:] + pixels[:-4]

    def speak(self):
        step = int(self.brightness / 12)
        position = int(self.brightness / 2)
        high, low, step = 10, 1, 1
        t = (1.0/((high-low)/step))/2
        while not self.stop:
            for i in range(low, high, step):
                pixels = [x//i for x in self.default_color_block] * self.pixels_number
                self.show(pixels)
                time.sleep(t)
            for i in range(high, low, -step):
                pixels = [x//i for x in self.default_color_block] * self.pixels_number
                self.show(pixels)
                time.sleep(t)
    def off(self):
        self.show([0] * 4 * 12)
