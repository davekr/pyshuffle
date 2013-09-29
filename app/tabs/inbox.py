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
        self.addWidget(ActionForm(True))

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
        if len(self.inboxList.selectedItems()) > 0:
            self.setCurrentIndex(1)
            self.edit.edit(self.inboxList.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject())
        else:
            self.window().show_status("Select item first")
            
    def delete_action(self):
        if len(self.inboxList.selectedItems()) > 0:
            DBManager.delete_actionn(self.inboxList.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject())
            self.window().show_status("Action deleted")
        else:
            self.window().show_status("Select item first")
            
    def complete_action(self):
        if len(self.inboxList.selectedItems()) > 0:
            DBManager.update_action(self.inboxList.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject())
            self.window().show_status("Action completed")
        else:
            self.window().show_status("Select item first")

    def _fill_inbox(self):
        self._inbox.clear()
        for action in DBManager.get_actions().values():
            if not action.completed:
                item = QtGui.QListWidgetItem(action.desc)
                item.setData(QtCore.Qt.UserRole, QtCore.QVariant(action))
                self._inbox.addItem(item)
