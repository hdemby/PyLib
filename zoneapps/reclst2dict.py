## get domain records:
mysql:
> select * from %domain where rdtype="A" into outfile "/tmp/recs_%domain.csv" fields terminated by "\t" lines terminated by "\n";

dig:
> dig -t axfr %domain > /tmp/recs_%domain.csv

python:
import re,sys,os
indata=open("/tmp/itcc_records",'r').readlines()

## static data:
ISAREC=re.compile("(\s)A(\s)")
testlst="""
cc153.itcc.unc.edu. 	86400 	IN 	A 	152.2.80.153
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
arecs=[s for s in indata if ISAREC.search(s)]

testsubdict={'recs': ['addm.itcc.unc.edu.\t86400\tIN\tA\t152.19.141.196\n']}
testdict={'152.19.141': testsubdict}

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

def splitIPv4(ipv4addr):
    """return the subnet and IP address from an IPv4 address"""
    assert type(ipv4addr)==type(""), "input must be 'string' type"
    subnet,ip=ipv4addr.rsplit(".",1)
    return subnet,ip
#>>> ip="152.2.80.153"; assert(splitIPv4(ip)[0]=='152.2.80')


def getArecData(arec):
    """convert a list of DNS A records into a subnet list"""
    assert type(arec)==type(""), "input must be 'string' type"
    rec=arec.replace(" ","\t")
    while rec.find("\t\t") > -1:		#minspace
        rec=rec.replace("\t\t","t")
    return rec.strip().split("\t")
#>>> arec=arecs[0];assert(getArecData(arec)=="152.19.141.196")


def addDictKey(rec):
    """add a key and initial to the container dictionary"""
    assert type(rec)==type(""), "input must be 'string' type"
    snet,ip=splitIPv4(getArecData(rec))
    if DEBUG: 
        print "adding new key '%s'"%snet
        raw_input("continue...")
    return {snet:{'recs':[minspace(rec).strip()]}}
#>>> arec=arecs[0];assert('152.19.141' in addDictKey(arec).keys())


def appendRecLst(data,recdict):
    """add a record to a dict"""
    assert type(data)==type(""), "input must be 'string' type:  'appendDictLst('',{},'')' "
    assert recdict.has_key('recs'), "'dict' must have key 'recs'"
    recdict['recs'].append(data)
    return recdict
#>>> arec=arecs[0];oldlen=len(testsubdict['recs']);assert(len(appendRecLst(arec,testsubdict)['recs'])==oldlen+1)


def procRec(rec,indict):
    """add a record to the proper dictionary hash"""
    assert type(rec)==type(""), "'rec' must be 'string' type:  'procRec("",{})' "
    assert type(indict)==type({}), "'indict' must be 'dict' type:  'procRec("",{})' "
    outdict=indict
    snet=splitIPv4(getArecData(rec))[0]
    if snet in outdict.keys():
        outdict[snet].update(appendRecLst(rec,outdict[snet]))
    else:
        outdict.update(addDictKey(rec))
    return outdict
#>>> refdict={};arec=arecs[0];assert('152.19.141' in procRec(arec,refdict).keys())

def main(reclist):
    """report the subnets associated with a DNS domain"""
    subnets={}
    for rec in arecs:
        if DEBUG > 1: print "processing %s..."%rec
        subnets=procRec(rec,subnets)
        if DEBUG: subnets.keys()
    return subnets

if __name__=="__main__":
    if sys.argv[1]:
        try: areclst=open(sys.argv[0],'r').readlines()
        except: print("using test data...")
    subnets=main(areclst)
    print "Subnets in domain: ",subnets.keys()
    for key in subnets:
        print "subnet: %s,\tsize: %s"%(key,len(subnets[key]['recs']))
    return






