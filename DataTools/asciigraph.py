#!/usr/bin/env python
"""
asciigraph.python

Plot data in a console terminal

"""
import os

## method 1:
#- create a list of values for records in a subnet for subnets in the list
#- convert the list into a frequency dictionary
#- display the frequency dictionary


## DBC functions:
ISVALID=lambda a:True and len(a.strip().split(":"))==3 or False

def snetrptline2num(lline):
    """extract the number of records from the subnet records report line"""
    assert ISVALID(lline), "miss configured data line: '%s'"%lline
    lline=lline.strip()
    return int(lline.strip().split(" ")[-1])
#>>> lline="subnet: 152.19.150  records: 54"; assert(snetrptline2num(lline)==54)

def incrDictVal(valdict):
    """increment the numeric value of a key"""
    return {valdict.keys()[0]:int(valdict[valdict.keys()[0]])+1}
#>>> valdict={'1':1}; assert(incrDictVal(valdict)=={'1':2})


def lst2FreqDict(vallst):
    """convert a list into a frequency hash"""
    freqdict={}
    for num in vallst:
        try:
            freqdict[num]+=1
        except KeyError:
            freqdict[num]=1
    return freqdict
#>>> vallst=[1,1,1,2,1,7,5,4,1,1,3,2,1,6,1,2,1,3]; assert(lst2FreqDict(vallst)[vallst[0]]==len([s for s in vallst if s==vallst[0]]))


def showVertChart(freqdict):
    """display ASCII histogram of frequency data"""
    for recs in sorted(freqdict):
        print "%3s:|"%recs,
        for snets in range(freqdict[recs]):
            print "*",
        print
    return
#>>> (no local test)

def showScaledVertChart(freqdict,res=60):
    """display ASCII histogram of frequency data"""
    res=res*1.0
    valmax=max(freqdict.values())   # max subnet count
    sf=(res/valmax)
    countmax=max(freqdict.keys())   # max recs in subnet
    for datapnt in sorted(freqdict):
        print "%3s:|"%datapnt,
        print "*"*int((freqdict[datapnt]*sf)),
        print "< %s"%freqdict[datapnt]
    return
#>>> (no local test)

## method 2:
#- plot scaled value into an array of points
#- accumulate array plots into plot array
#- display the array as text using arrayrender

def plotToArray(col,val,sf,res=60, char="*",rep=False):
    """create a character array representing the input value

    USAGE: plotToArray(col,val,sf,res=60, char="*",rep=False)
    """
    row=[]
    row.append("%3s:|"%col)
    for n in range(res):
        row.append((val*sf)>n and char or " ")
    if rep:    
        row.append(" :%s"%val)    
    return row
#>>> val=200; print "|%s|"%render(plotToArray(1,val,60.0/212))
#>>> val=200; print "|%s|"%render(plotToArray(val,rep=True))

render=lambda a:"".join("%s"%s for s in a)
rendern=lambda a:"\n".join("%s"%s for s in a)
arrayrender=lambda a:rendern(render(s) for s in a)

def arrayGraph(freqdict,res=60,char="*",rep=False):
    """generate 2 dimensional array for input data"""
    sf=max(freqdict.values())>res and (res*1.0)/max(freqdict.values()) or 1   # max subnet count
    matrix=[]
    for col in sorted(freqdict):
        matrix.append(plotToArray(col,freqdict[col],sf,res,char,rep))
    return matrix
#>>> print "\n".join("%s"%render(s) for s in arrayGraph(numdict,rep=True))


if __name__=="__main__":
    ## get subnet record counts as a list:
    rawdatalst=open("../zoneapps/subnetvals.data",'r').readlines()
    print len(rawdatalst)
    numvals=[snetrptline2num(s) for s in rawdatalst if ISVALID(s)]

    ## evaluate rejected lines:
    errorvals=[s for s in rawdatalst if not ISVALID(s)]
    errorvals
    [[c for c in s] for s in rawdatalst if not ISVALID(s)]
    print "\n".join("%s"%s for s in errorvals)

    ## prepare to display recs/zone frequency histogram:
    maxrecs=max(numvals)   ## maximum number of records in a zone

    ## create a numval dict: {'recs':zones}
    numdict=lst2FreqDict(numvals)
    maxnets=max(numdict.values())  ##maximum number of zones for category

    header="val | times found\n"+"----+"+"-"*75
    print "Raw Graph:\n=========="
    print header
    showVertChart(numdict)
    print
    print "Scaled Graph:\n============="
    print header
    showScaledVertChart(numdict,67)
    print
    print "Graph from Matrix plot"
    print header
    matrix=arrayGraph(numdict,rep=True)
    print "\n".join("%s"%render(s) for s in arrayGraph(numdict,rep=True))
	
	


