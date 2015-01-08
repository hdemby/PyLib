#!/usr/bin/env python
"""
DataTools.py

Must add input and function testing 


"""
import re,os,sys

##---------------------------------
## regular expression text patterns
##---------------------------------
linepatt=re.compile("(\s)IN(\s)")
nspatt=re.compile("(\s)NS(\s)")
soapatt=re.compile("(\s)SOA(\s)")
rrpatt=re.compile("IN(\s)(A|CNAME|MX|SRV|NAPTR)(\s)")

##--------------------------
## array to string functions
##--------------------------
dlmrender=lambda a:"%s"%dlm.join("%s" % s for s in a)# each line 's' has line[-1] != "\n"
render= lambda a:"".join("%s" % s for s in a)
rendern=lambda a:"\n".join("%s" % s for s in a)
hostrender=lambda a:".".join("%s"%s for s in a)# create dot delimited string
itemrender=lambda a:"\t".join("%s" % s for s in a) #create tab delimited string line
arrayrender=lambda a:rendern(render(s) for s in a)

# more sophisticated render functions
listrender=lambda a:"\n".join("%s" % s.strip() for s in a) # create text from list min linefeeds
listlinerender=lambda a:"\n".join("%s,"*len(s)%tuple(s) for s in a) # create text from list of list lines
dictrender=lambda a:"\n".join('{%s:%s}' % (k,v) for k,v in a.items())

##--------------------------
## data conditioning functions
##--------------------------
def minspace(line):
  """remove extra whitespace between fields"""
  newline=line.strip()
  newline=newline.replace(" ","\t")
  while newline.find("\t\t") > -1:
    newline=newline.replace("\t\t","\t")
  return newline
  
def rvstr(str):
  "reverse a sting"
  #rv=""
  #for n in range(len(str)-1,0,-1):
  #  rv+=str[n]
  return rvstr[::-1]

flipstr=lambda a:rvstr(a)

##--------------------------
## list functions
##--------------------------
striplst=lambda a:["%s"%s.strip() for s in a]
listdiff=lambda a,b:["%s"%s for s in a if s not in b]

def uniquelst(lst):
  """return a list of unique elements"""
  _dict={}
  for each in lst:
    _dict[each]=None
  uniquelst=_dict.keys()  
  return uniquelst

def revlst(inlst):
  "reverse a list"
  return inlst[::-1]
  
##--------------------------
## value testing functions
##--------------------------

def validRRec(line):
  """return countable record status of line"""
  import re

  ## line is a valid DNS record
  if not linepatt.search(line) or line[0]==";":
    stat=False
  ## line is not a NS or SOA record
  elif (nspatt.search(line) or (soapatt.search(line))):
    stat=False
  else:
    stat=True
  return stat


##--------------------------
## analysis Functions 
##--------------------------
def incrDictVal(valdict):
    """increment the numeric value of a key"""
    return {valdict.keys()[0]:int(valdict[valdict.keys()[0]])+1}
#>>> valdict={'1':1}; assert(incrDictVal(valdict)=={'1':2})

def lst2FreqDict(vallst):
    """convert a list of values into a frequency hash

    USAGE: lst2FreqDict(vallst)
    
    ex: [1,1,1,2,1,7,5,4,1,1,3,2,1,6,1,2,1,3] ==> {1:9,2:3,3:2,4:1,5:1,6:1,7:1}

    """
    freqdict={}
    for val in vallst:
        try:
            freqdict[val]+=1
        except KeyError:
            freqdict[val]=1
    return freqdict
#>>> vallst=[1,1,1,2,1,7,5,4,1,1,3,2,1,6,1,2,1,3]; assert(lst2FreqDict(vallst)[vallst[0]]==len([s for s in vallst if s==vallst[0]]))
#>>> wordlst=['if','and'

##--------------------------
## I/O Functions 
##--------------------------
def getResult(cmd):
  """return the result of a system command"""
  result=os.popen(cmd,'r').readlines()
  return result

def txt2file(text,filename,a=0):
    """ write test to an output file"""
    try:
        if a:
            outfile=open("./%s" % filename,'a')
        else:
            outfile=open("./%s" % filename,'w')
        outfile.write(text)
        outfile.close()
        stat= 0
    except:
        raise IOError
        print "Could not create file: %s" % filename
        stat= 1
    return stat

def list2dict(keys,vals=None):
  """ assign list paramaters to dictionary keys"""
  parmdict={}
  if vals:
    for n in range(0,len(keys)-1):
      parmdict.update({keys[n]:vals[n]})
  else:
    for n in range(0,len(keys)-1):
      parmdict.update({keys[n]:{}})
  return parmdict

def file2lst(filename):
  """read file data into list"""
  try:
    datalist=open(filename,'r').readlines()
  except IOError:
    print "file '%s' does not appear to exist"%filename
    datalist=[]
  return datalist
  
def lst2file(filename,data):
  """create a file from the input list"""
  try:
    outfile=open("%s" % filename,'w')
    outfile.write(listrender(data))
    outfile.close()
    stat= 0
  except:
    raise IOError
    print "Could not create file: %s" % filename
    stat= 1
  return stat

def lst2fileAdd(filename,data):
  """append a file with new data"""
  try:
    outfile=open("%s" % (filename),'+a')
    outfile.write(listrender(data))
    outfile.close()
    stat= 0
  except:
    print "Could not append file: %s" % filename
    raise IOError
    stat= 1
  return stat

def Dict2File(ffile,indict=None):
  """store a python dictionary into a file"""
  import pickle
  if indict:
    try:
      dictfile=open(ffile,'w')
      pickle.dump(indict,dictfile)
      dictfile.close()
      return 0
    except IOError:
      print "Can't write to output file"
      return 1

def File2Dict(ffile):
  """read a '.pkl' file into a python dictionary"""
  import pickle
  dictfile=open(ffile,'r')
  outdict=pickle.load(dictfile)
  dictfile.close()
  return outdict

def DictFile(ffile,indict=None):
  """store and retrieve a dictionary from a file"""
  import pickle
  if indict:                     # store available data
    dictfile=open(ffile,'w')
    pickle.dump(indict,dictfile)
    dictfile.close()
  newdict=open(ffile,'r')	 # read file data into a python dictionary
  outdict=pickle.load(newdict)
  newdict.close()
  return outdict
  
  

