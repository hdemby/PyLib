#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
macinfile.py
v0.1

Check for a 'regs.dhcp' MAC address in 'dhcpd.conf' or other specified file:

USAGE: ./macinconf.py {1C0ACADDRE55} [alt-file]

returns: 'found '1c:0a:ca:dd:fe:55:0f' in {file}'

20150223 pylint score: 10.00/10

"""

SRCFILE = "/etc/dhcp/dhcpd.conf"

def regmac(mac):
    """return the 'MAC address' field from 'regs.dhcp' record"""
    return len(mac.split(":")[1]) == 12 and mac.split(":")[1] or None
#>>>
#>>> 

def leasemac(macstr):
    """convert uppercase mac to dhcpe.leases format"""
    maclst = []
    while macstr:
        maclst.append(macstr[:2].lower())
        macstr = macstr[2:]
    newmac = ":".join("%s" % s for s in maclst)
    return newmac
#>>> macstr="DC86D8E48684"
#>>> assert(leasemac(macstr)=="dc:86:d8:e4:86:84"),"==> '%s'"%leasemac(macstr)

def chkformac(mac, srcdata):
    """scan srcdata for entered mac"""
    import re
    ans = re.compile(mac).search(srcdata)
    return ans and True or False

def main(parms):
    """run macinfile"""
    try:
        mac = parms[1]
    except IndexError:
        print "USAGE: ./macinconf.py {1C0ACADDRE55} [alt-file]"
    try:
        srcfile = parms[2]
    except IndexError:
        srcfile = SRCFILE
    srcdata = open(srcfile,'r').read()
    if chkformac(mac, srcdata):
        print "found %s in %s" % (mac, srcdata)
    else:
        print "did not find %s in %s" % (mac, srcdata)
    return

if __name__ == "__main__":
    import sys
    main(sys.argv)
    



