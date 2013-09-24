from PyQt4 import QtCore, QtGui

from app.forms import ActionForm, ProjectForm
from app.models import Action
from app.dbmanager import DBManager
from app.tabs.tab import Tab

class Projects(QtGui.QStackedWidget, Tab):

    ICON = "projects"
    LABEL = "Projects"

    def _setup_content(self):
        project_list = self._setup_projects()
        self.addWidget(project_list)
        self.addWidget(ActionForm(True))
        self.addWidget(ProjectForm(True))
        
    def _connect_events(self):
        self.connect(self._tree, QtCore.SIGNAL("itemDoubleClicked (QTreeWidgetItem *,int)"), self.edit_action)

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
        tree_widget.header().resizeSection(0, 130)
        tree_widget.header().resizeSection(2, 80)
        self._tree = tree_widget
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
        self.connect(edit, QtCore.SIGNAL("clicked()"), self.edit_action)
        complete = QtGui.QPushButton("Complete")
        self.connect(complete, QtCore.SIGNAL("clicked()"), self.complete_action)
        delete = QtGui.QPushButton("Delete")
        self.connect(delete, QtCore.SIGNAL("clicked()"), self.delete_action)
        return edit, complete, delete
        

    def edit_action(self):
        if len(self.treeWidget.selectedItems()) > 0:
            item = self.treeWidget.selectedItems()[0].data(0,QtCore.Qt.UserRole).toPyObject()
            if isinstance(item, Action):
                self.setCurrentIndex(1)
                self.edit.edit(item)
            else:
                self.setCurrentIndex(2)
                self.editProject.edit(item)
        else:
            self.window().show_status("Select item first")
            
    def delete_action(self):
        if len(self.treeWidget.selectedItems()) > 0:
            item = self.treeWidget.selectedItems()[0].data(0,QtCore.Qt.UserRole).toPyObject()
            if isinstance(item, Action):
                DBManager.delete_action(item)
                self.window().show_status("Action deleted")
            else:
                reply = QtGui.QMessageBox.question(self, 'Are you sure?',"Project will be" 
                                                   +" deleted and project of all project's actions will"
                                                   + "be set to none.", 
                                           QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
                if reply == QtGui.QMessageBox.Yes:
                    DBManager.delete_project(item)
                    self.window().show_status("Project deleted")
        else:
            self.window().show_status("Select item first")
            
    def complete_action(self):
        if len(self.treeWidget.selectedItems()) > 0:
            item = self.treeWidget.selectedItems()[0].data(0,QtCore.Qt.UserRole).toPyObject()
            if isinstance(item, Action):
                DBManager.update_action(item)
                self.window().show_status("Action completed")
            else:
                self.window().show_status("Project cannot be complete")
        else:
            self.window().show_status("Select item first")

    def refresh_projects(self):
        items = []
        for i in DBManager.get_projects().values():
            defContext = ""
            if i.context:
                defContext = i.context.name
                
            project = QtGui.QTreeWidgetItem(QtCore.QStringList([i.name,defContext]))
            project.setData(0,QtCore.Qt.UserRole, QtCore.QVariant(i))
            
            if i.context:
                project.setBackgroundColor(1, QtGui.QColor(i.context.color[22:29]))
                project.setTextColor(1, QtGui.QColor(i.context.color[38:45]))
                if i.context.icon:
                    project.setIcon(1, QtGui.QIcon(str(i.context.icon)))
                    
            for j in i.actions.values():
                if not j.completed:
                    context = ""
                    if j.context:
                        context = j.context.name
                    child = QtGui.QTreeWidgetItem(QtCore.QStringList([j.desc,context,
                                                                  j.sched.toString('yyyy-MM-dd'),
                                                                  j.details]))
                    child.setData(0,QtCore.Qt.UserRole, QtCore.QVariant(j))
                
                    if j.context:
                        child.setBackgroundColor(1, QtGui.QColor(j.context.color[22:29]))
                        child.setTextColor(1, QtGui.QColor(j.context.color[38:45]))
                        if j.context.icon:
                            child.setIcon(1, QtGui.QIcon(str(j.context.icon)))
                        
                    project.addChild(child)
            items.append(project)
            
        self.treeWidget.clear()    
        self.treeWidget.addTopLevelItems(items)
        self.edit.refreshAction()
        self.editProject.refreshProject()
