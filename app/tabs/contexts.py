from PyQt4 import QtCore, QtGui

from app.forms import ActionForm, ContextForm
from app.models import Action
from app.dbmanager import DBManager
from projects import Projects
from settings import DATE_FORMAT

class Contexts(Projects):

    ICON = "contexts"
    LABEL = "Contexts"

    def _setup_content(self):
        context_list = self._setup_projects()
        self.addWidget(context_list)
        self.addWidget(ActionForm(True))
        self.addWidget(ContextForm(True))

    def _setup_tree(self):
        tree = QtGui.QTreeWidget()
        tree.setColumnCount(2)
        tree.setHeaderLabels(["Name", "Project", "Date", "Details"])
        tree.header().resizeSection(0, 250)
        tree.header().resizeSection(2, 85)
        self._tree = tree
        self._fill_tree()
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
    
    def _fill_tree(self):
        actions = self._get_actions()
        self._tree.clear()    
        for context in DBManager.get_contexts().values():
            item = self._get_context_item(context)
            for action in actions[context.id]:
                if not action.completed:
                    child_item = self._get_action_item(action)
                    item.addChild(child_item)
            self._tree.addTopLevelItem(item)

    def _get_context_item(self, context):
        item = QtGui.QTreeWidgetItem(QtCore.QStringList(context.name))
        item.setBackgroundColor(0, QtGui.QColor(context.color[22:29]))
        item.setTextColor(0, QtGui.QColor(context.color[38:45]))
        item.setIcon(0,QtGui.QIcon(context.icon or ""))
        item.setData(0,QtCore.Qt.UserRole, QtCore.QVariant(context))
        return item
        
    def _get_action_item(self, action):
        project = action.project.name if action.project else ""
        labels = [action.desc, project, action.sched.toString(DATE_FORMAT), action.details]
        item = QtGui.QTreeWidgetItem(QtCore.QStringList(labels))
        item.setData(0,QtCore.Qt.UserRole, QtCore.QVariant(action))
        return item
