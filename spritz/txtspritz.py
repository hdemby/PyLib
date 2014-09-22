#!/usr/bin/env python

import sys,time,os
import txt2wrdlst as txw

##=========##
##  model  ##
##=========##
##==========##
## control  ##
##==========##
##======##
## VIEW ##
##======##
MAXWIDTH=30  # width of charaster display
XPOS=10      # start how far down
YPOS=15      # start how far to the right
WAIT=.12     # word display frequency
PWAIT=2      # end of sentence('.') pause multiplier

##----------------------------------------------
## Functions for console display of 'word list':
##----------------------------------------------

##if os.name=="nt":os.system('cls');else:os.system('clear')
cls=lambda :os.name=="nt" and os.system('cls') or os.system('clear')

def center(word,maxw=MAXWIDTH):
    """center a word in a space"""
    wwidth=len(word)
    pads=maxw-wwidth
    rpad=" "*(pads/2)
    lpad=rpad
    word=rpad+word+lpad
    return word

def frameWord(word,x=XPOS,y=YPOS):
    """create a frame for the output"""
    frame="\n"*(x-1)
    frame+="=============================|"+"="*(30+4)+"\n\n" 
    frame+=" "*y
    frame+="%s\n\n"%center(word)
    frame+="=============================|"+"="*(30+4)
    return frame
    
def showWord(word,pause=WAIT):
    """show a word for a period of time"""
    ans=0
    os.name==cls()
    try:
        sys.stdout.write(frameWord(word))
        sys.stdout.flush()
        if "." in word:
            pause=pause*PWAIT
        time.sleep(pause)
        ans=0
    except IOError:
        print "failed to display"
        ans=1
    return ans

def txtpause():
    ans=raw_input("press 'Enter' to continue:")
#    while True:
#        if sys.stdin.read(1)!=" ":
#           continue
    return
    
if __name__=="__main__":
    "test code for text to list application"
    import sys
    import getchar
    
    inchar=getchar._Getch()
    if len(sys.argv)>1:
        ffile=sys.argv[-1]
    else:
        ffile=True and raw_input("convert what file to a word list?: ") or "./networktext.txt"
    wordlst=txw.main(ffile) #raw_input("convert what file to a word list?: "))
    for word in wordlst:
        showWord(word)
#       Check for key command:
#        *** options appear to be limited to 'Tkinter' and 'mscrt' functions
#            key=inchar()
#            if key=='p':
#                raw_input("PAUSE")
#                key=''
                   
    print("\n\nFini!")

