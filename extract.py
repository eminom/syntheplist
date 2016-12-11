
# eminom
#pip install biplist (primero)

from __future__ import print_function
import sys, os
import biplist
import re
from PIL import Image, ImageFilter

offsetPat  = re.compile(r'\{\{(\d+)\,(\d+)\}\,\{(\d+)\,(\d+)\}\}')
doubleDPat = re.compile(r'\{(\d+)\,(\d+)\}')

def getFrame(frame, rotated):
	m = offsetPat.match(frame)
	assert m, "Must be matched for frame pattern"
	(x, y, width, height) = m.groups()
	if not rotated:
		return (int(x), int(y), int(x) + int(width), int(y) + int(height))  # Return a tuple list.
	return (int(x), int(y), int(x) + int(height), int(y) + int(width))

def separarFrames(frames, image, outd):
	count = 0
	for name in frames:
		#print name
		count += 1
		obj = frames[name]
		isRotated = False
		if 'true' == str(obj['rotated']).lower():
			isRotated = True
		box = getFrame(obj['frame'], isRotated)
		region = image.crop(box)
		if isRotated:
			# Is it rotated in the right direction ??
			region = region.transpose(Image.ROTATE_90)
		try:
			saveName = name
			if not saveName.endswith('.png'):
				saveName += ".png"
			region.save(os.path.join(outd, saveName))
			#print(name + ".png" + " is saved!!")
		except:
			print("Error***********************")
			pass
		#print '  rotate:', str(obj['rotated']).lower()
		#printFrame(obj['frame'])
		#printSourceSize(obj['sourceSize'])
		#printOffset(obj['offset'])
		#print '  index: -1'  #Fixed output
	print("There are %d in all" % count)

def doUnpack(listpath, pngpath, outd):
	plist = biplist.readPlist(listpath)
	obj = Image.open(pngpath)
	#print(obj.size)
	separarFrames(plist['frames'], obj, outd)
	
def getCurrentModPath():
	return os.path.dirname(os.path.abspath(__file__))

if '__main__' == __name__:
	#
	#if len(sys.argv) < 2:
	#	print("not enough input")
	#	print("need to specify your target")
	#	sys.exit(-1)
	#target = sys.argv[1]
	if len(sys.argv) <= 1:
		print("Not enough input")
		sys.exit(-1)
	uno = sys.argv[1]
	startd = getCurrentModPath()
	target_plist = os.path.join(startd, uno + ".plist")
	png_file = os.path.join(startd, uno + ".png")
	if not os.path.isfile(target_plist):
		raise RuntimeError("No %s" % target_plist)
	if not os.path.isfile(png_file):
		raise RuntimeError("No %s" % png_file)
	outs = os.path.join(startd, uno)
	try:
		os.mkdir(outs)
	except WindowsError:
		pass
	if not os.path.isdir(outs):
		raise RuntimeError("Cannot not create %s" % uno)
	doUnpack(target_plist, png_file, outs)
