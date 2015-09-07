DEFAULT_ADDRESS				= 0x70

import mraa

class Matrix64():

	_i2c = None

	def __init__(self, address=DEFAULT_ADDRESS):
		self._i2c=mraa.I2c(0)

		"""Create an HT16K33 driver for devie on the specified I2C address
		(defaults to 0x70) and I2C bus (defaults to platform specific bus).
		"""
		self._i2c.address(0x70);  
		self.buffer = bytearray([0]*17)

	def begin(self):
		self._i2c.writeByte(0x21); # Turn on oscillator  
		self._i2c.writeByte(0xef); # Brightness 15  
		self._i2c.writeByte(0x81); # No blinking

	def clear(self):
		for i, value in enumerate(self.buffer):
			self.buffer[i] = 0

	def show(self):
		"""Write display buffer to display hardware."""
		print ( " ".join(map(lambda b: format(b, "08b"), self.buffer)) )
		print ( " ".join(map(lambda b: format(b, "02x"), self.buffer)) )
		self._i2c.write(self.buffer)

	def set_pixel(self, x, y, value):
		"""Set pixel at position x, y to the given value.  X and Y should be values
		of 0 to 8.  Value should be 0 for off and non-zero for on.
		"""
		if x < 0 or x > 7 or y < 0 or y > 7:
			# Ignore out of bounds pixels.
			return
		self.set_led(y*16+((x+7)%8), value)

	def set_led(self, led, value):
		"""Sets specified LED (value of 0 to 127) to the specified value, 0/False 
		for off and 1 (or any True/non-zero value) for on.
		"""
		if led < 0 or led > 127:
			raise ValueError('LED must be value of 0 to 127.')
		# Calculate position in byte buffer and bit offset of desired LED.
		pos = led / 8
		offset = led % 8
		if not value:
			# Turn off the specified LED (set bit to zero).
			self.buffer[pos+1] &= ~(1 << offset)
		else:
			# Turn on the speciried LED (set bit to one).
			self.buffer[pos+1] |= (1 << offset)

	def setImage(self, image):
		"""Set display buffer to Python Image Library image.  Image will be converted
		to 1 bit color and non-zero color values will light the LEDs.
		"""
		imwidth, imheight = image.size
		if imwidth != 8 or imheight != 8:
			raise ValueError('Image must be an 8x8 pixels in size.')
		# Convert image to 1 bit color and grab all the pixels.
		pix = image.convert('1').load()
		# Loop through each pixel and write the display buffer pixel.
		for x in [0, 1, 2, 3, 4, 5, 6, 7]:
			for y in [0, 1, 2, 3, 4, 5, 6, 7]:
				color = pix[(x, y)]
				# Handle the color of the pixel, off or on.
				if color == 0:
					self.set_pixel(x, y, 0)
				else:
					self.set_pixel(x, y, 1)

	def writeBuffer(self, binaryBuffer):
		tempBuffer = bytearray([0]*(len(binaryBuffer)*2+1))
		tempBuffer[0] = 0x00;
		number = 0 
		for x in binaryBuffer:
			z = 0
 			y = x >> 1

 			if x & 0b00000001 :		
				z = ( y | 0b10000000 );	
			else:						
				z = y & 0b11111111;

			tempBuffer[number*2+1] = z
			tempBuffer[number*2+2] = 0
			number = number +1

		print ( " ".join(map(lambda b: format(b, "08b"), tempBuffer)) )
		print ( " ".join(map(lambda b: format(b, "02x"), tempBuffer)) )
		#zero = bytearray([0x00, 0x81, 0x00, 0x81, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00])
		self._i2c.write(tempBuffer)