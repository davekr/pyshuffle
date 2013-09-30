# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from app.models import Project
from app.utils import SelectAllLineEdit
from app.dbmanager import DBManager
from app.utils import event_register

class ProjectForm(QtGui.QWidget):
    
    def __init__(self, editmode = False):
        QtGui.QWidget.__init__(self)
        self.editmode = editmode
        self._project = Project()
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
        self._name = name
        
    def _setup_context_cbx(self, layout):
        layout.addWidget(QtGui.QLabel("Default context"), 1, 0)
        context_cbx = QtGui.QComboBox()
        layout.addWidget(context_cbx, 1, 1)
        self._context_cbx = context_cbx
        self._fill_cbx()
        event_register.context_change.connect(self._fill_cbx)

    def _fill_cbx(self):
        self._context_cbx.clear()
        self._context_cbx.addItem("None", QtCore.QVariant())
        for context in DBManager.get_contexts().values():
            self._context_cbx.addItem(context.name, QtCore.QVariant(context))
                
    def _setup_buttons(self, layout):
        save = QtGui.QPushButton("Save")
        self.connect(save, QtCore.SIGNAL("clicked()"),self.save_project)
        if self.editmode:
            cancel = QtGui.QPushButton("Back")
            layout.addWidget(cancel, 2, 0, QtCore.Qt.AlignBottom)
            self.connect(cancel, QtCore.SIGNAL("clicked()"), self.hide_form)
            save.setMaximumSize(QtCore.QSize(80, 30))
            layout.addWidget(save, 2, 1, QtCore.Qt.AlignBottom)
        else:
            layout.addWidget(save, 2, 0, QtCore.Qt.AlignBottom)
        
    def set_project(self, project):
        self._project = project
        self._name.setText(project.name)
        self._select_item(project.context, self._context_cbx)

    def _select_item(self, item, cbx):
        if item:
            for i in range(cbx.count()):
                data = cbx.itemData(i).toPyObject()
                if data!=None and data.id == item.id:
                    cbx.setCurrentIndex(i)
                    break
        
    def hide_form(self):
        self.parent().setCurrentIndex(self.parent().currentIndex() - 2)
        self.set_default()
    
    def save_project(self):
        project = self.get_project()
        if self.editmode:
            self.window().show_status("Project updated")
            self.hide_form() 
        else:
            self.window().show_status("Project created")
            self.set_default()
        project.save()
        self._project = Project()
        event_register.project_change.emit()

    def get_project(self):
        project = self._project
        project.name = unicode(self._project.text())
        project.context = self._selected_item(self._context_cbx)
        return project

    def _selected_item(self, cbx):
        data = cbx.itemData(cbx.currentIndex())
        obj = data.toPyObject()
        return obj
        
    def set_default(self):
        self._name.setText("My project")
        self._context_cbx.setCurrentIndex(0)
        
