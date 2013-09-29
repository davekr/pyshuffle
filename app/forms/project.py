# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from app.models import Project
from app.utils import SelectAllLineEdit
from app.dbmanager import DBManager
from app.utils import event_register

class ProjectForm(QtGui.QWidget):
    
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
        layout.addWidget(QtGui.QLabel("Name"), 0, 0)
        self._setup_name(layout)
        self._setup_context_cbx(layout)
        self._setup_buttons(layout)
        widget = QtGui.QWidget()
        widget.setLayout(layout)
        return widget

    def _setup_name(self, layout):
        name = SelectAllLineEdit("My project")
        layout.addWidget(name, 0, 1)
        
    def _setup_context_cbx(self, layout):
        layout.addWidget(QtGui.QLabel("Default context"), 1, 0)
        context_cbx = QtGui.QComboBox()
        layout.addWidget(context_cbx, 1, 1)
        self._context_cbx = context_cbx
        self._fill_cbx()
        event_register.context_change.connect(self._fill_cbx)

    def _fill_cbx(self):
        self._context_cbx.clear()
        self._context_cbx.addItem("None")
        for context in DBManager.get_contexts().values():
            self._context_cbx.addItem(context.name, QtCore.QVariant(context))
                
    def _setup_buttons(self, layout):
        save = QtGui.QPushButton("Save")
        self.connect(save, QtCore.SIGNAL("clicked()"),self.save_project)
        if self.editable:
            cancel = QtGui.QPushButton("Back")
            layout.addWidget(cancel, 2, 0, QtCore.Qt.AlignBottom)
            self.connect(cancel, QtCore.SIGNAL("clicked()"), self.hide_form)
            save.setMaximumSize(QtCore.QSize(80, 30))
            layout.addWidget(save, 2, 1, QtCore.Qt.AlignBottom)
        else:
            layout.addWidget(save, 2, 0, QtCore.Qt.AlignBottom)
        
    def edit(self, project):
        self.project = project
        self.projectNameEdit.setText(project.name)
        if project.context:
            for i in range(self.contextComboBox.count()):
                data = self.contextComboBox.itemData(i).toPyObject()
                if data!=None and data.id == project.context.id:
                    self.contextComboBox.setCurrentIndex(i)
                    break
        
    def hide_form(self):
        self.parent().setCurrentIndex(self.parent().currentIndex() - 2)
        self.setDefault()
    
    def save_project(self):
        name = unicode(self.projectNameEdit.text())
        data=self.contextComboBox.itemData(self.contextComboBox.currentIndex())
        context = data.toPyObject()
        if context == NotImplemented:
            context = None
        if self.editable:
            self.project.name = name
            self.project.context = context
            self.window().show_status("Project updated")
            self.hide_form() 
        else:
            self.project = Project(None, name, context)
            self.window().show_status("Project created")
            self.setDefault()
        DBManager.create_project(self.project)
        event_register.project_change.emit()
        
    def setDefault(self):
        self.projectNameEdit.setText("My project")
        self.contextComboBox.setCurrentIndex(0)
        
