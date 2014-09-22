#!/usr/bin/env python
"""
        spritztool.py

This program creates a GUI interface for a speed reading application

The module is called with a wordlist created from a '*.txt' file.

Usage: ./spritztool.py ./{filename.txt}

"""

from Tkinter import *
from ScrolledText import *
import string,os,sys,time

DEFAULTFILE="./spritzterms.txt"
DEBUG = 0
ERROR = ""

class SpritzReader( Frame ):
    """ This class opens a frame to read a word list"""
    def __init__(self,myfile):
        Frame.__init__(self)
        self.master.title("Spritz Style Text Reader")
        self.pack()
        self.varWord = StringVar()
        self.ERROR = ""
        self.myfile=DEFAULTFILE
        self.wordlst=[]
        self.addWidgets()
        
    def addWidgets(self):
        """ Places widgets in the application main frame """
        ## text panel
        txp=0
        self.txtpanel=Frame(self)
        self.txtpanel.grid(row=txp,column=0)
        self.varWord.set("          document           ")
        self.docText=Label(self.txtpanel,text=self.varWord.get(),font=("Arial",22),bg="black", fg="white",command=None)
        self.docText.grid(row=0,column=0,)

        ## user controls
        btp=1
        self.btnpanel=Frame(self)
        self.btnpanel.grid(row=btp,column=0)
        self.btnLoad=Button(self.btnpanel,text="Load",command=None,state=NORMAL)
        self.btnLoad.grid(row=1,column=0)
        self.btnStart=Button(self.btnpanel,text="Start",command=None,state=NORMAL)
        self.btnStart.grid(row=1,column=1)
        self.btnPause=Button(self.btnpanel,text="Pause",command=None,state=NORMAL)
        self.btnPause.grid(row=1,column=2)
        self.btnSave=Button(self.btnpanel,text="Save",command=None,state=NORMAL)
        self.btnSave.grid(row=1,column=3)
        self.btnQuit=Button(self.btnpanel,text="Quit",command=None,state=NORMAL)
        self.btnQuit.grid(row=1,column=4)

    
def main(filename=DEFAULTFILE):
    reader=SpritzReader(filename)
    reader.mainloop()
    
if __name__=="__main__":
    try:
        main(sys.argv[1])
    except:
        main()


