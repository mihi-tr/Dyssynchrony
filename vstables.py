""" This is a very simple framework to handle simple tables
(Non-Hierarchical and relational). It was designed to dump data into CSV
files and to read CSV files structured similarly to these tables. 

It defines the VsTable object with the following methods:

       append() 
       pop()
       read()
       write()
       order()
       """
import sys
class VsTable:

	def append(self,p):
	    """ Appends a line to the table. 
	    takes a dictionary as an argument, where the keys are the
	    column names. Returns True on success, False on failure.
	    """
	    try:
	      for k, v in p.items():
	        if k not in self.columns:
	          self.columns.append(k)
              self.rows.append(p)
	      return True
	    except:
	      return False
	
	def pop(self,p):
	    """ Pops a line from the table, takes parameters similar to
	    list.pop.
	    returns {"data": dataline}
	    where dataline is a dictionary with the column names as keys.
	    returns False on error.
	    """
	    try:
	      return {"data": self.rows.pop(p)}
	    except:
	      return False
	def read_csv(self,p):
	    """ reads a table from a file object. Called by read with
	    format "csv" """
	    line=p.readline()
	    line=line.rstrip('\r\n')
	    ncolumns=line.split(",")
	    self.columns=ncolumns
	    for line in p.readlines():
	      line=line.rstrip("\n")
	      ln=line.split(",")
	      nr={}
	      for col in ncolumns:
	        nr[col]=ln.pop(0)
              self.append(nr)
	    return True  

	      

	def read(self,p):
	    """ reads a file and converts it to a table. The first line is read
	    as a header and defines the column names. 
	    usage:
	    vstable.read({"format": format,
		 "filename" : filename})
	    where format is in ["csv"] and filename is the filename to be read
	    returns the number of lines read on success, False on error.
	    """
	    try:
	      if "filename" in p:
	        try:
		  f=open(p["filename"],"r")
		except:
		  sys.sterr.write("Cannot open File %s\n"%p["filename"])
		  return False
	      else: f=sys.stdin
	      exec "self.read_%s(f)" % p["format"]
	      if "filename" in p:
	        f.close()
	      return True
	    except:
	      return False


	def write_csv(self,p):
	    """ called by write if format=="csv", takes a file object as
	    parameter """
	    p.write(",".join(self.columns))
	    p.write("\n")
	    for row in self.rows:
	      line=[]
	      for column in self.columns:
	        if column in row:
		  line.append(row[column])
		else:
		  line.append("")
	      p.write(",".join(line))
	      p.write("\n")

	def write(self,p):
	    """ writes a table to a file. The first line will be the header
	    with the column names.
	    usage:
	    vstable.write({"format": format,
			"filename" : filename})
	    where format is in ["csv"] and filename is the filename to be
	    written to. 
	    returns the numbers written on success, False on error.
	    """
	    try:
	     	if "filename" in p:
	          f=open(p["filename"], "w")
		else:
		  f=sys.stdout	
	    except:
	        print ("Can not open file %s" % p["filename"])
		return False
	    exec "self.write_%s(f)" % p["format"]
	    if "filename" in p:
	      	f.close()
	    return True
	def order(self,p):
	    """ Puts the columns in the order specified in ({"columns":[]})
	    returns true on success, false on failure.
	    CAVE: missing columns you already put results in these columns
	    beeing ignored AKA lost!"""
	    try:
	       self.columns=p["columns"]
	       return True
	    except:
	       return False
	def __init__(self):
	    self.columns=[]
	    self.rows=[]
	      


if __name__== "__main__":
	""" test all components """
	test= VsTable()
	print ("Testing append: ")
	if test.append({"A":"1","B":"0"}):
	  print("Success")
	else: print("Failed")	
	
	print ("Testing pop: ")
	test.append({"C":"3"})
	a=test.pop(-1)
	if not a:
	  print ("Failed")
	else:	
	  if a["data"]["C"]=="3":
	    print ("Success")
	  else: print ("Failed")  
	
	print ("Testing write (csv): ")
	test.append({"D":"4"})
	if test.write({"format":"csv"}):
	  print ("Success")
	else: print ("Failed")

	print ("Testing read (csv): ")
	test.write({"format":"csv","filename":".test.csv"})
	test2=VsTable()
	test2.columns=[]
	test2.rows=[]
	if test2.read({"format":"csv","filename":".test.csv"}):
	  print ("Success")
	else: print ("Failed")  
	test2.write({"format":"csv"})
	
	print ("testing order: ")
	test3=VsTable()
	test3.append({"A":"a","B":"b","C":"c","D":"d"})
	test3.write({"format":"csv"})
	if test3.order({"columns":["D","C","B","A"]}):
		print ("Success")
	else:
		print ("Failed")
	test3.write({"format":"csv"})	

	
