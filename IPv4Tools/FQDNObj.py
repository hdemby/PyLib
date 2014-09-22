#!/usr/bin/env python

import IPobj_core

class IPnodeObj:
    def __init__(self,nodestr):
        self.name=""
        self.root=""
        self.setname(nodestr)
        self.setroot(nodestr)

    def setname(self,nodestr):
        self.name=IPobj_core.getname(nodestr)
        return
    
    def setroot(self,nodestr):
        self.root=IPobj_core.getroot(nodestr)
        return

    def getname(self):
        return self.name
    
    def getroot(self):
        return self.root
    
  
