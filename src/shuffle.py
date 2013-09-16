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
#                                                      #
#======================================================#

from PyQt4 import QtGui
import sys
import os

from tabs import New, Projects, Calendar, Inbox, Next, Contexts, Complete, Synchronization
import buffer
from main import Shuffle

def main():
    app = QtGui.QApplication(sys.argv)

    PROJECT_PATH = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
    app.db = os.path.join(os.path.dirname(PROJECT_PATH), 'db')
    buffer.init_db(app)
    buffer.init_buffer(app)
    
    app.newTab = New()
    app.projectTab = Projects()
    app.calendarTab = Calendar()
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
    
    

