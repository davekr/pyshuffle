from PyQt4 import QtCore, QtGui

from app.utils import ListItemDelegate, event_register
from app.forms import ActionForm
from app.dbmanager import DBManager
from app.tabs.tab import Tab

class Inbox(QtGui.QStackedWidget, Tab):

    ICON = "inbox"
    LABEL = "Inbox"

    def _setup_content(self):
        inbox = self._setup_inbox()
        self.addWidget(inbox)
        action_form = ActionForm(True)
        self.addWidget(action_form)
        self._action_form = action_form

    def _connect_events(self):
        self.connect(self._inbox, QtCore.SIGNAL("itemDoubleClicked (QListWidgetItem *)"), self.edit_action)

    def _setup_inbox(self):
        inbox_list = self._setup_list()
        bottom = self._setup_bottom()
        layout = QtGui.QVBoxLayout()
        layout.addWidget(inbox_list)
        layout.addWidget(bottom)
        inbox = QtGui.QWidget()
        inbox.setLayout(layout)
        return inbox

    def _setup_list(self):
        inbox = QtGui.QListWidget()
        inbox.setItemDelegate(ListItemDelegate(inbox))
        self._inbox = inbox
        self._fill_inbox()
        event_register.action_change.connect(self._fill_inbox)
        return inbox

    def _setup_bottom(self):
        edit, complete, delete = self._setup_buttons()
        layout = QtGui.QHBoxLayout()
        layout.addWidget(edit, 0)
        layout.addWidget(complete, 0)
        layout.addWidget(QtGui.QWidget(), 1)
        layout.addWidget(delete, 0, QtCore.Qt.AlignRight)
        widget = QtGui.QWidget()
        widget.setLayout(layout)
        return widget

    def _setup_buttons(self):
        edit = QtGui.QPushButton("Edit")
        self.connect(edit, QtCore.SIGNAL("clicked()"), self.edit_action)
        complete = QtGui.QPushButton("Complete")
        self.connect(complete, QtCore.SIGNAL("clicked()"), self.complete_action)
        delete = QtGui.QPushButton("Delete")
        self.connect(delete, QtCore.SIGNAL("clicked()"), self.delete_action)
        return edit, complete, delete

    def edit_action(self):
        if self._item_selected():
            self.setCurrentIndex(1)
            action = self._inbox.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject()
            self._action_form.set_action(action)
            
    def delete_action(self):
        if self._item_selected():
            action = self._inbox.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject()
            action.delete()
            self.window().show_status("Action deleted")
            event_register.action_change.emit()
            
    def complete_action(self):
        if self._item_selected():
            action = self._inbox.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject()
            action.completed = True
            action.save()
            self.window().show_status("Action completed")
            event_register.action_change.emit()

    def _item_selected(self):
        if len(self._inbox.selectedItems()) > 0:
            return True
        else:
            self.window().show_status("Select item first")

    def _fill_inbox(self):
        self._inbox.clear()
        for action in DBManager.get_actions().values():
            if not action.completed:
                item = QtGui.QListWidgetItem(action.desc)
                item.setData(QtCore.Qt.UserRole, QtCore.QVariant(action))
                self._inbox.addItem(item)
