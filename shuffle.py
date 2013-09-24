#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
import sys

from app.dbmanager import DBManager
from app.main import Main

def main():
    app = QtGui.QApplication(sys.argv)

    DBManager.init_dbmanager()
    
    #app.newTab = New()
    #app.projectTab = Projects()
    #app.calendarTab = Calendar()
    #app.inboxTab = Inbox()
    #app.nextTab = Next()
    #app.contextTab = Contexts()
    #app.completeTab = Complete()
    #app.syncTab = Synchronization()
    
    main = Main()
    main.show()
    #app.refresh = refreshApp
    #app.refresh(app)
    #app.syncTab.refresh_sync()
    
    #reply = QtGui.QMessageBox.question(app.mainWindow, 'First time',"Do you want to load demo data?", QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
    #if reply == QtGui.QMessageBox.Yes:
        #print 'yes'
    sys.exit(app.exec_())
    
def refreshApp(app):
    pass

if __name__ == "__main__": 
    main()
    
    

