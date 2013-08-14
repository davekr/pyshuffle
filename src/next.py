from PyQt4 import QtCore, QtGui

import buffer
from delegate import *
from forms import ActionForm

class Next(object):
    def setup_next(self, app, mainWidget):
        
        stack=QtGui.QStackedWidget(mainWidget.tab)
        
        nextWidget=QtGui.QWidget(stack)
        nextLayout=QtGui.QVBoxLayout(nextWidget)

        self.nextList = QtGui.QListWidget(nextWidget)
        deleg = ListItemDelegate(nextWidget)
        self.nextList.setItemDelegate(deleg)
        nextLayout.addWidget(self.nextList)
        
        editButton = QtGui.QPushButton("Edit", nextWidget)
        completeButton = QtGui.QPushButton("Complete", nextWidget)
        deleteButton = QtGui.QPushButton("Delete", nextWidget)
        
        buttonWidget=QtGui.QWidget(nextWidget)
        buttonLayout=QtGui.QHBoxLayout(buttonWidget)
        buttonLayout.addWidget(editButton, 0)
        buttonLayout.addWidget(completeButton, 0)
        buttonLayout.addWidget(QtGui.QWidget(), 1)
        buttonLayout.addWidget(deleteButton, 0, QtCore.Qt.AlignRight)
        
        nextLayout.addWidget(buttonWidget)
        
        stack.addWidget(nextWidget)
        self.edit = ActionForm(stack, app, mainWidget, True)
        stack.addWidget(self.edit)
        
        def editAction():
            if len(self.nextList.selectedItems()) > 0:
                stack.setCurrentIndex(1)
                self.edit.edit(self.nextList.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject())
            else:
                mainWidget.statusBar.showMessage("Select item first",2000)
                
        def deleteAction():
            if len(self.nextList.selectedItems()) > 0:
                buffer.deleteAction(app, (self.nextList.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject()))
                self.mainWidget.statusBar.showMessage("Action deleted",2000)
            else:
                self.mainWidget.statusBar.showMessage("Select item first",2000)
        
        def completeAction():
            if len(self.nextList.selectedItems()) > 0:
                buffer.completeAction(app, (self.nextList.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject()))
                mainWidget.statusBar.showMessage("Action completed",2000)
            else:
                mainWidget.statusBar.showMessage("Select item first",2000)
        
        app.connect(editButton, QtCore.SIGNAL("clicked()"),editAction)
        app.connect(deleteButton, QtCore.SIGNAL("clicked()"),deleteAction)
        app.connect(completeButton, QtCore.SIGNAL("clicked()"),completeAction)
        app.connect(self.nextList, QtCore.SIGNAL("itemDoubleClicked (QListWidgetItem *)"), editAction)

        return stack

    def refresh_next(self):
        self.nextList.clear()
        for project in buffer.projectsBuffer.values():
            if len(project.actions) > 0:
                earliest = QtCore.QDate().fromString('2999.12.31','yyyy.MM.dd')
                eAction = None
                for action in project.actions.values():
                    if not action.completed and action.sched.isValid() and earliest > action.sched:
                            earliest = action.sched
                            eAction = action
                if eAction:            
                    listItem = QtGui.QListWidgetItem(eAction.desc)
                    listItem.setData(QtCore.Qt.UserRole, QtCore.QVariant(eAction))
                    self.nextList.addItem(listItem)
        self.edit.refreshAction()
