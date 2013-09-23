from PyQt4 import QtCore, QtGui

from app.forms import ActionForm, ContextForm
from app.models import Action
from app.dbmanager import DBManager

class Contexts(object):
    def setup_contexts(self, app, mainWidget):
        self.app = app
        
        stack=QtGui.QStackedWidget(mainWidget.tab)
        
        contextsWidget=QtGui.QWidget(stack)
        contextsLayout=QtGui.QVBoxLayout(contextsWidget)

        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setHeaderLabels(["Name", "Project", "Date", "Details"])
        self.treeWidget.header().resizeSection(0, 130)
        self.treeWidget.header().resizeSection(2, 80)
        
        editButton = QtGui.QPushButton("Edit", contextsWidget)
        completeButton = QtGui.QPushButton("Complete", contextsWidget)
        deleteButton = QtGui.QPushButton("Delete", contextsWidget)
        
        buttonWidget=QtGui.QWidget(contextsWidget)
        buttonLayout=QtGui.QHBoxLayout(buttonWidget)
        buttonLayout.addWidget(editButton, 0)
        buttonLayout.addWidget(completeButton, 0)
        buttonLayout.addWidget(QtGui.QWidget(), 1)
        buttonLayout.addWidget(deleteButton, 0, QtCore.Qt.AlignRight)

        contextsLayout.addWidget(self.treeWidget)
        contextsLayout.addWidget(buttonWidget)
        
        stack.addWidget(contextsWidget)
        self.edit = ActionForm(True)
        stack.addWidget(self.edit)
        self.editContext = ContextForm(stack, app, mainWidget, True)
        stack.addWidget(self.editContext)
        stack.addWidget(self.editContext.chooseColor)
        stack.addWidget(self.editContext.chooseIcon)
        
        def editAction():
            if len(self.treeWidget.selectedItems()) > 0:
                item = self.treeWidget.selectedItems()[0].data(0,QtCore.Qt.UserRole).toPyObject()
                if isinstance(item, Action):
                    stack.setCurrentIndex(1)
                    self.edit.edit(item)
                else:
                    stack.setCurrentIndex(2)
                    self.editContext.edit(item)
            else:
                mainWidget.statusBar.showMessage("Select item first",2000)
                
        def deleteAction():
            if len(self.treeWidget.selectedItems()) > 0:
                item = self.treeWidget.selectedItems()[0].data(0,QtCore.Qt.UserRole).toPyObject()
                if isinstance(item, Action):
                    DBManager.deleteAction(app, item)
                    mainWidget.statusBar.showMessage("Action deleted",2000)
                else:
                    reply = QtGui.QMessageBox.question(contextsWidget, 'Are you sure?',"Context will be" 
                                                       +" deleted and context of all context's actions will" 
                                                       + "be set to none.", 
                                               QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
                    if reply == QtGui.QMessageBox.Yes:
                        DBManager.deleteContext(app, item)
                        mainWidget.statusBar.showMessage("Context deleted",2000)
            else:
                mainWidget.statusBar.showMessage("Select item first",2000)
                
        def completeAction():
            if len(self.treeWidget.selectedItems()) > 0:
                item = self.treeWidget.selectedItems()[0].data(0,QtCore.Qt.UserRole).toPyObject()
                if isinstance(item, Action):
                    DBManager.completeAction(app, item)
                    mainWidget.statusBar.showMessage("Action completed",2000)
                else:
                    mainWidget.statusBar.showMessage("Context cannot be completed",2000)
            else:
                mainWidget.statusBar.showMessage("Select item first",2000)
        
        app.connect(editButton, QtCore.SIGNAL("clicked()"),editAction)
        app.connect(deleteButton, QtCore.SIGNAL("clicked()"),deleteAction)
        app.connect(completeButton, QtCore.SIGNAL("clicked()"),completeAction)
        app.connect(self.treeWidget, QtCore.SIGNAL("itemDoubleClicked (QTreeWidgetItem *,int)"), editAction)
        
        return stack    
    
    def refresh_contexts(self):
        items = []
        for i in DBManager.get_contexts().values():
            context = QtGui.QTreeWidgetItem(QtCore.QStringList(i.name))
            context.setBackgroundColor(0, QtGui.QColor(i.color[22:29]))
            context.setTextColor(0, QtGui.QColor(i.color[38:45]))
            context.setIcon(0,QtGui.QIcon(i.icon or ""))
            context.setData(0,QtCore.Qt.UserRole, QtCore.QVariant(i))
            for j in i.actions.values():
                if not j.completed:
                    project = ""
                    if j.project:
                        project = j.project.name
                    child = QtGui.QTreeWidgetItem(QtCore.QStringList([j.desc, project,
                                                                  j.sched.toString('yyyy-MM-dd'),
                                                                  j.details]))
                    child.setData(0,QtCore.Qt.UserRole, QtCore.QVariant(j))
                    context.addChild(child)
            items.append(context)
        self.treeWidget.clear()    
        self.treeWidget.addTopLevelItems(items)
        
        self.edit.refreshAction()
