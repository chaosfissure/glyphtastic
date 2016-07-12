# Note - this implementation uses PILLOW rather than PIL.

from PIL import Image
from sys import argv
from time import time
import random

# ------------------------------------------------------------------------
# Handle filling and unfilling parts of blocks
# ------------------------------------------------------------------------

def BlockFill(left, right, top, bottom, pixels):
	for x in xrange(left, right):
		for y in xrange(top, bottom):
			pixels[x,y] = (0,0,0)
			
def BlockErase(left, right, top, bottom, pixels):
	for x in xrange(left, right):
		for y in xrange(top, bottom):
			pixels[x,y] = (255,255,255)
	
# ------------------------------------------------------------------------
# Create our actual glyph shapes.	
# ------------------------------------------------------------------------
def Glyph(seed, square, blockoffset, width, height, forcemode, exclusive, fixed):
	
	# For repeatability on any given input set.  This can be removed
	# if you're not concerned with this, replaced with something like
	
	if not fixed:
		random.seed(time()*10000.0)
	else:
		random.seed(seed)
	
	# ------------------------------------------------------------------------
	# Higher ratio of vertical lines to horizontal lines.
	# ------------------------------------------------------------------------
	leftProbability = 0.072333333
	rightProbability = 0.0666
	downProbability = 0.9
	invisibleProbablilty = 0.01
	
	if forcemode == 1: 

		# ------------------------------------------------------------------------
		# Connections snake around a bit more and don't form solid or straight
		# lines nearly as frequently.	
		# ------------------------------------------------------------------------
		leftProbability = 0.6
		rightProbability = 0.01
		downProbability = 0.3333
		invisibleProbablilty = 0.15
		
	elif forcemode > 1:
	
		# ------------------------------------------------------------------------
		# Pure randomization based off of the seeded value
		# ------------------------------------------------------------------------
		leftProbability = random.random()
		rightProbability = random.random() 
		downProbability = random.random()
		invisibleProbablilty = random.random() *0.33333
	
	# We're going to return an image with the pixels already filled in,
	# so we can just copy them into the final image at the end.
	image = Image.new("RGB", (w, h), 0xffffff)
	pixels = image.load()	

	for x in range(2, width):
		for y in range(1, height+1):
				
			left = (square+blockOffset)*x
			top = (square+blockOffset)*y

			# Invisible is special, has to go first to clean up any edges that would "connect"
			# to it so that there aren't very small extrusions in random places!
			
			if random.random() > invisibleProbablilty:

				# Generate the square base
				BlockFill(left, left+square, top, top+square, pixels)
				
				used = False
				
				# Send a connection below?
				if y < height and random.random() <= downProbability:
					BlockFill(left, left + square, top + square, top+square+blockOffset, pixels)
					used = True
					
				if random.random() >= exclusive or not used:
				
					# Send a connection to the left?
					if random.random() <= leftProbability:
						BlockFill(left-blockOffset-square, left, top, top + square, pixels)

					# Send a connection to the right?
					if random.random() <= rightProbability:
						BlockFill(left+square, left+square+blockOffset+square, top, top + square, pixels)
								
			else:
				# Clean up any edge parts (block offset) that might have been filled in
				# by either down / left / right generations.
				
				# Clean up the pixels above.
				if y >= 1:
					BlockErase(left, left+square, top-blockOffset, top, pixels)
							
				# Clean up the pixels below.
				BlockErase(left, left+square, top+square, top+square+blockOffset, pixels)
							
				# Clean up the pixels to the left.
				BlockErase(left-blockOffset, left, top, top+square, pixels)
					
	return image
		
if __name__ == '__main__':

	# These parameters control how many glyphs are stacked vertically and horizontally.
	vglyphs, hglyphs = 6, 8
	
	# These parameters control how wide and tall the glyphs are.
	vblocks, hblocks = 6, 12
	
	# This controls the size of the blocks that are filled in for the glyphs.  The larger
	# this is, the larger the blocks will be.
	blocksize = 8
	
	# Force all generated terms to be in a single mode?
	forcemode = -1
	
	# Only allow down OR left+right generation?  This is a probabillity.
	exclusive=0.5
	
	# Use a fixed seed based on position of generated image? (true)
	# Or use a seed based on the time it is generated? (false)
	
	fixed = False

	for arg in [x.lower() for x in argv[1:]]:
		if   'vglyphs='   in arg: vglyphs   = int(arg.replace('vglyphs=', ''))
		elif 'hglyphs='   in arg: hglyphs   = int(arg.replace('hglyphs=', ''))
		elif 'vblocks='   in arg: vblocks   = int(arg.replace('vblocks=', ''))
		elif 'hblocks='   in arg: hblocks   = int(arg.replace('hblocks=', ''))
		elif 'blocksize=' in arg: blocksize = int(arg.replace('blocksize=', ''))
		elif 'mode='      in arg: forcemode = int(arg.replace('mode=', ''))
		elif 'exclusive=' in arg: exclusive = float(arg.replace('exclusive=', ''))
		elif 'fixed='     in arg: fixed     = int(arg.replace('fixed=', '')) != 0
		
	blockOffset = blocksize / 4
	w = (blocksize + blockOffset) * (vblocks+2)
	h = (blocksize + blockOffset) * (hblocks+2)

	image = Image.new("RGB", (w*hglyphs, h*vglyphs + blockOffset), 0xffffff)
	pixels = image.load()
	counter = 0

	for x in xrange(hglyphs):
		for y in xrange(vglyphs):
			modeforce = y%3 if forcemode == -1 else forcemode
			
			tile = Glyph(counter, blocksize, blockOffset, vblocks, hblocks, modeforce, exclusive, fixed).load()
			counter += 1
		
			xmin = x*w
			ymin = y*h
			xmax = (x+1)*w
			ymax = (y+1)*h
			
			for xx in range(w):
				for yy in range(h):
					pixels[xmin + xx, ymin + yy] = tile[xx, yy]
					
			print 'Finished', counter, '/', vglyphs*hglyphs

	image.save("test_" + str(int(time())) + ".png")

