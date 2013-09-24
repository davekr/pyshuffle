from PyQt4 import QtCore, QtGui

from app.forms import ActionForm, ContextForm
from app.models import Action
from app.dbmanager import DBManager
from projects import Projects

class Contexts(Projects):

    ICON = "contexts"
    LABEL = "Contexts"

    def _setup_content(self):
        context_list = self._setup_projects()
        self.addWidget(context_list)
        self.addWidget(ActionForm(True))
        context_form = ContextForm(True) 
        self.addWidget(context_form)
        self.addWidget(context_form.chooseColor)
        self.addWidget(context_form.chooseIcon)

    def _setup_tree(self):
        tree = QtGui.QTreeWidget()
        tree.setColumnCount(2)
        tree.setHeaderLabels(["Name", "Project", "Date", "Details"])
        tree.header().resizeSection(0, 130)
        tree.header().resizeSection(2, 80)
        self._tree = tree
        return tree
        
    def edit_action(self):
        if len(self.treeWidget.selectedItems()) > 0:
            item = self.treeWidget.selectedItems()[0].data(0,QtCore.Qt.UserRole).toPyObject()
            if isinstance(item, Action):
                self.setCurrentIndex(1)
                self.edit.edit(item)
            else:
                self.setCurrentIndex(2)
                self.editContext.edit(item)
        else:
            self.window().show_status("Select item first")
            
    def delete_action(self):
        if len(self.treeWidget.selectedItems()) > 0:
            item = self.treeWidget.selectedItems()[0].data(0,QtCore.Qt.UserRole).toPyObject()
            if isinstance(item, Action):
                DBManager.deleteAction(item)
                self.window().show_status("Action deleted")
            else:
                reply = QtGui.QMessageBox.question(self, 'Are you sure?',"Context will be" 
                                                   +" deleted and context of all context's actions will" 
                                                   + "be set to none.", 
                                           QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
                if reply == QtGui.QMessageBox.Yes:
                    DBManager.deleteContext(item)
                    self.window().show_status("Context deleted")
        else:
            self.window().show_status("Select item first")
            
    def complete_action(self):
        if len(self.treeWidget.selectedItems()) > 0:
            item = self.treeWidget.selectedItems()[0].data(0,QtCore.Qt.UserRole).toPyObject()
            if isinstance(item, Action):
                DBManager.completeAction(item)
                self.window().show_status("Action completed")
            else:
                self.window().show_status("Context cannot be completed")
        else:
            self.window().show_status("Select item first")
    
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
