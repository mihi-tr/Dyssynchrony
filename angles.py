import numpy,os,vstables
from straindata import Strain

def calculateAngle(a,b):
  ret=numpy.arccos(numpy.dot(a,b)/(numpy.linalg.norm(a)*numpy.linalg.norm(b)))
  return ret

def calculateAngles(vectors):
  """ calculate the angles between an numpy array of vectors, where
  vectors are in the first axis """

  ret=[]
  for i in range(0,len(vectors)):
    for v2 in vectors[i+1:]:
      ret.append(calculateAngle(vectors[i],v2))

  return(ret)

def getAngleStatistics(vectors):
  """ returns a dict of mean, median and sd """
  dist=calculateAngles(vectors)
  return {"mean":numpy.average(dist), 
    "median":numpy.median(dist), 
    "sd":numpy.std(dist)}

def tostring(a):
  return ["%f" % b for b in a]

def process(outfile,files):
  t=vstables.VsTable()
  parameters=["Strain", "StrainRate", "RadialStrain",
  "RadialStrainRate"]
  values=["mean","median","sd"]
  sort=["name"]
  sort+=[i+" "+j for i in parameters for j in values]
  for filename in files:
    s=Strain()
    line={};
    s.getdata({"filename":filename})
    line["name"]=filename;
    for p in parameters:
      print s.param.keys()
      a=getAngleStatistics(s.param[p])
      for v in values:
        line["%s %s"%(p,v)]=str(a[v])
  
    t.append(line)
  t.order({"columns":sort})
  t.write({"format":"csv","filename":outfile})
    
if __name__=="__main__":
  import sys
  sys.argv.pop(0)
  outfile=sys.argv.pop(0)
  process(outfile,sys.argv)
  
    

