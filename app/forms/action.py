# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import datetime

from app.dbmanager import DBManager
from app.models import Action
from app.utils import SelectAllLineEdit, SelectAllTextEdit

class ActionForm(QtGui.QWidget):
    
    def __init__(self, edit=False):
        QtGui.QWidget.__init__(self)
        self.editable = edit
        content = self._setup_content()
        layout = QtGui.QHBoxLayout()
        layout.addWidget(content, 1)
        layout.addWidget(QtGui.QWidget(self), 1)
        self.setLayout(layout)
        
    def _setup_content(self):
        layout = QtGui.QGridLayout()
        self._setup_description(layout)
        self._setup_project_cbx(layout)
        self._setup_context_cbx(layout)
        self._setup_details(layout)
        self._setup_schedule(layout)
        self._setup_date(layout)
        self._setup_buttons(layout)
        widget = QtGui.QWidget()
        widget.setLayout(layout)
        return widget

    def _setup_description(self, layout):
        layout.addWidget(QtGui.QLabel("Description"), 0, 0)
        layout.addWidget(SelectAllLineEdit("My action"), 0, 1)
        
    def _setup_project_cbx(self, layout):
        layout.addWidget(QtGui.QLabel("Project"), 1, 0)
        project_cbx = QtGui.QComboBox()
        layout.addWidget(project_cbx, 1, 1)
        self._project_cbx = project_cbx
        
    def _setup_context_cbx(self, layout):
        layout.addWidget(QtGui.QLabel("Context"), 2, 0)
        context_cbx = QtGui.QComboBox()
        layout.addWidget(context_cbx, 2, 1)
        self._context_cbx = context_cbx

    def _setup_details(self, layout):
        layout.addWidget(QtGui.QLabel("Details"), 3, 0, QtCore.Qt.AlignTop)
        layout.addWidget(SelectAllTextEdit("Description of my action"), 3, 1)
        
    def _setup_schedule(self, layout):
        layout.addWidget(QtGui.QLabel("Scheduling"), 4, 0)
        sched = QtGui.QCheckBox()
        sched.setFocusPolicy(QtCore.Qt.NoFocus)
        layout.addWidget(sched, 4, 1)
        self._sched = sched
        self.connect(sched, QtCore.SIGNAL("stateChanged(int)"), self.show_sched)
        
    def _setup_date(self, layout):
        date = QtGui.QDateEdit(datetime.date.today())
        date.setHidden(True)
        layout.addWidget(date, 5, 1)
        layout.setRowMinimumHeight(5, 28)
        self._date = date
        
    def _setup_buttons(self, layout):
        save = QtGui.QPushButton("Save")
        self.connect(save, QtCore.SIGNAL("clicked()"), self.save_action)
        if self.editable:
            cancel = QtGui.QPushButton("Back")
            layout.addWidget(cancel, 6, 0, QtCore.Qt.AlignBottom)
            self.connect(cancel, QtCore.SIGNAL("clicked()"), self.hide_form)
            save.setMaximumSize(QtCore.QSize(80, 30))
            layout.addWidget(save, 6, 1, QtCore.Qt.AlignBottom)
        else:
            layout.addWidget(save, 6, 0, QtCore.Qt.AlignBottom)
        
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
        
    def hide_form(self):
        self.parent().setCurrentIndex(self.parent().currentIndex() - 1)
        self.setDefault()
            
    def show_sched(self, state):
        if(state):
            self.dateInput.setHidden(False)
        else:
            self.dateInput.setHidden(True)

    def save_action(self):
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
            
        detail = unicode(self.details.toPlainText())
        
        action = Action(None, unicode(self.descLineEdit.text()), project, context, dat, detail, 
                        0)
        
        if self.editable:
            action.id = self.actionId
            self.window().show_status("Action updated")
            self.hide_form() 
        else:
            self.window().show_status("Action created")
            self.setDefault()
        action.save()
        
    def set_default(self):
        self.descLineEdit.setText("My action")
        self.projectComboBox.setCurrentIndex(0)
        self.contextComboBox.setCurrentIndex(0)
        self.details.setText("Description of my action")
        self.dateInput.setDate(datetime.date.today())
        self.sched.setCheckState(QtCore.Qt.Unchecked)
        
        
    def refresh(self):
        self.projectComboBox.clear()
        self.projectComboBox.addItem("None")
        self.contextComboBox.clear()
        self.contextComboBox.addItem("None")
        for project in DBManager.get_projects().values():
            self.projectComboBox.addItem(project.name, QtCore.QVariant(project))
        for context in DBManager.get_contexts().values():
            self.contextComboBox.addItem(context.name, QtCore.QVariant(context))

