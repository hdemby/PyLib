#!/usr/bin/env python

"""
a library of functions to manipulate IPv4 Hostnames

"""

def getname(nodestr):
    """return the 'name' part of a FQDN string:

    USAGE: getname("name.root.ext") ==> "name"

    """
    assert len(nodestr.split(".")) > 2
    return nodestr.split(".",1)[0]

def getroot(nodestr):
    """return the 'root' part of a FQDN string:

    USAGE: getroot("name.root.ext") ==> "root.ext"

    """
    assert len(nodestr.split(".")) > 2
    return nodestr.split(".",1)[-1]

def setname(nodestr,newname):
    """return the FQDN with a new name:
    
    USAGE: setname("name.root.ext","newname") ==> "newname.root.ext"

    """
    assert len(nodestr.split(".")) > 2
    assert type(newname)==type("")
    oldname,root=nodestr.split(".",1)
    return "%s.%s"%(newname,root)

def setroot(nodestr,newroot):
    """return the FQDN with a new root:

    USAGE: setroot("name.root.ext","branch.org") ==> "name.branch.org"

    """
    assert len(nodestr.split(".")) > 2
    assert type(newroot)==type("")
    name,oldroot=nodestr.split(".",1)
    return "%s.%s"%(name,newroot)

