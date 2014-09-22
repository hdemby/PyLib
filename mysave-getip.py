#!/usr/bin/env python
"""
getip.py
 notify by mail when router IP address changes
"""

import os,time,smtplib
from keis import *

DEBUG=1
WEBIP="http://web2mamba.net.unc.edu/getip"
IPFILE="/home/hdemby/getip"
REFFILE="/home/hdemby/_getip"
LOGFILE="/home/hdemby/ip.log"

tto=["hdemby@unc.edu","hdemby41@gmail.com"]
recvrs=",".join("%s"%s for s in tto)
ffrom="hdemby@email.unc.edu"
subj="IP address change report"
parms={'ffrom':ffrom,'tto':tto,'subj':subj,'recvrs':recvrs}

mesg="""
From: Hiawatha Demby <%(ffrom)s>
To: %(tto)s
Subject: %(subj)s



This should be a messsage to me with a subject.

"""%parms

def sendIP(ipinfo):
  "send the IP change report"
  s=smtplib.SMTP('localhost')
  s.sendmail(ffrom,tto,mesg)

  server = smtplib.SMTP('smtp.unc.edu:587')
  username='hdemby'  
  password=HDEMBY  
  server.ehlo()
  server.starttls()  
  server.login(username,password)
  mesg+="%s:new IP: %s\n"%(time.ctime(),ipinfo)
  mesg+="\nGoto <http://dembyville.com/cpanel>"
  try:  
    server.sendmail(ffrom, tto, mesg)         
    server.quit()
    logIPchange("%s:new IP: %s\n"%(time.ctime(),ipinfo))
    print "successfully sent!"
  except:
    print "mail did not go"

def logIPchange(report):
  "log the IP change"
  try:
    log=open("%s"%LOGFILE,'a')
    log.write("%s\n"%report)
    log.close()
  except:
    print "could not write to log"
  return

def checkIP():
  "see if IP address has changed"
  os.system("wget %s"%WEBIP)
  ans=os.popen("/usr/bin/diff %s %s"%(IPFILE,REFFILE),'r').readlines()
  return ans

if __name__=="__main__":
  "do IP check"
  try:
    os.system("mv %s %s"%(IPFILE,REFFILE))
    checkIP()
    print "IP checked"
  except IOError:
    pass
  except:
    print "serious error. IP not assessed"

