# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import git

from app.utils import SelectAllLineEdit

class RepositoryForm(QtGui.QWidget):
    
    def __init__(self, repo):
        QtGui.QWidget.__init__(self)
        self.repo = repo
        
        repLayout=QtGui.QHBoxLayout(self)
        repWidget=QtGui.QWidget(self)
        
        self.contentLayout=QtGui.QGridLayout(repWidget)
        
        self.contentLayout.addWidget(QtGui.QLabel("Name"), 0, 0)
        
        self.repLineEdit = SelectAllLineEdit("My_repository")
        self.contentLayout.addWidget(self.repLineEdit, 0, 1)
        
        self.contentLayout.addWidget(QtGui.QLabel("URI"), 1, 0)
        
        self.uriLineEdit = SelectAllLineEdit("/home/")
        self.contentLayout.addWidget(self.uriLineEdit, 1, 1)
        
        cancelButton=QtGui.QPushButton("Back")
        self.contentLayout.addWidget(cancelButton, 2, 0, QtCore.Qt.AlignBottom)
        
        saveButton=QtGui.QPushButton("Create")
        saveButton.setMaximumSize(QtCore.QSize(80, 30))
        self.contentLayout.addWidget(saveButton, 2, 1, QtCore.Qt.AlignBottom)
        
        repLayout.addWidget(repWidget, 1)
        repLayout.addWidget(QtGui.QWidget(self), 1)
        
        self.connect(cancelButton, QtCore.SIGNAL("clicked()"), self.cancel)
        self.connect(saveButton, QtCore.SIGNAL("clicked()"), self.create)
        
    def cancel(self):
        self.parent().setCurrentIndex(self.parent().currentIndex() - 1)
        self.setDefault()
        
    def create(self):
        name = str(self.repLineEdit.text())
        uri = str(self.uriLineEdit.text())
        if len(name) == 0:
            self.window().show_status("Repository should have a name")
        elif ' ' in name or ' ' in uri:
            self.window().show_status("Spaces in the name are not allowed")
        elif len(uri) == 0:
            self.window().show_status("Not a valid URI")
        else:
            try:
                self.repo.git.execute(["git", "remote", "add", name, uri])
            except git.errors.GitCommandError:
                self.window().show_status("Remote repository with that name exists")
                return
            try:
                self.window().show_status("Trying to fetch from remote repository. This may take a while" +
                                                      " depends on size of transfering data.")
                self.repo.git.execute(["git", "fetch", name])
                #self.app.syncTab.refresh_sync()
                self.window().show_status("Remote repository created")
                self.setDefault()
            except git.errors.GitCommandError:
                self.repo.git.execute(["git", "remote", "rm", name])
                QtGui.QMessageBox.warning(self, "An error occurred", "Upps\n" +
                                          "Is entered URI valid? Do you have permission to access" +
                                          " that URI?")
        
    def setDefault(self):
        self.repLineEdit.setText("My_repository")
        self.uriLineEdit.setText("/home/")
