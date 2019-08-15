import random

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

from pids import *

class Guage(object):
    def __init__(self):
        self.i2c = busio.I2C(SCL, SDA)
        self.disp = adafruit_ssd1306.SSD1306_I2C(128, 32, self.i2c)

        self.width = self.disp.width
        self.height = self.disp.height

        self.smallfont = ImageFont.truetype('Roboto-Regular.ttf', size=8)
        self.bigfont = ImageFont.truetype('Roboto-Regular.ttf', size=16)

        self.clear()

    def clear(self):
        self.disp.fill(0)
        self.disp.show()

    def display(self, payload):
        image = Image.new('1', (self.width, self.height))

        draw = ImageDraw.Draw(image)
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        thispid = pids[payload['name']]

        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        deg = int((float(payload['value']) / (thispid['max'] - thispid['min']) ) * 180)


        draw.arc((0,0,64,64), 180, 360, fill=1)
        draw.pieslice((0,0,64,64), 180, 180+deg, fill=1)
        draw.pieslice((16,16,48,48), 180, 360, fill=0)
        draw.arc((16,16,48,48), 180, 360, fill=1)

        draw.text((70, 0), thispid['title'], font=self.smallfont, fill=255)
        draw.text((70, 16), str(payload['value']), font=self.bigfont, fill=255)

        self.disp.image(image)
        self.disp.show()

if __name__ == '__main__':
    g = Guage()
    g.display( {"value": "26.666666666666668", "name": "ENGINE_LOAD", "time": 1565711433.1096218, "units": "percent"} )
