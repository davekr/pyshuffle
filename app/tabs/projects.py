from PyQt4 import QtCore, QtGui
from collections import defaultdict

from app.forms import ActionForm, ProjectForm
from app.dbmanager import DBManager
from app.tabs.tab import Tab
from app.utils import event_register
from settings import DATE_FORMAT

class Projects(QtGui.QStackedWidget, Tab):

    ICON = "projects"
    LABEL = "Projects"

    def _setup_content(self):
        project_list = self._setup_projects()
        action_form = ActionForm(True)
        project_form = ProjectForm(True)
        self.addWidget(project_list)
        self.addWidget(action_form)
        self.addWidget(project_form)
        self._action_form = action_form
        self._project_form = project_form
        
    def _connect_events(self):
        self.connect(self._tree, QtCore.SIGNAL("itemDoubleClicked (QTreeWidgetItem *,int)"), self.edit_item)
        event_register.project_change.connect(self._fill_tree)
        event_register.action_change.connect(self._fill_tree)
        event_register.context_change.connect(self._fill_tree)

    def _setup_projects(self):
        tree = self._setup_tree()
        bottom = self._setup_bottom()
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tree)
        layout.addWidget(bottom)
        projects_widget = QtGui.QWidget()
        projects_widget.setLayout(layout)
        return projects_widget

    def _setup_tree(self):
        tree_widget = QtGui.QTreeWidget()
        tree_widget.setColumnCount(4)
        tree_widget.setHeaderLabels(["Name", "Context", "Date", "Details"])
        tree_widget.header().resizeSection(0, 250)
        tree_widget.header().resizeSection(2, 85)
        self._tree = tree_widget
        self._fill_tree()
        return tree_widget

    def _setup_bottom(self):
        edit, complete, delete = self._setup_buttons()
        layout = QtGui.QHBoxLayout()
        layout.addWidget(edit, 0)
        layout.addWidget(complete, 0)
        layout.addWidget(QtGui.QWidget(), 1)
        layout.addWidget(delete, 0, QtCore.Qt.AlignRight)
        buttons_widget = QtGui.QWidget()
        buttons_widget.setLayout(layout)
        return buttons_widget

    def _setup_buttons(self):
        edit = QtGui.QPushButton("Edit")
        self.connect(edit, QtCore.SIGNAL("clicked()"), self.edit_item)
        complete = QtGui.QPushButton("Complete")
        self.connect(complete, QtCore.SIGNAL("clicked()"), self.complete_item)
        delete = QtGui.QPushButton("Delete")
        self.connect(delete, QtCore.SIGNAL("clicked()"), self.delete_item)
        return edit, complete, delete
        

    def edit_item(self):
        self._perform_action('edit')

    def delete_item(self):
        self._perform_action('delete')

    def complete_item(self):
        self._perform_action('complete')

    def _perform_action(self, action):
        if self._item_selected():
            item = self._tree.selectedItems()[0].data(0,QtCore.Qt.UserRole).toPyObject()
            fnc = getattr(self,'_%s_%s' % (action, item.class_name()))
            fnc(item)

    def _edit_action(self, action):
        self.setCurrentIndex(1)
        self._action_form.set_action(action)

    def _edit_project(self, project):
        self.setCurrentIndex(2)
        self._project_form.set_project(project)
            
    def _delete_action(self, action):
        action.delete()
        self.window().show_status("Action deleted")
        event_register.action_change.emit()

    def _delete_project(self, project):
        reply = QtGui.QMessageBox.question(self, 'Are you sure?',"Project will be" 
                                           +" deleted and project of all project's actions will"
                                           + "be set to none.", 
                                   QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
        if reply == QtGui.QMessageBox.Yes:
            project.delete()
            self.window().show_status("Project deleted")
            event_register.project_change.emit()
            
    def _complete_action(self, action):
        action.completed = True
        action.save()
        self.window().show_status("Action completed")
        event_register.action_change.emit()

    def _complete_project(self, project):
        self.window().show_status("Project cannot be complete")

    def _item_selected(self):
        if len(self._tree.selectedItems()) > 0:
            return True
        else:
            self.window().show_status("Select item first")

    def _fill_tree(self):
        actions = self._get_actions()
        self._tree.clear()
        for project in DBManager.get_projects().values():
            item = self._get_project_item(project)
            item.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(project))
            for action in actions[project.id]:
                if not action.completed:
                    child_item = self._get_action_item(action)
                    item.addChild(child_item)
            self._tree.addTopLevelItem(item)

    def _get_actions(self):
        actions = defaultdict(list)
        for action in DBManager.get_actions().values():
            if action.project:
                actions[action.project.id].append(action) 
        return actions

    def _get_project_item(self, project):
        if project.context:
            item = QtGui.QTreeWidgetItem(QtCore.QStringList([project.name, project.context.name]))
            item.setBackgroundColor(1, QtGui.QColor(project.context.color[22:29]))
            item.setTextColor(1, QtGui.QColor(project.context.color[38:45]))
            if project.context.icon:
                item.setIcon(1, QtGui.QIcon(str(project.context.icon)))
        else:
            item = QtGui.QTreeWidgetItem(QtCore.QStringList([project.name, ""]))
        return item

    def _get_action_item(self, action):
        if action.context:
            labels = [action.desc, action.context.name, action.sched.toString(DATE_FORMAT), action.details]
            item = QtGui.QTreeWidgetItem(QtCore.QStringList(labels))
            item.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(action))
            item.setBackgroundColor(1, QtGui.QColor(action.context.color[22:29]))
            item.setTextColor(1, QtGui.QColor(action.context.color[38:45]))
            if action.context.icon:
                item.setIcon(1, QtGui.QIcon(str(action.context.icon)))
        else:
            labels = [action.desc, "", action.sched.toString(DATE_FORMAT), action.details]
            item = QtGui.QTreeWidgetItem(QtCore.QStringList(labels))
        return item
