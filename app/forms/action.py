# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import datetime

from app.dbmanager import DBManager
from app.models import Action
from app.utils import SelectAllLineEdit, SelectAllTextEdit, event_register

class ActionForm(QtGui.QWidget):
    
    def __init__(self, editmode = False):
        QtGui.QWidget.__init__(self)
        self._action = Action()
        self.editmode = editmode
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
        self._fill_cbxs()
        event_register.project_change.connect(self._fill_projects)
        event_register.context_change.connect(self._fill_contexts)
        self._setup_details(layout)
        self._setup_schedule(layout)
        self._setup_date(layout)
        self._setup_buttons(layout)
        widget = QtGui.QWidget()
        widget.setLayout(layout)
        return widget

    def _setup_description(self, layout):
        description = SelectAllLineEdit("My action")
        layout.addWidget(QtGui.QLabel("Description"), 0, 0)
        layout.addWidget(description, 0, 1)
        self._description = description
        
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
        details = SelectAllTextEdit("Description of my action")
        layout.addWidget(QtGui.QLabel("Details"), 3, 0, QtCore.Qt.AlignTop)
        layout.addWidget(details, 3, 1)
        self._details = details
        
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
        if self.editmode:
            cancel = QtGui.QPushButton("Back")
            layout.addWidget(cancel, 6, 0, QtCore.Qt.AlignBottom)
            self.connect(cancel, QtCore.SIGNAL("clicked()"), self.hide_form)
            save.setMaximumSize(QtCore.QSize(80, 30))
            layout.addWidget(save, 6, 1, QtCore.Qt.AlignBottom)
        else:
            layout.addWidget(save, 6, 0, QtCore.Qt.AlignBottom)
        
    def _fill_cbxs(self):
        self._fill_projects()
        self._fill_contexts()

    def _fill_projects(self):
        self._project_cbx.clear()
        self._project_cbx.addItem("None", QtCore.QVariant())
        for project in DBManager.get_projects().values():
            self._project_cbx.addItem(project.name, QtCore.QVariant(project))

    def _fill_contexts(self):
        self._context_cbx.clear()
        self._context_cbx.addItem("None", QtCore.QVariant())
        for context in DBManager.get_contexts().values():
            self._context_cbx.addItem(context.name, QtCore.QVariant(context))

        
    def hide_form(self):
        self.parent().setCurrentIndex(self.parent().currentIndex() - 1)
        self.set_default()
            
    def show_sched(self, state):
        if state:
            self._date.setHidden(False)
        else:
            self._date.setHidden(True)

    def save_action(self):
        action = self.get_action()
        if self.editmode:
            self.window().show_status("Action updated")
            self.hide_form() 
        else:
            self.window().show_status("Action created")
            self.set_default()
        action.save()
        self._action = Action()
        event_register.action_change.emit()

    def get_action(self):
        action = self._action
        action.desc = unicode(self._description.text())
        action.project = self._selected_item(self._project_cbx)
        action.context = self._selected_item(self._context_cbx)
        action.sched = self._get_date()
        action.details = unicode(self._details.toPlainText())
        return action

    def _selected_item(self, cbx):
        data = cbx.itemData(cbx.currentIndex())
        obj = data.toPyObject()
        return obj

    def _get_date(self):
        date = QtCore.QDate()
        if self._sched.isChecked():
            date = self._date.date() 
        return date
        
    def set_action(self, action):
        self._action = action
        self._description.setText(action.desc)
        self._select_item(action.project, self._project_cbx)
        self._select_item(action.context, self._context_cbx)
        self._details.setText(action.details)
        self._set_date(action.sched)

    def _select_item(self, item, cbx):
        if item:
            for i in range(cbx.count()):
                data = cbx.itemData(i).toPyObject()
                if data and data.id == item.id:
                    cbx.setCurrentIndex(i)
                    break

    def _set_date(self, date):
        if date.isValid():
            self._sched.setCheckState(QtCore.Qt.Checked)
            self._date.setDate(date)

    def set_default(self):
        self._description.setText("My action")
        self._project_cbx.setCurrentIndex(0)
        self._context_cbx.setCurrentIndex(0)
        self._details.setText("Description of my action")
        self._date.setDate(datetime.date.today())
        self._sched.setCheckState(QtCore.Qt.Unchecked)
        
        

