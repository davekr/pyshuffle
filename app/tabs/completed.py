from PyQt4 import QtCore, QtGui

from app.utils import ListItemDelegate
from app.dbmanager import DBManager

class Complete(object):
    def setup_complete(self, app, mainWidget):
        self.app = app
        self.mainWidget = mainWidget
        
        completeWidget=QtGui.QWidget(mainWidget)
        completeLayout=QtGui.QVBoxLayout(completeWidget)

        self.completeList = QtGui.QListWidget(completeWidget)
        deleg = ListItemDelegate(completeWidget)
        self.completeList.setItemDelegate(deleg)
        completeButton = QtGui.QPushButton("Not Complete", completeWidget)
        deleteButton = QtGui.QPushButton("Delete", completeWidget)
        
        buttonWidget=QtGui.QWidget(completeWidget)
        buttonLayout=QtGui.QHBoxLayout(buttonWidget)
        buttonLayout.addWidget(completeButton, 0)
        buttonLayout.addWidget(QtGui.QWidget(), 1)
        buttonLayout.addWidget(deleteButton, 0, QtCore.Qt.AlignRight)

        completeLayout.addWidget(self.completeList)
        completeLayout.addWidget(buttonWidget)
        
        def deleteAction():
            if len(self.completeList.selectedItems()) > 0:
                DBManager.deleteAction(app, (self.completeList.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject()))
                mainWidget.statusBar.showMessage("Action deleted",2000)
            else:
                mainWidget.statusBar.showMessage("Select item first",2000)
        
        def restoreAction():
            if len(self.completeList.selectedItems()) > 0:
                DBManager.completeAction(app, 
                    (self.completeList.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject()),
                     True)
                mainWidget.statusBar.showMessage("Action restored",2000)
            else:
                mainWidget.statusBar.showMessage("Select item first",2000)
        
        app.connect(deleteButton, QtCore.SIGNAL("clicked()"),deleteAction)
        app.connect(completeButton, QtCore.SIGNAL("clicked()"),restoreAction)

        return completeWidget
    
    def refresh_complete(self):
        self.completeList.clear()
        for item in DBManager.get_actions().values():
            if item.completed:
                listItem = QtGui.QListWidgetItem(item.desc)
                listItem.setData(QtCore.Qt.UserRole, QtCore.QVariant(item))
                self.completeList.addItem(listItem)
