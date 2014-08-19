""" This module defines the Strain object. The object has several
attributes, the attributes are defined in the attribute parameters.

All these Parameters are taken from a tab seperated file as saved by the
VevoStrain package, passed to init() or if init was empty to getdata.

More shit to come here
"""

""" This code has been written by Michael Bauer <mihi@lo-res.org>, I am not
responsible for anything, use at your own risk, feel free to rewrite, reuse
etc."""

import numpy,re,os

def __version__():
	import ToolBox as tb
	name="straindata"
	commit=tb.get_git_commit("straindata")
	ret=[]
	ret.append(": ".join([name,commit]))
	modules=[tb]
	for module in modules:
		ret.append(module.__version__())
	return ("\n\t".join(ret))	
	
class Group:
	""" Group of Strain Objects, made to have an easy handle for
	averages etc. """
	def __init__(self):
		self.groups=({})
	def addgroup(self, group):
		""" Adds a group to the set of groups, Do NOT readd groups,
		since it initializes the group with zero elements! """
		self.groups[group]=[]

	def add(self,p):
		""" Adds a strain object to a group. takes the following
		parameters ({"group":groupname, "sobj": strain object}) """
		self.groups[p["group"]].append(p["sobj"])
	
	def getpk(self, p):
		""" Determines the Peak values for a given parameter, takes
		the following parameters ({"group": groupname,
		"parameter":parameter, "func": max or min}) 
		returns a dict with ({"average","stdev","sterr"})"""
		r=[]
		for i in self.groups[p["group"]]:
			if p["func"]=="min":
				pk=i.param[p["parameter"]].min(1).transpose()
			if p["func"]=="max":
				pk=i.param[p["parameter"]].max(1).transpose()
			r.append(pk)
		rdict=({})
		rdict["average"]=numpy.average(r,axis=0)
		rdict["stdev"]=numpy.std(r,axis=0)
		rdict["stderr"]=numpy.divide(rdict["stdev"],numpy.sqrt(len(r)))
		return rdict
	def readfromfile(self, p):
		""" Reads group definitions from a file and tries to load
		the strain objects. parameters ({"filename":filename}) """
		import xml.dom.minidom
		defs=xml.dom.minidom.parse(p["filename"])
		(base,null)=os.path.split(p["filename"])
		defs=defs.getElementsByTagName("strain")[0]
		for i in defs.getElementsByTagName("group"):
			g=i.getAttribute("name")
			self.addgroup(g)
			for j in i.getElementsByTagName("item"):
				s=Strain()
				c=re.compile("^/")
				if (c.match(j.getAttribute("href"))):
					s.getdata(({"filename":j.getAttribute("href")}))
				else:	
					s.getdata(({"filename":base+os.sep+j.getAttribute("href")}))
				self.add(({"group":g,"sobj":s}))
	def read(self, p):
		""" reads the definitin with parameters: ({"xml":xml}) """
		defs=p["xml"]
		defs=defs.getElementsByTagName("strain")[0]
		for i in defs.getElementsByTagName("group"):
			g=i.getAttribute("name")
			self.addgroup(g)
			for j in i.getElementsByTagName("item"):
				s=Strain()
				s.getdata(({"filename":j.getAttribute("href")}))
				self.add(({"group":g,"sobj":s}))


		

		
			

class Strain:
	parameters=["Axis", "Bpm", "PixelDimension",
	"TracePointsEndoXYpixel", "TracePointsEndoXYmm", "EcgPoints",
	"FrameTime", "TimeProgr", "Strain ", "StrainRate", "tX", "tY",
	"tVx", "tVy", "RadialStrain ", "RadialStrainRate", "Vol", "Seg_Vol",
	"DMin", "DMax", "dV/dt", "Shear ", "ShearRate"]
	def __init__(self):
		""" the init function """
		self.param=({})
			
	def getdata(self,p):
		""" imports it's data from the file given in ({"filename":
		filename}) """
		try:
			if "filename" in p:
				f=open(p["filename"],"r")
			else: return False
			self.param=parse(f,self.parameters)            
		except:
			print(p["filename"])
			return False
			
		
def returnarray(file,spc):
	""" returns an numpy array object from a file, continues to read
	until it finds an empty line """
	line=file.readline()
	a=[]
	while (len(line)>2):
		linecols=line.strip().split(spc)
		f=listfloat(linecols)
		if len(f)>0:
			a.append([f])
		""" FIXME: The [ ] brackets don't need to be here """
		line=file.readline()
	return numpy.array(a)	

def createaverages(s,prm):
	""" Averages a parameter over multiple cycles """
	cycles=int(s.param["TimeProgr"].max()/(60/float(s.param["Bpm"])*1000))
	cyclelength=int((60/float(s.param["Bpm"])*1000)/numpy.average(s.param["FrameTime"]))
	if cycles<1:
		cycles=1
		a=0
	else:
		a=numpy.abs(numpy.average(s.param["Strain"],axis=0)).argmin()
	if a>cyclelength/2.:
		a=0
	r=[]
	for i in range(0,cycles):
		l=a+cyclelength*i
		h=a+cyclelength*(i+1)
		r.append(s.param[prm][::,0,l:h])
	return numpy.average(r,axis=0)	
		

def listfloat(slist):
	""" converts a list of strings to a list of floats """
	flist=[]
	for s in slist:
		try:
			flist.append(float(s))
		except: 
			""" do nothing, we don't want strings in here """
	return (flist)
	
def parse(file,parameters):
	""" Parses a file, sends the file to either parsetab or parsecsv,
	depending on the files format """
	line=file.readline()
	k=re.compile("[=\[]")
	file.seek(0)
	if k.search(line):
		return parsetab(file,parameters)
	else:
		return parsecsv(file,parameters)
	
def parsetab(file,parameters):
	""" Parses a tab seperated file for parameters """
	p=({})
	line=file.readline()
	while(line):
		linecols=line.strip().split("\t")
		for key in parameters:
			k=re.compile("^"+key)
			key=key.strip()
			if k.search(linecols[0]):
				he=re.compile("=")
				if he.search(linecols[0]):
					p[key]=linecols[0].split("=")[1]
				else:
					p[key]=returnarray(file,"\t")
		line=file.readline()
	return p
	

def parsecsv(file,parameters):
	""" Parses a comma seperated file for parameters """
	p=({})
	line=file.readline()
	while(line):
		linecols=line.strip().split(",")
		for key in parameters:
			k=re.compile("^"+key)
			key=key.strip()
			if k.search(linecols[0]):
				if len(linecols) > 1 and len(linecols[1])>1:
					p[key]=linecols[1]
				else:
					p[key]=returnarray(file,",")
		line=file.readline()
	return p

		
		
	

if __name__== "__main__":
	""" test object initializing """
	s=Strain()
	s.getdata(({"filename":"test.txt"}))
	print s.param
