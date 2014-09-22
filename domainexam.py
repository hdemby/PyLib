#!/usr/bin/env python
"""
domSnetRecRpt.py : domain subnet records report summary

returns a frequency graph of the records/subnet related a DNS domain 

USAGE: ./domSnetRecRpt.py {FQdomain}

ex. ./domSnetRecRpt.py unc.edu

"""
import DataTools.asciigraphv2 as graph
import DataTools.DataTools as dt
import zoneapps.getDomainSubnets as gds

if __name__=="__main__":
    """show a graph of subnets associated with the given domain by number of records in the domain"""

    import sys

    ## get 'domain' records:
    try:
        domain=sys.argv[1]
        zonerecs=gds.getDigRecs(domain)
    except IndexError:
        print "USAGE: python ./domainexamine.py {domain}"
        sys.exit(1)
    ## get zone Arecs:
    arecs=gds.recLstByType(zonerecs)
    if len(arecs)<1:
        print("no data to report. Aborting.")
        sys.exit(1)

    ## process domain arecs into subnetsdict:
    snetdict={}
    for rec in arecs:
        snet,ip=gds.splitIPv4(gds.getArecData(rec))
        try:
            snetdict[snet]['recs'].append(rec)
        except KeyError:
            snetdict.update({snet:{'recs':[rec]}})

    print "Domain: %s\tsubnets: %s"%(domain,len(snetdict.keys()))

    ## PLOTTING:
    if raw_input("plot #records/subnet in domain?[y,N]: ") not in ['y','Y']:
        print "bye!"
        sys.exit(0)

    ## process snetdict into reclst:
    countlst=[]
    for snet in snetdict.keys():
        countlst.append(len(snetdict[snet]['recs']))

    ## generate plotting data from freqdict:
    countdict=dt.lst2FreqDict(countlst)

    ## plot the data:
    print "\nDomain: '%s'"%domain
    print " - number of subnets: \t%s"%len(snetdict.keys())
    print " - max records in a subnet: \t%s"%(max(countlst))
    title="\nNumber of Records Found in subnets for the '%s' domain:\n"%domain
    print "%s"%title+"="*len(title)
    header="#recs| times found\n"+"----+"+"-"*75
    print header
    matrix=graph.freqDict2HistGraph(countdict,"%3s|"," :%s",70)
    print dt.arrayrender(matrix)
    print

    if raw_input("view number of records per subnet?[y,N]: ") not in ['y','Y']:
        print "bye!"
        sys.exit(0)
    else:
    ## create a dict of subnets in each count category:
        cntsnetsdict={}
        for snet in snetdict.keys():
            reccnt=len(snetdict[snet]['recs'])
            print "%s:\t%s"%(snet,reccnt)

    ## collect subnets for each countdict key:
            try:
                cntsnetsdict[eval("%s"%reccnt)]['snets'].append(snet)
            except KeyError:
                cntsnetsdict.update({eval("%s"%reccnt):{'snets':[snet]}})

        if raw_input("view specific records per subnet?[y,N]: ") not in ['y','Y']:
            print "bye!"
            sys.exit(0)
        else:
            for key in cntsnetsdict.keys():
                for snet in cntsnetsdict[key]['snets']:
                    print "subnet:%s\trecords:%s"%(snet,len(snetdict[snet]['recs']))
                    print dt.render(snetdict[snet]['recs'])
                    print "--------"

    ## allow examination of specific data points:
            while True:
                if raw_input("examine subnets in a count category?[y,N]: ") not in ['y','Y']:
                    print "bye!"
                    sys.exit(0)
                else:
                    cntcat=raw_input("which count category?[#val]: ")
                    try:
                        cntcat=int(cntcat)
                    except ValueError:
                        cntcat=cntcat
                print "count category '%s':"%cntcat
                if cntcat not in countdict.keys():
                    print "categories are:"
                    print countdict.keys()
                    print "Try again..."
                    continue
             
                while True:
                    print cntsnetsdict[eval("%s"%cntcat)]
                    if raw_input("examine records in a subnet?[y,N]: ") not in ['y','Y']:
                        print "bye!"
                        break
                    else:
                        snet=raw_input("which subnet?: ")
                        if snet not in snetdict.keys():
                            print "subnets are:"
                            print snetdict.keys()
                            print "Try again ..."
                            continue
                        else:
                            print dt.render(snetdict[snet]['recs'])
                            print "%s records shown for '%s'\n\n"%(len(snetdict[snet]['recs']),snet)



