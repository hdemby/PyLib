#!/usr/bin/env python
"""
asciigraph.python

Plot data in a console terminal

"""
import os
import DataTools as dt

## method 1:
#- create a list of values for records in a subnet for subnets in the list
#- convert the list into a frequency dictionary
#- display the frequency dictionary

def val2txtplot(val,mark="*"):
    """represent val in ascii characters"""
    return "%s"%mark*int(val)
#>>> val=10;assert(val2txtplot(val)=='**********')

def plotfill(valstr,fscale=70):
    """fill a string to full scale dimensions"""
    return (valstr+" "*fscale)[:fscale]
#>>> chkval='********************                                        '
#>>> fscale=60;valstr='********************'; assert(plotfill(valstr,fscale)==chkval)

def formatrow(head,plot,foot):
    """format a plotted row"""
    return [head,plot,foot]
#>>> head="001|"; foot=" :20"; plot='********************          '
#>>> assert(formatrow(head,plot,foot)==['001|', '********************          ', ' :20'])

def freqDict2HistGraph(freqdict,rowhead="",rowfoot="",fscale=70):
    """return a matrix of ascii plotted rows"""
    plotlst=[]
    valmax=max(freqdict.values())
    sf=(valmax<=fscale) and 1 or fscale/(valmax*1.0)
    for row in sorted(freqdict.keys(),key=int):
        head=rowhead and rowhead%row or ""
        foot=rowfoot and rowfoot%freqdict[row] or ""
        plot=plotfill(val2txtplot(freqdict[row]*sf),fscale)
        plotlst.append(formatrow(head,plot,foot))
    return plotlst
#>>> freqdict={1:4,2:3,3:2,4:1}; 
#>>> assert(freqDict2HistGraph(freqdict,fscale=10)==[['', '****      ', ''], ['', '***       ', ''], ['', '**        ', ''], ['', '*         ', '']])
#>>> head="%3s|"; foot=": %s"
#>>> assert(freqDict2HistGraph(freqdict,head,foot,fscale=10)==[['  1|', '****      ', ': 4'], ['  2|', '***       ', ': 3'], ['  3|', '**        ', ': 2'], ['  4|', '*         ', ': 1']])

if __name__=="__main__":
    ## get subnet record counts as a list:
    rawdatalst=open("../zoneapps/subnetvals.data",'r').readlines()
    print len(rawdatalst)
    numvals=[s.strip().split(" ")[-1] for s in rawdatalst]

    ## create a numval dict: {'categ':#found}:
    numdict=dt.lst2FreqDict(numvals)

    ## graph the frequency data:
    print "Graph from frequency data as dictionary"
    matrix=freqDict2HistGraph(numdict,"%3s|"," :%s",70)
    print dt.arrayrender(matrix)
	
	


