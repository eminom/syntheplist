#
# run in Python 2.7

from __future__ import print_function
import json, os, biplist
from PIL import Image, ImageFilter

###############
class EntItemStatic:
	@staticmethod
	def getPreName(name):
		lpos = name.rfind('.')
		if lpos >= 0:
			return name[:lpos]
		return name
	@staticmethod	
	def makeEnt(parent, name):
		pre_name = EntItemStatic.getPreName(name) # A name without suffix
		plist_name = pre_name + ".plist"
		return {
			'Parent':parent,
			'Fullpath':os.path.join(parent, name),
			'Plist':os.path.join(parent, plist_name),
			'Name':pre_name,
			'Basename':name,
		}
	
class EntItem:
	def __init__(self, parent, name):
		self.__dict__ = EntItemStatic.makeEnt(parent, name)   # Access to memeber instantly.
	def __str__(self):
		return '%s' % self.Name
	def __repr__(self):
		return '<%s>' % self.Name

# Get the processing targets.
def retrieveTargets(nd):
	ls = []
	for parent, ds, fs in os.walk(nd):
		#for dir in ds:
		#	print("[%s]" % dir)
		for file in fs:
			#print("%s" % file)
			if file.startswith('sk_') and file.endswith('.png'):
				if not os.path.isfile(os.path.join(parent, file[:file.rfind('.')] + ".plist")):
					print("Cannot locate plist for %s" % file)
				ls.append(EntItem(parent, file))
				
	dset = {}
	for ent in ls:
		name = ent.Name
		seq = '_'.join(name.split('_')[:-1])
		nset = dset.get(seq, [])
		nset.append(ent)
		dset[seq] = nset
	return dset

def processGo(subName):
	cur = os.path.abspath(__file__)
	curdir = os.path.dirname(cur)
	if not os.path.isdir(curdir):
		raise RuntimeError("Not a directory for path `%s'" % curdir)
	nextdir = os.path.join(curdir, subName)
	if not os.path.isdir(nextdir):
		raise RuntimeError("Not a directory for target path `%s'"%nextdir)
	print("Processing of <%s>" % nextdir)
	targets = retrieveTargets(nextdir)
	return targets
	#print(targets)

def getDef():
	return processGo('outs')
	
def doAnalyze(targets):
	keyCount = 0
	for i in targets:
		keyCount += 1
	print("Keycount:%d" % keyCount)
	for k in targets:
		print("%s"%k)
	
def doSyn():
	ts = getDef()
	doAnalyze(ts)
	prtCount = 0
	for k in ts:
		ents = ts[k]
		print("Entries of <%s>" % k)
		for ent in ents:
			o = Image.open(ent.Fullpath)
			print("%d - %d" % (o.width, o.height))
			prtCount += 1
	print("print count to %d" % prtCount)
	return ts, prtCount
	
if '__main__' == __name__:
	doSyn()