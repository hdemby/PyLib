#!/usr/bin/env python
"""  txt2wrdlst.py

This application converts and displays a text document as a sequence of words
in a console panel. The functions most useful to external applications are:

- getWordLst(lline)	: Generates a list of words from a line of text
- getLineLst(intext)	: parses a text file into a list of lines based on "\n"
- catLists(lists)	: Concatenates a array of list into a single list

"""

##=========##
##  model  ##
##=========##
DEFFILE="./networktext.txt"

##===========##
##  control  ##
##===========##
## Functions for translation of a text document to a word list:
def getWordLst(line):
    """ break down a line of text into a list of words """
    assert type(line)==type(""),"input must be a string"
    return line.strip().split(" ")
#>>> line='faults in IP networks and their locations. Rectifying such' 
#>>> assert(len(getWordLst(line))==9); assert(getWordLst(line)[-1]=="such"),"Broken!"

def getLineLst(intext):
    """return all sentences in a text file as a list"""
    assert type(intext)==type(""),"input must be a string"
    return intext.split("\n")
#>>> intext='faults in IP networks and their locations. Rectifying such'; assert(len(getLineLst(intext))==1),"Broken!"
#>>> intext='faults in IP networks and their locations.\n Rectifying such'; assert(len(getLineLst(intext))==2),"Broken!"

def catLists(llist):
    """concatenate the elements of a list array into a single list"""
    assert type(llist)==type([])
    w=[]
    for each in llist:
        w+=each
    return w
#>>> llist=[['faults', 'in', 'IP', 'networks', 'and', 'their', 'locations.'],[ 'Rectifying', 'such']]
#>>> assert(len(catLists(llist))==9),"Broken!"

##======##
## VIEW ##
##======##
## display for spritz output:

##========##
##  Demo  ##
##========##

def main(ffile):
    """convert file text into word list"""
    intext=open(ffile,'r').read()
    wordlst=catLists([getWordLst(s) for s in getLineLst(intext) if s])
    return wordlst

if __name__=="__main__":
    "test code for text to list application"
    import sys
    print "returns a word list extracted from the submitted file" 
    if len(sys.argv)>1:
        ffile=sys.argv[-1]
    else:
        ffile=True and raw_input("convert what file to a word list?( default:'%s'): "%DEFFILE) or DEFFILE
    wordlst=main(ffile) #raw_input("convert what file to a word list?: "))
    print wordlst



