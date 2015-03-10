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

SRCFILE = "./dhcpd.conf"

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

def main(mac, infile=SRCFILE):
    """run macinfile"""
    try:
        mac = leasemac(mac)
    except:
        raise ValueError, "USAGE: ./macinconf.py {1C0ACADDRE55} [alt-file]"
    srcdata = open(infile,'r').read()
    if chkformac(mac, srcdata):
        print "found '%s' in '%s'" % (mac, infile)
    else:
        print "did not find '%s' in '%s'" % (mac, infile)
    return

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])


test_code="""
lesefil="./dhcpd.leases"
confile="./dhcpd.conf"
leselst=open("./dhcpd.leases",'r').readlines()
conflst=open("./dhcpd.conf",'r').readlines()
lesemacs=[s.split(" ")[-1][:-1] for s in leselst if re.compile("hardware ethernet").search(s)]
confmacs=[s.split(" ")[-1][:-1] for s in conflst if re.compile("hardware ethernet").search(s)]
len(lesemacs)
len(conf1macs)
leseset=set(lesemacs)
confset=set(confmacs)
print set(lesemacs),len(leseset)
print set(confmacs),len(confset)
print list(leseset.intersection(confset))
print len(leseset.intersection(confset)), len(confset.intersection(leseset))
print list(leseset)[0]
print sorted(list(leseset))[0]
print sorted(list(leseset),reverse=True)[0]
"""

    



