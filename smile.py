import time

import Image
import ImageDraw
import Matrix64

display = Matrix64.Matrix64() 
display.begin();
display.clear();

# First create an 8x8 1 bit color image.
image = Image.new('1', (8, 8))

# Then create a draw instance.
draw = ImageDraw.Draw(image)
draw.line((2,0,5,0), fill=255)
#draw.rectangle((0,0,7,7), outline=255, fill=0)
display.setImage(image)
#display.full();
display.show();

buf = bytearray([0b00111100, 0b01000010, 0b10100101, 0b10000001, 0b10100101, 0b10011001, 0b01000010, 0b00111100])
display.writeBuffer( buf );