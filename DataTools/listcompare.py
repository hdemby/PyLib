#!/usr/bin/env python
"""
listCompare.py

compate the contents of two similar lists


"""

def basicListdiff(listA,listB):
    """ return a list of 'basic' matching items from listA not found in similar listB:
            
        ex. listdiff(listA,listB) => []

    """
    missing=[]
    for each in listA:
        found=0
        name=each.split(" ",1)[0]
        for other in listB:
            if name in other.split(" "):
                found=1
                break
            else:
                pass
        if not found:
            missing.append(each)
            found=0
    return missing



#>>> listA=['a','b','c','d','e','f']; listB=['a','b','c','d']; assert(listdiff(listA,listB)==['e','f']),"failed!"
#>>> listA=['a','b','c','d','e']; listB=['a','b','c','d','e']; assert(listdiff(listA,listB)==[]),"failed!"

