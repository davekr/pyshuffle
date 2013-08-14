from PyQt4 import QtCore, QtGui

import buffer

from forms import ActionForm, ProjectForm
from models import Action

class Projects(object):
    def setup_projects(self, app, mainWidget):
        
        stack=QtGui.QStackedWidget(mainWidget.tab)
        
        projectsWidget=QtGui.QWidget(stack)
        projectsLayout=QtGui.QVBoxLayout(projectsWidget)

        self.treeWidget = QtGui.QTreeWidget(projectsWidget)
        self.treeWidget.setColumnCount(4)
        self.treeWidget.setHeaderLabels(["Name", "Context", "Date", "Details"])
        self.treeWidget.header().resizeSection(0, 130)
        self.treeWidget.header().resizeSection(2, 80)
        
        editButton = QtGui.QPushButton("Edit", projectsWidget)
        completeButton = QtGui.QPushButton("Complete", projectsWidget)
        deleteButton = QtGui.QPushButton("Delete", projectsWidget)
        
        buttonWidget=QtGui.QWidget(projectsWidget)
        buttonLayout=QtGui.QHBoxLayout(buttonWidget)
        buttonLayout.addWidget(editButton, 0)
        buttonLayout.addWidget(completeButton, 0)
        buttonLayout.addWidget(QtGui.QWidget(), 1)
        buttonLayout.addWidget(deleteButton, 0, QtCore.Qt.AlignRight)
        
        projectsLayout.addWidget(self.treeWidget)
        projectsLayout.addWidget(buttonWidget)
        
        stack.addWidget(projectsWidget)
        self.edit = ActionForm(stack, app, mainWidget, True)
        stack.addWidget(self.edit)
        self.editProject = ProjectForm(stack, app, mainWidget, True)
        stack.addWidget(self.editProject)
        
        def editAction():
            if len(self.treeWidget.selectedItems()) > 0:
                item = self.treeWidget.selectedItems()[0].data(0,QtCore.Qt.UserRole).toPyObject()
                if isinstance(item, Action):
                    stack.setCurrentIndex(1)
                    self.edit.edit(item)
                else:
                    stack.setCurrentIndex(2)
                    self.editProject.edit(item)
            else:
                mainWidget.statusBar.showMessage("Select item first",2000)
                
        def deleteAction():
            if len(self.treeWidget.selectedItems()) > 0:
                item = self.treeWidget.selectedItems()[0].data(0,QtCore.Qt.UserRole).toPyObject()
                if isinstance(item, Action):
                    buffer.deleteAction(app, item)
                    mainWidget.statusBar.showMessage("Action deleted",2000)
                else:
                    reply = QtGui.QMessageBox.question(projectsWidget, 'Are you sure?',"Project will be" 
                                                       +" deleted and project of all project's actions will"
                                                       + "be set to none.", 
                                               QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
                    if reply == QtGui.QMessageBox.Yes:
                        buffer.deleteProject(app, item)
                        mainWidget.statusBar.showMessage("Project deleted",2000)
            else:
                mainWidget.statusBar.showMessage("Select item first",2000)
                
        def completeAction():
            if len(self.treeWidget.selectedItems()) > 0:
                item = self.treeWidget.selectedItems()[0].data(0,QtCore.Qt.UserRole).toPyObject()
                if isinstance(item, Action):
                    buffer.completeAction(app, item)
                    mainWidget.statusBar.showMessage("Action completed",2000)
                else:
                    mainWidget.statusBar.showMessage("Project cannot be complete",2000)
            else:
                mainWidget.statusBar.showMessage("Select item first",2000)
        
        app.connect(editButton, QtCore.SIGNAL("clicked()"),editAction)
        app.connect(deleteButton, QtCore.SIGNAL("clicked()"),deleteAction)
        app.connect(completeButton, QtCore.SIGNAL("clicked()"),completeAction)
        app.connect(self.treeWidget, QtCore.SIGNAL("itemDoubleClicked (QTreeWidgetItem *,int)"), editAction)
        
        return stack  

    def refresh_projects(self):
        items = []
        for i in buffer.projectsBuffer.values():
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
