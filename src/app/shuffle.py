#!/usr/bin/env python
# -*- coding: utf-8 -*-

#======================================================#
#    Author kru228, David Krutký                       #
#    Bachelors thesis                                  #
#    Desktop application for GTD Shuffle on Android    #
#                                                      #
#    Using - python 2.6                                #
#          - sqlite3                                   #
#          - Git 1.5.3.7 or higher                     #
#          - GitPython                                 #
#          - Python Nose                               #
#          - Mock by Michael Foord 0.5 or higher       #
#                                                      #
#======================================================#

from PyQt4 import QtCore, QtGui
import sys

from new import New
from projects import Projects
from scalendar import Scalendar
from inbox import Inbox
from next import Next
from contexts import Contexts
from complete import Complete
from sync import Synchronization

import buffer
from main import Shuffle
from models import Action, Project, Context

def main():
    app = QtGui.QApplication(sys.argv)

    app.db = "../../db/"
    #app.db = "../../../../android/db/"
    buffer.openConn(app)
    buffer.init_sql(app)
    buffer.init_buffer(app)
    
    app.newTab = New()
    app.projectTab = Projects()
    app.calendarTab = Scalendar()
    app.inboxTab = Inbox()
    app.nextTab = Next()
    app.contextTab = Contexts()
    app.completeTab = Complete()
    app.syncTab = Synchronization()
    app.inSync = False
    
    app.mainWindow = Shuffle(app)
    app.refresh = refreshApp
    app.refresh(app)
    app.syncTab.refresh_sync()
    
    app.mainWindow.show()
    
    sys.exit(app.exec_())
    
def refreshApp(app):
    app.newTab.refresh_new()
    app.projectTab.refresh_projects()
    app.calendarTab.refresh_calendar()
    app.inboxTab.refresh_inbox()
    app.nextTab.refresh_next()
    app.contextTab.refresh_contexts()
    app.completeTab.refresh_complete()

if __name__ == "__main__": 
    main()
    
    

