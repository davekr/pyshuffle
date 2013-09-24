from PyQt4 import QtCore, QtGui
from git import *

from app.forms import RepositoryForm
import app.buffer as buffer
from app.models import Action, Project
from settings import DATABASE
from app.static import icons
from app.tabs.tab import Tab

class Synchronization(QtGui.QStackedWidget, Tab):

    ICON = "sync"
    LABEL = "Synchronization"
    
    def _setup_content(self):
        self.repo = Repo(DATABASE)
        '''
        except InvalidGitRepositoryError:
            self.repo = Repo.create(app.db + "/.git")
            self.repo.git.execute(["git", "add", "shuffle.db"])
            self.repo.git.execute(["git", "commit", "-m", "'init'"])
        '''
        self.infos = []
        sync = self._setup_sync()
        conflict = self._setup_conflict()
        resolve = self._setup_resolve()
        self.addWidget(sync)
        self.addWidget(RepositoryForm(self.repo))
        self.addWidget(conflict)
        self.addWidget(resolve)

    def _setup_sync(self):
        selection = self._setup_selection()
        info_label = QtGui.QLabel("")
        sync = QtGui.QPushButton("Synchronize")
        sync.setMaximumSize(QtCore.QSize(80, 30))
        layout = QtGui.QVBoxLayout()
        layout.addWidget(selection, 0)
        layout.addWidget(QtGui.QLabel("<hr />"), 0)
        layout.addWidget(info_label, 1, QtCore.Qt.AlignTop)
        layout.addWidget(sync, 0, QtCore.Qt.AlignBottom)
        widget = QtGui.QWidget()
        widget.setLayout(layout)
        return widget

    def _setup_selection(self):
        choose_label = QtGui.QLabel("Choose remote repository to synchronize with: ")
        repo_select = QtGui.QComboBox()
        repo_select.addItem("None")
        create = QtGui.QPushButton("Create new repository")
        layout = QtGui.QHBoxLayout()
        layout.addWidget(choose_label, 0, QtCore.Qt.AlignRight)
        layout.addWidget(repo_select, 0, QtCore.Qt.AlignLeft)
        layout.addWidget(create, 0, QtCore.Qt.AlignLeft)
        layout.addWidget(QtGui.QWidget(), 1)
        widget = QtGui.QWidget()
        widget.setLayout(layout)
        return widget
        
    def _setup_conflict(self):
        bottom = self._setup_conflict_bottom()
        tree = self._setup_conflict_tree()
        layout = QtGui.QHBoxLayout()
        layout.addWidget(tree, 1)
        layout.addWidget(bottom, 0)
        widget = QtGui.QWidget()
        widget.setLayout(layout)
        return widget

    def _setup_conflict_tree(self):
        tree = QtGui.QTreeWidget()
        tree.setColumnCount(3)
        tree.setHeaderLabels(["From/To/Conflict", "Type", "Name"])
        tree.setToolTip("Displaying items that can be forwarded from server to \
                        local (To),\n forwarded from local to server (From) and \
                        conflicting items (Conflict).")
        self._conflict_tree = tree
        return tree

    def _setup_conflict_bottom(self):
        accept, detail, auto, end = self._setup_conflict_buttons()
        layout = QtGui.QVBoxLayout()
        layout.addWidget(accept)
        layout.addWidget(detail)
        layout.addStretch()
        layout.addWidget(auto)
        layout.addWidget(end)
        widget = QtGui.QWidget()
        widget.setLayout(layout)
        return widget

    def _setup_conflict_buttons(self):
        accept = QtGui.QPushButton("Proceed item")
        self.connect(accept, QtCore.SIGNAL("clicked()"), self.accept_item)
        detail = QtGui.QPushButton("Details")
        self.connect(detail, QtCore.SIGNAL("clicked()"), self.detail_item)
        auto = QtGui.QPushButton("Autosync")
        self.connect(auto, QtCore.SIGNAL("clicked()"), self.auto_sync)
        end = QtGui.QPushButton("End synchronization")
        self.connect(end, QtCore.SIGNAL("clicked()"), self.end_conflict)
        return accept, detail, auto, end
        
    def _setup_resolve(self):
        local_text = QtGui.QLabel()
        local_button = QtGui.QPushButton("Keep local")
        local_button.setMaximumSize(QtCore.QSize(80, 30))
        server_text = QtGui.QLabel()
        server_button = QtGui.QPushButton("Replace with server")
        server_button.setMaximumSize(QtCore.QSize(120, 30))
        layout = QtGui.QGridLayout()
        layout.addWidget(local_text, 0, 0, QtCore.Qt.AlignTop)
        layout.addWidget(server_text, 0, 1, QtCore.Qt.AlignTop)
        layout.addWidget(local_button, 1, 0, QtCore.Qt.AlignBottom)
        layout.addWidget(server_button, 1, 1, QtCore.Qt.AlignBottom)
        widget = QtGui.QWidget()
        widget.setLayout(layout)
        return widget
        
    def create_dialog(self):
        self.setCurrentIndex(1)
        
    def synchronize(self):
        text = unicode(self.repoComboBox.currentText())
        if(text == "None"):
            self.window().show_status("Select valid remote repository")
        else:
            self.repo.git.execute(["git", "fetch", text])
            output = ""
            try:
                buffer.closeConn(app)
                output = "Local: " + self.repo.git.execute(["git", "merge", text+"/master"])
                mainWidget.statusBar.showMessage("Trying to fetch from remote repository. This may take a while" +
                                                  " depends on size of transfering data.",4000)
                buffer.openConn(app)
                buffer.clearBuffer()
                buffer.init_buffer(app)
                app.refresh(app)
                
                self.repo.git.execute(["git", "push", text])
                output = output + "\nServer: Pushed"
                self.info_label.setText(output)
                self.infos[self.repoComboBox.currentIndex()-1] = output
                QtGui.QMessageBox.information(syncWidget, "Success", "Synchronization completed")
            # auto merge failed
            except GitCommandError:
                self.repo.git.execute(["git", "checkout", text+"/master", "shuffle.db"])
                buffer.openConn(app)
                buffer.init_buffer(app, True)
                self.fillConflict()
                app.inSync = True
                stack.setCurrentIndex(2)
            
    def message(self, page):
        if page == 0:
            self.info_label.setText("")
        else:
            self.info_label.setText(self.infos[page-1])
    
    def end_conflict(self):
        reply = QtGui.QMessageBox.question(conflictWidget, 'Are you sure?',"All unresolved conflicts will" 
                                           + " keep local version and all non-added items will be deleted.", 
                                           QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
        if reply == QtGui.QMessageBox.Yes:
            for i in range(self.treeWidget.topLevelItemCount()):
                item = self.treeWidget.topLevelItem(i)
                data = item.data(0,QtCore.Qt.UserRole).toPyObject()
                if item.text(0) == "Conflict":
                    if isinstance(data, Action):
                        buffer.actionsBuffer[data.id].simpleCreate(app, True)
                    elif isinstance(data, Project):
                        buffer.projectsBuffer[data.id].simpleCreate(app, True)
                    else:
                        buffer.contextsBuffer[data.id].simpleCreate(app, True)
                elif item.text(0) == "To":
                    data.simpleDelete(app)
            mergeResolved()
            
    def accept_item(self):
        if isItemSelected():
            item = self.treeWidget.selectedItems()[0]
            data = item.data(0,QtCore.Qt.UserRole).toPyObject()
            if item.text(0) == "From":
                data.simpleCreate(app)
                self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(item))
            elif item.text(0) == "To":
                self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(item))
            elif item.text(0) == "Conflict":
                serverText.setText("Server\n\n" + data.toString())
                if isinstance(data, Action):
                    localText.setText("Local\n\n" + buffer.actionsBuffer[data.id].toString())
                elif isinstance(data, Project):
                    localText.setText("Local\n\n" + buffer.projectsBuffer[data.id].toString())
                else:
                    localText.setText("Local\n\n" + buffer.contextsBuffer[data.id].toString())
                stack.setCurrentIndex(3)
            if not self.treeWidget.topLevelItemCount():
                mergeResolved()
    
    def choose_server(self):
        item = self.treeWidget.selectedItems()[0]
        self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(item))
        if not self.treeWidget.topLevelItemCount():
                mergeResolved()
        else:
            stack.setCurrentIndex(2)
        
    def choose_local(self):
        item = self.treeWidget.selectedItems()[0]
        data = item.data(0,QtCore.Qt.UserRole).toPyObject()
        if isinstance(data, Action):
            buffer.actionsBuffer[data.id].simpleCreate(app, True)
        elif isinstance(data, Project):
            buffer.projectsBuffer[data.id].simpleCreate(app, True)
        else:
            buffer.contextsBuffer[data.id].simpleCreate(app, True)
        self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(item))
        if not self.treeWidget.topLevelItemCount():
                mergeResolved()
        else:
            stack.setCurrentIndex(2)
    
    def detail_item(self):
        if isItemSelected():
            item = self.treeWidget.selectedItems()[0]
            data = item.data(0,QtCore.Qt.UserRole).toPyObject()
            QtGui.QMessageBox.information(conflictWidget, "Detail", data.toString())
    
    def auto_sync(self):
        delete = [] # cannot delete while looping
        for i in range(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(i)
            data = item.data(0,QtCore.Qt.UserRole).toPyObject()
            if item.text(0) == "From":
                data.simpleCreate(app)
                delete.append(item)
            elif item.text(0) == "To":
                delete.append(item)
        for item in delete:
            self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(item))
        if self.treeWidget.topLevelItemCount():
            QtGui.QMessageBox.information(syncWidget, "Info", "There are conflicting items"  
                                            + " that can't be auto synchronized. Resolve conflict"
                                            + " by yourself.")
        else:
            mergeResolved()
            
    
    def isItemSelected(self):
        if len(self.treeWidget.selectedItems()) > 0:
            return True
        else:
            mainWidget.statusBar.showMessage("Select item first",2000)
            return False
        
    def merge_resolved(self):
        try:
            self.repo.git.execute(["git", "add", "shuffle.db"])
            self.repo.git.execute(["git","commit","-m", "'merge resolved by user'"])
        except GitCommandError:
            pass #nothing to commit (working directory clean)
        # here is the bug, to prevent use >>> git reset --hard >>> git pull
        self.repo.git.execute(["git", "push", unicode(self.repoComboBox.currentText())])
        output = "Local: Merge completed\nServer: Pushed"
        
        buffer.clearTempBuffer()
        buffer.clearBuffer()
        buffer.init_buffer(app)
        app.refresh(app)
        
        app.inSync = False
        infoLabel.setText(output)
        self.infos[self.repoComboBox.currentIndex()-1] = output
        stack.setCurrentIndex(0)
        QtGui.QMessageBox.information(syncWidget, "Success", "Synchronization completed")
        
        app.connect(createButton, QtCore.SIGNAL("clicked()"), createDialog)
        app.connect(syncButton, QtCore.SIGNAL("clicked()"), synchronize)
        app.connect(self.repoComboBox, QtCore.SIGNAL("activated(int)"), message)
        app.connect(localButton, QtCore.SIGNAL("clicked()"), chooseLocal)
        app.connect(serverButton, QtCore.SIGNAL("clicked()"), chooseServer)
    
    def refresh_sync(self):
        self.infos = []
        self.repoComboBox.clear()
        self.repoComboBox.addItem("None")
        result = self.repo.git.execute(["git","remote"])
        remotes = result.split()
        if len(result) > 0:
            for i in remotes:
                self.infos.append("No synchronization has been done lately")
                self.repoComboBox.addItem(i)
        
    def fillConflict(self):
        '''
        In buffer are local items, in tempbuffer are server items. For every local item
        find if server equivalent exists - if so, check hashes and accordingly show conflict or
        do nothing, item is already on server and local too. Delete the item from tempBuffer.
                                         - if no, show arrow, which means this item will be added
        to server. 
        Now in tempbuffer are only items, which are only on server. Show that items with arrow, they
        will be added to local.
        Do it for action, project and context buffers...
        '''
        self.treeWidget.clear()
        items = []
        for i in buffer.actionsBuffer:
            found = False
            for j in buffer.tempActionBuffer:
                if j == i:
                    found = True
                    if buffer.tempActionBuffer[j].generateHash() != buffer.actionsBuffer[i].generateHash():
                        action = QtGui.QTreeWidgetItem(QtCore.QStringList(["Conflict","Action",buffer.tempActionBuffer[j].desc]))
                        action.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(buffer.tempActionBuffer[j]))
                        self.colors(action, "#CF2501")
                        action.setIcon(0, QtGui.QIcon(icons['syncconflict']))
                        items.append(action)
                    del buffer.tempActionBuffer[j]
                    break
            if not found:
                action = QtGui.QTreeWidgetItem(QtCore.QStringList(["From","Action",buffer.actionsBuffer[i].desc]))
                action.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(buffer.actionsBuffer[i]))
                self.colors(action, "#57881B")
                action.setIcon(0, QtGui.QIcon(icons['syncfrom']))
                items.append(action)
                
        for i in buffer.tempActionBuffer.values():
            action = QtGui.QTreeWidgetItem(QtCore.QStringList(["To","Action",i.desc]))
            action.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(i))
            self.colors(action, "#57881B")
            action.setIcon(0, QtGui.QIcon(icons['syncto']))
            items.append(action)
            
        for i in buffer.projectsBuffer:
            found = False
            for j in buffer.tempProjectBuffer:
                if j == i:
                    found = True
                    if buffer.tempProjectBuffer[j].generateHash() != buffer.projectsBuffer[i].generateHash():
                        project = QtGui.QTreeWidgetItem(QtCore.QStringList(["Conflict","Project",buffer.tempProjectBuffer[j].name]))
                        project.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(buffer.tempProjectBuffer[j]))
                        self.colors(project, "#CF2501")
                        project.setIcon(0, QtGui.QIcon(icons['syncconflict']))
                        items.append(project)
                    del buffer.tempProjectBuffer[j]
                    break
            if not found:
                project = QtGui.QTreeWidgetItem(QtCore.QStringList(["From","Project",buffer.projectsBuffer[i].name]))
                project.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(buffer.projectsBuffer[i]))
                self.colors(project, "#57881B")
                project.setIcon(0, QtGui.QIcon(icons['syncfrom']))
                items.append(project)
        for i in buffer.tempProjectBuffer.values():
            project = QtGui.QTreeWidgetItem(QtCore.QStringList(["To","Project",i.name]))
            project.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(i))
            self.colors(project, "#57881B")
            project.setIcon(0, QtGui.QIcon(icons['syncto']))
            items.append(project)
            
        for i in buffer.contextsBuffer:
            found = False
            for j in buffer.tempContextBuffer:
                if j == i:
                    found = True
                    if buffer.tempContextBuffer[j].generateHash() != buffer.contextsBuffer[i].generateHash():
                        context = QtGui.QTreeWidgetItem(QtCore.QStringList(["Conflict","Context",buffer.tempContextBuffer[j].name]))
                        context.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(buffer.tempContextBuffer[j]))
                        self.colors(context, "#CF2501")
                        context.setIcon(0, QtGui.QIcon(icons['syncconflict']))
                        items.append(context)
                    del buffer.tempContextBuffer[j]
                    break
            if not found:
                context = QtGui.QTreeWidgetItem(QtCore.QStringList(["From","Context",buffer.contextsBuffer[i].name]))
                context.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(buffer.contextsBuffer[i]))
                self.colors(context, "#57881B")
                context.setIcon(0, QtGui.QIcon(icons['syncfrom']))
                items.append(context)
        for i in buffer.tempContextBuffer.values():
            context = QtGui.QTreeWidgetItem(QtCore.QStringList(["To","Context",i.name]))
            context.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(i))
            self.colors(context, "#57881B")
            context.setIcon(0, QtGui.QIcon(icons['syncto']))
            items.append(context)
            
        self.treeWidget.addTopLevelItems(items)
        
    def colors(self, item, color):
        for i in range(3):
            pass
            #item.setBackgroundColor(i, QtGui.QColor(color))
            
                    
