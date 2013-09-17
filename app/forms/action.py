# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import datetime

from app.models import Action
from app.utils import MyLineEdit

class ActionForm(QtGui.QWidget):
    
    def __init__(self, parent, app, mainWidget, edit=False):
        QtGui.QWidget.__init__(self)
        self.app = app
        self.mainWidget = mainWidget
        self.editable=edit
        
        actionLayout=QtGui.QHBoxLayout(self)
        contentWidget=QtGui.QWidget(self)
        
        self.contentLayout=QtGui.QGridLayout(contentWidget)
        
        self.contentLayout.addWidget(QtGui.QLabel("Description"), 0, 0)
        self.descLineEdit=MyLineEdit("My action")
        self.contentLayout.addWidget(self.descLineEdit, 0, 1)
        
        self.contentLayout.addWidget(QtGui.QLabel("Project"), 1, 0)
        
        self.projectComboBox=QtGui.QComboBox(contentWidget)
        self.contentLayout.addWidget(self.projectComboBox, 1, 1)
        
        self.contentLayout.addWidget(QtGui.QLabel("Context"), 2, 0)
        
        self.contextComboBox=QtGui.QComboBox(contentWidget)
        self.contentLayout.addWidget(self.contextComboBox, 2, 1)
        
        self.contentLayout.addWidget(QtGui.QLabel("Details"), 3, 0)
        
        self.details = MyLineEdit("Description of my action")
        self.contentLayout.addWidget(self.details, 3, 1)
        
        self.contentLayout.addWidget(QtGui.QLabel("Scheduling"), 4, 0)
        
        self.sched=QtGui.QCheckBox()
        self.sched.setFocusPolicy(QtCore.Qt.NoFocus)
        self.contentLayout.addWidget(self.sched, 4, 1)
        
        self.dateInput=QtGui.QDateEdit(datetime.date.today())
        self.dateInput.setHidden(True)
        self.contentLayout.addWidget(self.dateInput, 5, 1)
        
        self.saveButton=QtGui.QPushButton("Save")
        
        if edit:
            cancelButton=QtGui.QPushButton("Back")
            self.contentLayout.addWidget(cancelButton, 6, 0, QtCore.Qt.AlignBottom)
            self.connect(cancelButton, QtCore.SIGNAL("clicked()"), self.cancel)
            self.saveButton.setMaximumSize(QtCore.QSize(80, 30))
            self.contentLayout.addWidget(self.saveButton, 6, 1, QtCore.Qt.AlignBottom)
        else:
            self.contentLayout.addWidget(self.saveButton, 6, 0, QtCore.Qt.AlignBottom)

        
        actionLayout.addWidget(contentWidget, 1)
        actionLayout.addWidget(QtGui.QWidget(self), 1)
        
        self.connect(self.sched, QtCore.SIGNAL("stateChanged(int)"),self.showSched)
        self.connect(self.saveButton, QtCore.SIGNAL("clicked()"),self.saveAction)
        
    def edit(self, action):
        self.actionId = action.id
        self.projectId = None
        self.contextId = None
        
        self.descLineEdit.setText(action.desc)
        
        if action.project:
            self.projectId = action.project.id
            for i in range(self.projectComboBox.count()):
                data = self.projectComboBox.itemData(i).toPyObject()
                if data!=None and data.id == action.project.id:
                    self.projectComboBox.setCurrentIndex(i)
                    break
                
        if action.context:
            self.contextId = action.context.id
            for i in range(self.contextComboBox.count()):
                data = self.contextComboBox.itemData(i).toPyObject()
                if data!=None and data.id == action.context.id:
                    self.contextComboBox.setCurrentIndex(i)
                    break
            
        self.details.setText(action.details)
        if action.sched.isValid():
            self.sched.toggle()
            self.dateInput.setDate(action.sched)
        
    def cancel(self):
        self.parent().setCurrentIndex(self.parent().currentIndex() - 1)
        self.setDefault()
            
    def showSched(self, state):
        if(state):
            self.dateInput.setHidden(False)
        else:
            self.dateInput.setHidden(True)

    def saveAction(self):
        data=self.projectComboBox.itemData(self.projectComboBox.currentIndex())
        project = data.toPyObject()
        data=self.contextComboBox.itemData(self.contextComboBox.currentIndex())
        context = data.toPyObject()
        
        if project == NotImplemented:
            project = None
        if context == NotImplemented:
            context = None

        dat = QtCore.QDate()
        if self.sched.isChecked():
            dat = self.dateInput.date() 
            
        detail = unicode(self.details.text())
        
        action = Action(None, unicode(self.descLineEdit.text()), project, context, dat, detail, 
                        0, self.app.cursor)
        
        if self.editable:
            action.id = self.actionId
            
            self.app.buffer.updateAction(self.app, action, self.projectId, self.contextId)
            
            self.mainWidget.statusBar.showMessage("Action updated",2000)
            
            self.cancel() #not cancel but I use function in method
        else:
            self.app.buffer.createAction(self.app, action)
            
            self.mainWidget.statusBar.showMessage("Action created",2000)
            
            self.setDefault()
        
    def setDefault(self):
        self.descLineEdit.setText("My action")
        self.projectComboBox.setCurrentIndex(0)
        self.contextComboBox.setCurrentIndex(0)
        self.details.setText("Description of my action")
        self.dateInput.setDate(datetime.date.today())
        self.sched.setCheckState(QtCore.Qt.Unchecked)
        
        
    def refreshAction(self):
        self.projectComboBox.clear()
        self.projectComboBox.addItem("None")
        self.contextComboBox.clear()
        self.contextComboBox.addItem("None")
        for project in self.app.buffer._projects.values():
            self.projectComboBox.addItem(project.name, QtCore.QVariant(project))
        for context in self.app.buffer._contexts.values():
            self.contextComboBox.addItem(context.name, QtCore.QVariant(context))
