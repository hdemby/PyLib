#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""text for a 'keepalive' session function"""

import pygtk
pygtk.require('2.0')
import gtk

mesg=r"while true ; do echo -ne '\000'; sleep 300; done &"
clipboard = gtk.clipboard_get()

clipboard.set_text("%s"%mesg)
print "use 'Paste' to retrieve command"
clipboard.store()

## alternatives
#from subprocess import Popen, PIPE
#p = Popen(['xsel','-pi'], stdin=PIPE)
#p.communicate(input="%s"%mesg)
#
#def paste(str, p=True, c=True):
#    from subprocess import Popen, PIPE
#
#    if p:
#        p = Popen(['xsel', '-pi'], stdin=PIPE)
#        p.communicate(input=str)
#    if c:
#        p = Popen(['xsel', '-bi'], stdin=PIPE)
#        p.communicate(input=str)
#
#paste('Hello', False)    # pastes to CLIPBOARD only
#paste('Hello', c=False)  # pastes to PRIMARY only
#paste('Hello')           # pastes to both
#
#Notes:
#    -p works with the PRIMARY selection. That's the middle click one.
#    -s works with the SECONDARY selection. I don't know if this is used anymore.
#    -b works with the CLIPBOARD selection. That's your Ctrl + V one.

