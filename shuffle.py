#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
import sys

from app.dbmanager import DBManager
from app.main import Main

def main():
    app = QtGui.QApplication(sys.argv)
    dialog = lambda: QtGui.QMessageBox.question(QtGui.QWidget(), 'First time', \
            "It appears you've started the app for the first time. Do you want to load demo data?", QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
    DBManager.init_dbmanager(dialog)
    main = Main()
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__": 
    main()
    
    

