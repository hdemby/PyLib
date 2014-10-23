#!/usr/bin/env python
"""
                        getSubnetDomains.py

## methods to create record files: subnets and IP 'PTR' records associated with a subnet:

(1) mysql:
> select * from %zone_tbl where rdtype="PTR" into outfile "/tmp/recs_%subnet.csv" fields terminated by "\t" lines terminated by "\n";

(2) dig:
> dig -t axfr %zone > /tmp/recs_%subnet.csv


USAGE: getSubnetDomains.py /tmp/recs_%domain.csv

"""
import re,sys,os

## static data:
ISPTR=re.compile("(\s)PTR(\s)")

testlst="""
152.2.145.40      in      ptr     titan.net.unc.edu.
152.2.145.41      in      ptr     asafoetida.net.unc.edu. ;sstafford
152.2.145.42      in      ptr     paprikash.net.unc.edu.  ;sstafford
152.2.145.43      in      ptr     airwave-vm-test.net.unc.edu.    ;florio
152.2.145.44      in      ptr     demeter.net.unc.edu.
152.2.145.45      in      ptr     redman.net.unc.edu.
152.2.145.46      in      ptr     roger.net.unc.edu.      ;sstafford
152.2.145.47      in      ptr     delgado.net.unc.edu.    ;sstafford
152.2.145.48      in      ptr     eduroam1.net.unc.edu.   ;sstafford
152.2.145.49      in      ptr     eduroam2.net.unc.edu.   ;stafford
152.2.145.50      in      ptr     fits-hp-lj2200.net.unc.edu.
152.2.145.51      in      ptr     fits-hp-lj2200dn.net.unc.edu.
152.2.145.52      in      ptr     archie.net.unc.edu.     ;sstafford
152.2.145.53      in      ptr     betty.net.unc.edu.
;;152.2.145.54    in      ptr     veronica.net.unc.edu.
152.2.145.55      in      ptr     jughead.net.unc.edu.
152.2.145.56      in      ptr     moose.net.unc.edu.
152.2.145.57      in      ptr     atlantic.net.unc.edu.   ;sstafford
152.2.145.58      in      ptr     pacific.net.unc.edu.    ;sstafford
152.2.145.59      in      ptr     jerry.net.unc.edu.      ;sstafford
""".split("\n")
arecs=[s for s in testlst if ISPTR.search(s)]

testdomdict={'recs': ['152.19.141.196\t86400\tIN\tPTR\taddm.itcc.unc.edu.\n']}
testdict={'itcc.unc.edu': testdomdict}

DEBUG=0

##functions:
render=lambda a:"".join("%s"%s for s in a)
rendern=lambda a:"\n".join("%s"%s for s in a)

subnets={}
rectags=['host','ttl','cls','typ','data']

##==================
## common functions:
##==================
def minspace(string):
    """remove excess spaces within a line of text"""
    string=string.replace(" ","\t")
    while string.find("\t\t")>-1:
        string=string.replace("\t\t","\t")
    return string
#>>> string="this  is	a      sloppy string."; assert(minspace(string)=="this\tis\ta\tsloppy\tstring.")

def recLstByType(inlst,rtype='PTR'):
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


def getRecData(rec):
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


##================================
## application specific functions
##================================
def get_domains(reclist):
    """report the subnets associated with a DNS domain"""
    assert type(reclist)==type([]), "input must be a tab delimited 'list' type:  'main([csv_list])' "
    subnets={}
    for rec in reclist:
        if DEBUG > 1: print "processing %s..."%rec
        try:
            domains=procRec(rec,subnets)
        except:
            print "could not process %s"%rec
        if DEBUG: subnets.keys()
    return domains
#>>> reclist=arecs;assert(get_domains(reclist).keys()==['152.19.141', '152.2.80'])

def get_dig_recs(domain,svr='152.2.21.1'):
    """return the records in a DNS domain or subdomain"""
    digrecs=os.popen("dig -t axfr %s @%s"%(domain,svr),'r').readlines()
    if len(digrecs)<=4:
        digrecs=os.popen("dig -t axfr %s @%s | grep %s"%(domain.split(".",1)[1],svr,domain),'r').readlines()
    return digrecs
#>>> import os; domain="itcc.unc.edu";assert(getDigRecs(domain)==os.popen("dig -t axfr unc.edu | grep 'itcc.unc.edu'",'r').readlines()))

def main(reclist):
    return get_domains(reclist)
    

if __name__=="__main__":
    try:
        if sys.argv[1]:
            digrecs=get_dig_recs(sys.argv[1]) # this should be a function to handle subdomains
            arecs=[s for s in digrecs if ISPTR.search(s)]
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
    domains=main(arecs)
    print "Subnets in domain: ",domains.keys()
    for key in domains:
        print "subnet: %s\tsize: %s"%(key,len(domains[key]['recs']))







