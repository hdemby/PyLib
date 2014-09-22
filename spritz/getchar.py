#!/usr/bin/env python

##================================
##  'sys,tty' and 'mscrt' methods
##================================

class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()
#
    def __call__(self): 
        char = self.impl()
        if char == '\x03':
            raise KeyboardInterrupt
        elif char == '\x04':
            raise EOFError
        return char

class _GetchUnix:
    def __init__(self):
        import tty
        import sys
#
    def __call__(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt
#
    def __call__(self):
        import msvcrt
        return msvcrt.getch()

def dokeys():
    mykey=Getch()
    while True:
        key=mykey()
        if (key!='q'):
            sys.stdout.write(key)
        else:         
            print
            break
#>>> dokeys()

##=========================
##  Tkinter method
##=========================
import Tkinter as tk

class Keypress:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('30x20')
        self.root.bind('<KeyPress>', self.onKeyPress)
#
    def onKeyPress(self, event):
        import sys
        cmds={'r':'this is a report','p':'this is a pause'}
        self.key = event.char
        exec(cmds[self.key])
#
    def __eq__(self, other):
        return self.key == other
#
    def __str__(self):
        return self.key

if __name__=="__main__":
    getch = Keypress()
    getch.root.mainloop()


    
