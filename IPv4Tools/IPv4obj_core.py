#!/usr/bin/env python

"""
Name: IPv4obj_core.py
version: 1.0; H. Demby 09/12/2014

Description: a library of functions to manipulate IPv4 addresses of the form: 'aaa.bbb.ccc.ddd'

Notes:
- 'aaa','bbb','ccc','ddd' represent numeric values between 0-255


"""

def getNetAndIP(ipstr):
    """return the 'name' part of a FQDN string:

    USAGE: getNetAndIP("aaa.bbb.ccc.ddd") ==> ["aaa.bbb.ccc","ddd"]

    """
    assert len(ipstr.split("."))==4,"input is not a valid IPv4 string"
    return ipstr.rsplit(".",1)
#>>> ipstr='192.168.0.1'; assert(getNetAndIP(ipstr)==["192.168.0","1"])

def ipToARPA(ipstr):
    """return 'in-addr.arpa' form of the IP address:
    
    USAGE: ipToARPA(aaa.bbb.ccc.ddd) ==> "ddd.ccc.bbb.aaa.in-addr.arpa."
    
    """
    assert len(ipstr.split("."))>=1,"Input IPaddress string must be a subset of 'aaa[.bbb[.ccc[.ddd]]]'."
    return ".".join("%s"%s for s in ipstr.split(".")[::-1])+".in-addr.arpa."
#>>> ipstr='192.168.0'; assert(ipToARPA(ipstr)=="0.168.192.in-addr.arpa.")

def fillIP(ipval):
    """return an IP value as a 3 digit number string between (0-255):

    USAGE: fillIP('#') ==> "00#"
    
    """
    assert type(ipval)==type(""),"input must be a string"
    assert ipval.isdigit(),"ip must be a numeric integer"
    assert len(ipval)<=3, "ipaddress string limited to 3 digits"
    assert eval(ipval)<=255, "ip address value is greater than '255'"
    numstr="0000"+ipval
    return numstr[-3:]
#>>> ipval='2';assert(fillIP(ipval)=='002')

def ipToDec(ipstr):
    """return IP address as a 12 digit integer:

    USAGE: ipToDec("111.222.33.4") ==> 111222033004

    """
    assert type(ipstr)==type(""),"input must be a string"
    assert len(ipstr.split("."))==4,"Input IPaddress string must be in the form 'aaa.bbb.ccc.ddd'."
    fullipstr=""
    for ip in ipstr.split("."):
        fullipstr+=fillIP(ip)
    return eval(fullipstr)
#>>> ipstr='192.168.0.1'; assert(ipToDec(ipstr)==192168000001L)




