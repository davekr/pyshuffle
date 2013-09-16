# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from models import Project
import buffer
from utils import MyLineEdit

class ProjectForm(QtGui.QWidget):
    
    def __init__(self, parent, app, mainWidget, edit=False):
        QtGui.QWidget.__init__(self)
        self.app = app
        self.mainWidget = mainWidget
        self.editable = edit
        
        projectLayout=QtGui.QHBoxLayout(self)
        projectWidget=QtGui.QWidget(self)
        
        self.contentLayout=QtGui.QGridLayout(projectWidget)
        
        self.contentLayout.addWidget(QtGui.QLabel("Name"), 0, 0)
        
        self.projectNameEdit=MyLineEdit("My project")
        self.contentLayout.addWidget(self.projectNameEdit, 0, 1)
        
        self.contentLayout.addWidget(QtGui.QLabel("Default context"), 1, 0)
        
        self.contextComboBox=QtGui.QComboBox()
        self.contentLayout.addWidget(self.contextComboBox, 1, 1)
                
        projectSaveButton=QtGui.QPushButton("Save")
        
        if edit:
            cancelButton=QtGui.QPushButton("Back")
            self.contentLayout.addWidget(cancelButton, 2, 0, QtCore.Qt.AlignBottom)
            self.connect(cancelButton, QtCore.SIGNAL("clicked()"), self.cancel)
            projectSaveButton.setMaximumSize(QtCore.QSize(80, 30))
            self.contentLayout.addWidget(projectSaveButton, 2, 1, QtCore.Qt.AlignBottom)
        else:
            self.contentLayout.addWidget(projectSaveButton, 2, 0, QtCore.Qt.AlignBottom)
        
        
        projectLayout.addWidget(projectWidget, 1)
        projectLayout.addWidget(QtGui.QWidget(self), 1)
        
        self.connect(projectSaveButton, QtCore.SIGNAL("clicked()"),self.saveProject)
        
    def edit(self, project):
        self.project = project
        self.projectNameEdit.setText(project.name)
        if project.context:
            for i in range(self.contextComboBox.count()):
                data = self.contextComboBox.itemData(i).toPyObject()
                if data!=None and data.id == project.context.id:
                    self.contextComboBox.setCurrentIndex(i)
                    break
        
    def cancel(self):
        self.parent().setCurrentIndex(self.parent().currentIndex() - 2)
        self.setDefault()
    
    def saveProject(self):
        name = unicode(self.projectNameEdit.text())
        data=self.contextComboBox.itemData(self.contextComboBox.currentIndex())
        context = data.toPyObject()
        if context == NotImplemented:
            context = None

        if self.editable:
            self.project.name = name
            self.project.context = context
            
            buffer.createProject(self.app, self.project, True)
            
            self.mainWidget.statusBar.showMessage("Project updated",2000)
            
            self.cancel() #not cancel but I use function in method
        else:
            project = Project(None, name, context, self.app.cursor)
            
            buffer.createProject(self.app, project)
            
            self.mainWidget.statusBar.showMessage("Project created",2000)
        
            self.setDefault()
        
    def setDefault(self):
        self.projectNameEdit.setText("My project")
        self.contextComboBox.setCurrentIndex(0)
        
    def refreshProject(self):
        self.contextComboBox.clear()
        self.contextComboBox.addItem("None")
        for context in buffer.contextsBuffer.values():
            self.contextComboBox.addItem(context.name, QtCore.QVariant(context))
