from PyQt4 import QtCore, QtGui

from app.utils import ListItemDelegate, event_register
from app.dbmanager import DBManager
from app.tabs.tab import Tab

class Complete(Tab):

    ICON = "completed"
    LABEL = "Completed"

    def _setup_content(self):
        completed = self._setup_list()
        bottom = self._setup_bottom()
        layout = QtGui.QVBoxLayout()
        layout.addWidget(completed)
        layout.addWidget(bottom)
        self.setLayout(layout)

    def _setup_list(self):
        completed = QtGui.QListWidget()
        completed.setItemDelegate(ListItemDelegate(completed))
        self._completed = completed
        self._fill_list()
        event_register.action_change.connect(self._fill_list)
        return completed

    def _setup_bottom(self):
        complete, delete = self._setup_buttons()
        layout = QtGui.QHBoxLayout()
        layout.addWidget(complete, 0)
        layout.addWidget(QtGui.QWidget(), 1)
        layout.addWidget(delete, 0, QtCore.Qt.AlignRight)
        widget = QtGui.QWidget()
        widget.setLayout(layout)
        return widget

    def _setup_buttons(self):
        complete = QtGui.QPushButton("Not Complete")
        self.connect(complete, QtCore.SIGNAL("clicked()"), self.restore_action)
        delete = QtGui.QPushButton("Delete")
        self.connect(delete, QtCore.SIGNAL("clicked()"), self.delete_action)
        return complete, delete
        
    def delete_action(self):
        if self._item_selected():
            action = self._completed.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject()
            action.delete()
            self.window().show_status("Action deleted")
            self._fill_list()
    
    def restore_action(self):
        if self._item_selected():
            action = self._completed.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject()
            action.completed = False
            action.save()
            self.window().show_status("Action restored")
            event_register.action_change.emit()
    
    def _item_selected(self):
        if len(self._completed.selectedItems()) > 0:
            return True
        else:
            self.window().show_status("Select item first")

    def _fill_list(self):
        self._completed.clear()
        for action in DBManager.get_actions().values():
            if action.completed:
                item = QtGui.QListWidgetItem(action.desc)
                item.setData(QtCore.Qt.UserRole, QtCore.QVariant(action))
                self._completed.addItem(item)
