#!/usr/bin/env python
"""
                        getDomainSubnets.py

## methods to create record files: subnets and IP 'A' records associated with a domain:

(1) mysql:
> select * from %domain where rdtype="A" into outfile "/tmp/recs_%domain.csv" fields terminated by "\t" lines terminated by "\n";

(2) dig:
> dig -t axfr %domain > /tmp/recs_%domain.csv


USAGE: getDomainSubnets.py /tmp/recs_%domain.csv

"""
import re,sys,os

## static data:
ISAREC=re.compile("(\s)A(\s)")

testlst="""
cc153.itcc.unc.edu.	86400	IN	A	152.2.80.153
dev.itcci.fpg.unc.edu.	86400	IN	CNAME	kubrick.fpgsm.unc.edu.
qa.itcci.fpg.unc.edu.	86400	IN	CNAME	hagrid.fpgsm.unc.edu.
addm.itcc.unc.edu.	86400	IN	A	152.19.141.196
addm-dev.itcc.unc.edu.	86400	IN	A	152.19.141.197
addm-esx.itcc.unc.edu.	86400	IN	A	152.19.141.195
addmwindis.itcc.unc.edu. 86400	IN	A	152.19.141.194
bronco.itcc.unc.edu.	86400	IN	CNAME	cc141.itcc.unc.edu.
cacti.itcc.unc.edu.	86400	IN	A	152.19.141.201
cams.itcc.unc.edu.	86400	IN	A	152.2.80.110
cc-matrix8.itcc.unc.edu. 86400	IN	CNAME	cc166.itcc.unc.edu.
cc100.itcc.unc.edu.	86400	IN	A	152.2.80.100
cc101.itcc.unc.edu.	86400	IN	A	152.2.80.101
cc102.itcc.unc.edu.	86400	IN	A	152.2.80.102
cc107.itcc.unc.edu.	86400	IN	A	152.2.80.107
cc108.itcc.unc.edu.	86400	IN	A	152.2.80.108
cc109.itcc.unc.edu.	86400	IN	A	152.2.80.109
""".split("\n")
arecs=[s for s in testlst if ISAREC.search(s)]

testsubdict={'recs': ['addm.itcc.unc.edu.\t86400\tIN\tA\t152.19.141.196\n']}
testdict={'152.19.141': testsubdict}

DEBUG=0

##functions:
render=lambda a:"".join("%s"%s for s in a)
rendern=lambda a:"\n".join("%s"%s for s in a)

subnets={}
rectags=['host','ttl','cls','typ','data']

def minspace(string):
    """remove excess spaces from a line of text"""
    string=string.replace(" ","\t")
    while string.find("\t\t")>-1:
        string=string.replace("\t\t","\t")
    return string
#>>> string="this  is	a      sloppy string."; assert(minspace(string)=="this\tis\ta\tsloppy\tstring.")

def recLstByType(inlst,rtype='A'):
    """return a list containing only items with 'sel' included"""
    import re
    return [s for s in inlst if re.compile("\t%s\t"%rtype).search(s)]
#>>> inlst=testlst;assert(recLstByType(inlst,rtype='A')[-1]=='cc109.itcc.unc.edu.\t86400\tIN\tA\t152.2.80.109')

def splitIPv4(ipv4addr):
    """return the subnet and IP address from an IPv4 address"""
    assert type(ipv4addr)==type(""), "input must be 'string' type"
    subnet,ip=ipv4addr.rsplit(".",1)
    return subnet,ip
#>>> ip="152.2.80.153"; assert(splitIPv4(ip)[0]=='152.2.80')

## DBC functions:
ISVALID=lambda a:True and len(a.strip().split(":"))==3 or False

def snetrptline2num(lline):
    """extract the number of records from the subnet records report line"""
    assert ISVALID(lline), "miss configured data line: '%s'"%lline
    lline=lline.strip()
    return int(lline.strip().split(" ")[-1])
#>>> lline="subnet: 152.19.150  records: 54"; assert(snetrptline2num(lline)==54)


def getArecData(arec):
    """return the ip address from an 'A' record"""
    assert type(arec)==type(""), "input must be 'string' type"
    return minspace(arec).strip().split("\t")[-1]
#>>> arec=arecs[0];assert(getArecData(arec)=="152.19.141.196")


def procRec(rec,indict):
    """add a record to the proper dictionary hash"""
    assert type(rec)==type(""), "'rec' must be 'string' type:  'procRec("",{})' "
    assert type(indict)==type({}), "'indict' must be 'dict' type:  'procRec("",{})' "
    outdict=indict
    snet=splitIPv4(getArecData(rec))[0]
    if snet in outdict.keys():
        outdict[snet]['recs'].append(rec)
    else:
        outdict[snet]={'recs':[rec]}
    return outdict
#>>> refdict={};arec=arecs[0];assert('152.19.141' in procRec(arec,refdict).keys())

def getsubnets(reclist):
    """report the subnets associated with a DNS domain"""
    assert type(reclist)==type([]), "input must be a tab delimited 'list' type:  'main([csv_list])' "
    subnets={}
    for rec in reclist:
        if DEBUG > 1: print "processing %s..."%rec
        try:
            subnets=procRec(rec,subnets)
        except:
            print "could not process %s"%rec
        if DEBUG: subnets.keys()
    return subnets
#>>> reclist=arecs;assert(getsubnets(reclist).keys()==['152.19.141', '152.2.80'])

def getDigRecs(domain,svr='152.2.21.1'):
    """return the records in a DNS domain or subdomain"""
    digrecs=os.popen("dig -t axfr %s @%s"%(domain,svr),'r').readlines()
    if len(digrecs)<=4:
        digrecs=os.popen("dig -t axfr %s @%s | grep %s"%(domain.split(".",1)[1],svr,domain),'r').readlines()
    return digrecs
#>>> import os; domain="itcc.unc.edu";assert(getDigRecs(domain)==os.popen("dig -t axfr unc.edu | grep 'itcc.unc.edu'",'r').readlines()))

def main(reclist):
    return getsubnets(reclist)
    

if __name__=="__main__":
    try:
        if sys.argv[1]:
            digrecs=getDigRecs(sys.argv[1]) # this should be a function to handle subdomains
            arecs=[s for s in digrecs if ISAREC.search(s)]
            print "processing %s records..."%(len(arecs))
    except IndexError, IOError: 
        if raw_input("use test data?: ") in ['y','Y']:
            print ("processing test data; %s records..."%len(arecs))
        else:
            print "good bye!"
            sys.exit(1)
    except ValueError:
        print "%s records found. Insufficient for analysis. Aborting."
        sys.exit(1)
    subnets=main(arecs)
    print "Subnets in domain: ",subnets.keys()
    for key in subnets:
        print "subnet: %s\tsize: %s"%(key,len(subnets[key]['recs']))







