#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
import sys

from app.tabs import New, Projects, Calendar, Inbox, Next, Contexts, Complete, Synchronization
import app.buffer as buffer
from app.main import Shuffle

def main():
    app = QtGui.QApplication(sys.argv)

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
    
    

