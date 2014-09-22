#!/usr/bin/env python

import getDomainSubnets
import sys,os

DEBUG=1

if __name__=="__main__":
    """get the current DNS arecords for a domain and """
    try:
        if sys.argv[1]:
            domdict={'dom':sys.argv[1]}
            allrecs=os.popen("dig -t axfr %(dom)s"%domdict,'r').readlines()
            arecs=[s for s in allrecs if getDomainSubnets.ISAREC.search(s)]
            domdict.update({'arecs':arecs,'len':len(arecs)})
            if DEBUG: print "processing %(len)s records...for '%(dom)s'"%domdict
    except IOError:
        print "domain requested was not resolvable, good bye!"
        sys.exit(1) ## replace this with a routine to get the data from the parent domain
    try:
        subnets=getDomainSubnets.getsubnets(arecs)
        domdict.update({'subnets':subnets,'numnets':len(subnets)})
    except:
        print "Sorry, no go" 
        sys.exit(2)

    if int(domdict['numnets'])<1:
        print "Sorry, this domain is un-resolvable in DNS; No records to report. Bye!"
        sys.exit(0)
    else:
        print "There are %(numnets)s in Subnets in the %(dom)s domain."%domdict
    if raw_input("Show list?[y,N]: ") in ['y','Y']:
        print subnets.keys()
    if raw_input("\nShow records per subnet?[y,N]: ") in ['y','Y']:
        for key in sorted(subnets):
            print "subnet: %s\trecords: %s"%(key,len(subnets[key]['recs']))

    while True:
        if raw_input("examine subnet records?[y,N]: ") in ['y','Y']:
            snet=raw_input("which subnet: ")
            if snet:
                print "subnet %s:"%snet
                print getDomainSubnets.render(subnets[snet]['recs'])
        else:
            break

     if raw_input("View graphic summary of domain subnets?[y,N]: ") in ['y','Y']:
         ## add histogram display of #zones vs. #records for domain
         pass





