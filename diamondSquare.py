import random
import math
import copy

# We intend to use this in maya, which doesn't need PIL and has trouble finding it
# However the write function is useful for testing outside of maya so let's try and access it
try:
	import Image
	pilAvailable = True
except:
	pilAvailable = False
	print "PIL not found, write is unavailable"

# Adapted from http://www.bluh.org/code-the-diamond-square-algorithm/

def linearInterp(a, b, t):
	return a + (b - a) * t

def cosineInterp(a, b, t):
	t2 = (1-math.cos(t * math.pi))/2
	return a * (1 - t2) + b * t2

# Stores pixel data and provides methods that automatically wrap 
# sample values for us when reading/writing pixel data
class PixelData:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.values = [0] * (width*height)

	def setSample(self, x, y, value):
		self.values[ (x & (self.width-1)) + (y & (self.height - 1)) * self.width] = value

	def sample(self, x, y):
		return self.values[(x & (self.width - 1)) + (y & (self.height - 1)) * self.width]

	def getInterpolatedPixels(self, interpFunction, min = 0, max = 1):
		pixelBuffer = copy.deepcopy(self.values)

		for i, pixel in enumerate(pixelBuffer):
			pixelBuffer[i] = interpFunction(min, max, pixel)

		return pixelBuffer

def write(filename, values, width, height):
	if(pilAvailable):
		image = Image.new("L", (width, height), "white")

		# Avoid accidentally modifying the pixels we're passing in
		pixelBuffer = copy.deepcopy(values)

		# Remap for 8-bit image output
		for i, pixel in enumerate(pixelBuffer):
			pixelBuffer[i] = linearInterp(0, 255, pixel)

		image.putdata(pixelBuffer)
		image.save(filename)
	else:
		print "PIL not found, write is unavailable"

def sampleSquare(pixels, x, y, size, value):
	hs = size / 2

	a = pixels.sample(x - hs, y - hs)
	b = pixels.sample(x + hs, y - hs)
	c = pixels.sample(x - hs, y + hs)
	d = pixels.sample(x + hs, y + hs)

	pixels.setSample(x, y, ((a + b + c + d) / 4.0) + value)

def sampleDiamond(pixels, x, y , size, value):
	hs = size / 2

	a = pixels.sample(x - hs, y)
	b = pixels.sample(x + hs, y)
	c = pixels.sample(x, y - hs)
	d = pixels.sample(x, y + hs)

	pixels.setSample(x, y, ((a + b + c + d) / 4.0) + value)

def DiamondSquare(pixels, stepSize, scale):
	halfstep = stepSize / 2

	for y in range(halfstep, pixels.height + halfstep, stepSize):
		for x in range(halfstep, pixels.width + halfstep, stepSize):
			sampleSquare(pixels, x, y, stepSize, random.uniform(-1, 1) * scale)

	for y in range(0, pixels.height, stepSize):
			for x in range(0, pixels.width, stepSize):
				sampleDiamond(pixels, x + halfstep, y, 				stepSize, random.uniform(-1, 1) * scale)	
				sampleDiamond(pixels, x, 			y + halfstep, 	stepSize, random.uniform(-1, 1) * scale)	

def generate(width, height, featuresize, scale):
	pixels = PixelData(width, height) 

	samplesize = featuresize

	while(samplesize > 1):
		DiamondSquare(pixels, samplesize, scale)
		samplesize /= 2
		scale /= 2

	return pixels

if __name__ == "__main__":
	width = 512
	height = 512

	pixelMap = generate(width, height, 16, 1.0)
	
	write("cerp.tif", pixelMap.getInterpolatedPixels(cosineInterp, 0, 2), width, height)
	write("lerp.tif", pixelMap.getInterpolatedPixels(linearInterp, 0, 2), width, height)