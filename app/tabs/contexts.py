from PyQt4 import QtCore, QtGui
from collections import defaultdict

from app.forms import ActionForm, ContextForm
from app.dbmanager import DBManager
from projects import Projects
from settings import DATE_FORMAT
from app.utils import event_register
from app.static import styles, contexticons

class Contexts(Projects):

    ICON = "contexts"
    LABEL = "Contexts"

    def _setup_content(self):
        context_list = self._setup_projects()
        self.addWidget(context_list)
        action_form = ActionForm(True)
        context_form = ContextForm(True)
        self.addWidget(action_form)
        self.addWidget(context_form)
        self._action_form = action_form
        self._context_form = context_form

    def _setup_tree(self):
        tree = QtGui.QTreeWidget()
        tree.setColumnCount(2)
        tree.setHeaderLabels(["Name", "Project", "Date", "Details"])
        tree.header().resizeSection(0, 200)
        tree.header().resizeSection(1, 150)
        tree.header().resizeSection(2, 85)
        self._tree = tree
        self._fill_tree()
        return tree
        
    def _edit_context(self, context):
        self.setCurrentIndex(2)
        self._context_form.set_context(context)
            
    def _delete_context(self, context):
        reply = QtGui.QMessageBox.question(self, 'Are you sure?',"Context will be" 
                                           +" deleted and context of all context's actions will" 
                                           + "be set to none.", 
                                   QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
        if reply == QtGui.QMessageBox.Yes:
            context.delete()
            self.window().show_status("Context deleted")
            event_register.context_change.emit()
            
    def _complete_context(self, context):
        self.window().show_status("Context cannot be completed")
    
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

    def _get_actions(self):
        actions = defaultdict(list)
        for action in DBManager.get_actions().values():
            if action.context:
                actions[action.context.id].append(action) 
        return actions

    def _get_context_item(self, context):
        item = QtGui.QTreeWidgetItem(QtCore.QStringList(context.name))
        item.setBackgroundColor(0, QtGui.QColor(styles[context.color]["background"]))
        item.setTextColor(0, QtGui.QColor(styles[context.color]["text"]))
        item.setIcon(0, QtGui.QIcon(contexticons.get(context.icon, "")))
        item.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(context))
        return item
        
    def _get_action_item(self, action):
        project = action.project.name if action.project else ""
        labels = [action.desc, project, action.sched.toString(DATE_FORMAT), action.details]
        item = QtGui.QTreeWidgetItem(QtCore.QStringList(labels))
        item.setData(0,QtCore.Qt.UserRole, QtCore.QVariant(action))
        return item
