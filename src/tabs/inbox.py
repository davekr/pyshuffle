from PyQt4 import QtCore, QtGui

import buffer
from utils import ListItemDelegate
from forms import ActionForm

class Inbox(object):
    def setup_inbox(self, app, mainWidget):
        self.mainWidget = mainWidget
        
        stack=QtGui.QStackedWidget(mainWidget.tab)
        
        inboxWidget=QtGui.QWidget(stack)
        inboxLayout=QtGui.QVBoxLayout(inboxWidget)

        self.inboxList = QtGui.QListWidget(inboxWidget)
        deleg = ListItemDelegate(inboxWidget)
        self.inboxList.setItemDelegate(deleg)
        editButton = QtGui.QPushButton("Edit", inboxWidget)
        completeButton = QtGui.QPushButton("Complete", inboxWidget)
        deleteButton = QtGui.QPushButton("Delete", inboxWidget)
        
        buttonWidget=QtGui.QWidget(inboxWidget)
        buttonLayout=QtGui.QHBoxLayout(buttonWidget)
        buttonLayout.addWidget(editButton, 0)
        buttonLayout.addWidget(completeButton, 0)
        buttonLayout.addWidget(QtGui.QWidget(), 1)
        buttonLayout.addWidget(deleteButton, 0, QtCore.Qt.AlignRight)

        inboxLayout.addWidget(self.inboxList)
        inboxLayout.addWidget(buttonWidget)

        stack.addWidget(inboxWidget)
        self.edit = ActionForm(stack, app, mainWidget, True)
        stack.addWidget(self.edit)
        

        def editAction():
            if len(self.inboxList.selectedItems()) > 0:
                stack.setCurrentIndex(1)
                self.edit.edit(self.inboxList.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject())
            else:
                self.mainWidget.statusBar.showMessage("Select item first",2000)
                
        def deleteAction():
            if len(self.inboxList.selectedItems()) > 0:
                buffer.deleteAction(app, (self.inboxList.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject()))
                self.mainWidget.statusBar.showMessage("Action deleted",2000)
            else:
                self.mainWidget.statusBar.showMessage("Select item first",2000)
                
        def completeAction():
            if len(self.inboxList.selectedItems()) > 0:
                buffer.completeAction(app, (self.inboxList.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject()))
                self.mainWidget.statusBar.showMessage("Action completed",2000)
            else:
                self.mainWidget.statusBar.showMessage("Select item first",2000)

        app.connect(editButton, QtCore.SIGNAL("clicked()"),editAction)
        app.connect(deleteButton, QtCore.SIGNAL("clicked()"),deleteAction)
        app.connect(completeButton, QtCore.SIGNAL("clicked()"),completeAction)
        app.connect(self.inboxList, QtCore.SIGNAL("itemDoubleClicked (QListWidgetItem *)"), editAction)

        return stack

    def refresh_inbox(self):
        self.inboxList.clear()
        for item in buffer.actionsBuffer.values():
            if not item.completed:
                listItem = QtGui.QListWidgetItem(item.desc)
                listItem.setData(QtCore.Qt.UserRole, QtCore.QVariant(item))
                self.inboxList.addItem(listItem)
        self.edit.refreshAction()
            
