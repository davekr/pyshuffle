from PyQt4 import QtCore, QtGui
import git
import datetime

from static import icons, styles
from models import Action, Project, Context
import buffer

class ActionForm(QtGui.QWidget):
    
    def __init__(self, parent, app, mainWidget, edit=False):
        QtGui.QWidget.__init__(self)
        self.app = app
        self.mainWidget = mainWidget
        self.editable=edit
        
        actionLayout=QtGui.QHBoxLayout(self)
        contentWidget=QtGui.QWidget(self)
        
        self.contentLayout=QtGui.QGridLayout(contentWidget)
        
        self.contentLayout.addWidget(QtGui.QLabel("Description"), 0, 0)
        self.descLineEdit=MyLineEdit("My action")
        self.contentLayout.addWidget(self.descLineEdit, 0, 1)
        
        self.contentLayout.addWidget(QtGui.QLabel("Project"), 1, 0)
        
        self.projectComboBox=QtGui.QComboBox(contentWidget)
        self.contentLayout.addWidget(self.projectComboBox, 1, 1)
        
        self.contentLayout.addWidget(QtGui.QLabel("Context"), 2, 0)
        
        self.contextComboBox=QtGui.QComboBox(contentWidget)
        self.contentLayout.addWidget(self.contextComboBox, 2, 1)
        
        self.contentLayout.addWidget(QtGui.QLabel("Details"), 3, 0)
        
        self.details = MyLineEdit("Description of my action")
        self.contentLayout.addWidget(self.details, 3, 1)
        
        self.contentLayout.addWidget(QtGui.QLabel("Scheduling"), 4, 0)
        
        self.sched=QtGui.QCheckBox()
        self.sched.setFocusPolicy(QtCore.Qt.NoFocus)
        self.contentLayout.addWidget(self.sched, 4, 1)
        
        self.dateInput=QtGui.QDateEdit(datetime.date.today())
        self.dateInput.setHidden(True)
        self.contentLayout.addWidget(self.dateInput, 5, 1)
        
        self.saveButton=QtGui.QPushButton("Save")
        
        if edit:
            cancelButton=QtGui.QPushButton("Back")
            self.contentLayout.addWidget(cancelButton, 6, 0, QtCore.Qt.AlignBottom)
            self.connect(cancelButton, QtCore.SIGNAL("clicked()"), self.cancel)
            self.saveButton.setMaximumSize(QtCore.QSize(80, 30))
            self.contentLayout.addWidget(self.saveButton, 6, 1, QtCore.Qt.AlignBottom)
        else:
            self.contentLayout.addWidget(self.saveButton, 6, 0, QtCore.Qt.AlignBottom)

        
        actionLayout.addWidget(contentWidget, 1)
        actionLayout.addWidget(QtGui.QWidget(self), 1)
        
        self.connect(self.sched, QtCore.SIGNAL("stateChanged(int)"),self.showSched)
        self.connect(self.saveButton, QtCore.SIGNAL("clicked()"),self.saveAction)
        
    def edit(self, action):
        self.actionId = action.id
        self.projectId = None
        self.contextId = None
        
        self.descLineEdit.setText(action.desc)
        
        if action.project:
            self.projectId = action.project.id
            for i in range(self.projectComboBox.count()):
                data = self.projectComboBox.itemData(i).toPyObject()
                if data!=NotImplemented and data.id == action.project.id:
                    self.projectComboBox.setCurrentIndex(i)
                    break
                
        if action.context:
            self.contextId = action.context.id
            for i in range(self.contextComboBox.count()):
                data = self.contextComboBox.itemData(i).toPyObject()
                if data!=NotImplemented and data.id == action.context.id:
                    self.contextComboBox.setCurrentIndex(i)
                    break
            
        self.details.setText(action.details)
        if action.sched.isValid():
            self.sched.toggle()
            self.dateInput.setDate(action.sched)
        
    def cancel(self):
        self.parent().setCurrentIndex(self.parent().currentIndex() - 1)
        self.setDefault()
            
    def showSched(self, state):
        if(state):
            self.dateInput.setHidden(False)
        else:
            self.dateInput.setHidden(True)

    def saveAction(self):
        data=self.projectComboBox.itemData(self.projectComboBox.currentIndex())
        project = data.toPyObject()
        data=self.contextComboBox.itemData(self.contextComboBox.currentIndex())
        context = data.toPyObject()
        
        if project == NotImplemented:
            project = None
        if context == NotImplemented:
            context = None

        dat = QtCore.QDate()
        if self.sched.isChecked():
            dat = self.dateInput.date() 
            
        detail = unicode(self.details.text())
        
        action = Action(None, unicode(self.descLineEdit.text()), project, context, dat, detail, 
                        0, self.app.cursor)
        
        if self.editable:
            action.id = self.actionId
            
            buffer.updateAction(self.app, action, self.projectId, self.contextId)
            
            self.mainWidget.statusBar.showMessage("Action updated",2000)
            
            self.cancel() #not cancel but I use function in method
        else:
            buffer.createAction(self.app, action)
            
            self.mainWidget.statusBar.showMessage("Action created",2000)
            
            self.setDefault()
        
    def setDefault(self):
        self.descLineEdit.setText("My action")
        self.projectComboBox.setCurrentIndex(0)
        self.contextComboBox.setCurrentIndex(0)
        self.details.setText("Description of my action")
        self.dateInput.setDate(datetime.date.today())
        self.sched.setCheckState(QtCore.Qt.Unchecked)
        
        
    def refreshAction(self):
        self.projectComboBox.clear()
        self.projectComboBox.addItem("None")
        self.contextComboBox.clear()
        self.contextComboBox.addItem("None")
        for project in buffer.projectsBuffer.values():
            self.projectComboBox.addItem(project.name, QtCore.QVariant(project))
        for context in buffer.contextsBuffer.values():
            self.contextComboBox.addItem(context.name, QtCore.QVariant(context))
        
class ProjectForm(QtGui.QWidget):
    
    def __init__(self, parent, app, mainWidget, edit=False):
        QtGui.QWidget.__init__(self)
        self.app = app
        self.mainWidget = mainWidget
        self.editable = edit
        
        projectLayout=QtGui.QHBoxLayout(self)
        projectWidget=QtGui.QWidget(self)
        
        self.contentLayout=QtGui.QGridLayout(projectWidget)
        
        self.contentLayout.addWidget(QtGui.QLabel("Name"), 0, 0)
        
        self.projectNameEdit=MyLineEdit("My project")
        self.contentLayout.addWidget(self.projectNameEdit, 0, 1)
        
        self.contentLayout.addWidget(QtGui.QLabel("Default context"), 1, 0)
        
        self.contextComboBox=QtGui.QComboBox()
        self.contentLayout.addWidget(self.contextComboBox, 1, 1)
                
        projectSaveButton=QtGui.QPushButton("Save")
        
        if edit:
            cancelButton=QtGui.QPushButton("Back")
            self.contentLayout.addWidget(cancelButton, 2, 0, QtCore.Qt.AlignBottom)
            self.connect(cancelButton, QtCore.SIGNAL("clicked()"), self.cancel)
            projectSaveButton.setMaximumSize(QtCore.QSize(80, 30))
            self.contentLayout.addWidget(projectSaveButton, 2, 1, QtCore.Qt.AlignBottom)
        else:
            self.contentLayout.addWidget(projectSaveButton, 2, 0, QtCore.Qt.AlignBottom)
        
        
        projectLayout.addWidget(projectWidget, 1)
        projectLayout.addWidget(QtGui.QWidget(self), 1)
        
        self.connect(projectSaveButton, QtCore.SIGNAL("clicked()"),self.saveProject)
        
    def edit(self, project):
        self.project = project
        self.projectNameEdit.setText(project.name)
        if project.context:
            for i in range(self.contextComboBox.count()):
                data = self.contextComboBox.itemData(i).toPyObject()
                if data!=NotImplemented and data.id == project.context.id:
                    self.contextComboBox.setCurrentIndex(i)
                    break
        
    def cancel(self):
        self.parent().setCurrentIndex(self.parent().currentIndex() - 2)
        self.setDefault()
    
    def saveProject(self):
        name = unicode(self.projectNameEdit.text())
        data=self.contextComboBox.itemData(self.contextComboBox.currentIndex())
        context = data.toPyObject()
        if context == NotImplemented:
            context = None

        if self.editable:
            self.project.name = name
            self.project.context = context
            
            buffer.createProject(self.app, self.project, True)
            
            self.mainWidget.statusBar.showMessage("Project updated",2000)
            
            self.cancel() #not cancel but I use function in method
        else:
            project = Project(None, name, context, self.app.cursor)
            
            buffer.createProject(self.app, project)
            
            self.mainWidget.statusBar.showMessage("Project created",2000)
        
            self.setDefault()
        
    def setDefault(self):
        self.projectNameEdit.setText("My project")
        self.contextComboBox.setCurrentIndex(0)
        
    def refreshProject(self):
        self.contextComboBox.clear()
        self.contextComboBox.addItem("None")
        for context in buffer.contextsBuffer.values():
            self.contextComboBox.addItem(context.name, QtCore.QVariant(context))
    
class ContextForm(QtGui.QWidget):
    
    def __init__(self, parent, app, mainWidget, edit=False):
        QtGui.QWidget.__init__(self)
        self.app = app
        self.mainWidget = mainWidget
        self.editAble = edit
        
        contextLayout=QtGui.QHBoxLayout(self)
        contextWidget=QtGui.QWidget(self)
        
        self.contentLayout=QtGui.QGridLayout(contextWidget)
        
        self.contentLayout.addWidget(QtGui.QLabel("Name"), 0, 0)
        
        self.contextLineEdit = MyLineEdit("My context")
        self.contentLayout.addWidget(self.contextLineEdit, 0, 1)
        
        self.contentLayout.addWidget(QtGui.QLabel("Color"), 1, 0)
        
        self.colorButton = QtGui.QToolButton()
        self.colorButton.setText("Abc")
        self.colorButton.setStyleSheet("* { background-color: #DEDFEF; color: #5A6984 }")
        self.contentLayout.addWidget(self.colorButton, 1, 1)
        
        self.contentLayout.addWidget(QtGui.QLabel("Icon"), 2, 0)
        
        self.iconButton= QtGui.QToolButton()
        self.iconButton.setText("No icon")
        self.contentLayout.addWidget(self.iconButton, 2, 1)
        #color page
        self.chooseColor=QtGui.QWidget(self)
        colorLayout=QtGui.QGridLayout(self.chooseColor)
        
        colorMapper = QtCore.QSignalMapper(mainWidget)
        for (counter, i) in enumerate(styles):
            button = QtGui.QToolButton()
            button.setText("Abc")
            button.setStyleSheet(styles[i])
            app.connect(button, QtCore.SIGNAL("clicked()"), colorMapper, QtCore.SLOT("map()"))
            colorMapper.setMapping(button, styles[i])
            colorLayout.addWidget(button, counter / 6, counter % 6)
        
        #icon page
        self.chooseIcon=QtGui.QWidget(self)
        iconLayout=QtGui.QGridLayout(self.chooseIcon)
        noIcon = QtGui.QToolButton()
        noIcon.setText("No icon")
        iconMapper = QtCore.QSignalMapper(mainWidget)
        for (counter, i) in enumerate(icons):
            button = QtGui.QToolButton()
            button.setIcon(QtGui.QIcon(icons[i]))
            app.connect(button, QtCore.SIGNAL("clicked()"), iconMapper, QtCore.SLOT("map()"))
            iconMapper.setMapping(button, icons[i])
            iconLayout.addWidget(button, counter / 6, counter % 6, QtCore.Qt.AlignCenter)
        
        iconLayout.addWidget(noIcon, 4, 1, QtCore.Qt.AlignCenter)
        
        contextSaveButton=QtGui.QPushButton("Save")
        
        if edit:
            cancelButton=QtGui.QPushButton("Back")
            self.contentLayout.addWidget(cancelButton, 3, 0, QtCore.Qt.AlignBottom)
            self.connect(cancelButton, QtCore.SIGNAL("clicked()"), self.cancel)
            contextSaveButton.setMaximumSize(QtCore.QSize(80, 30))
            self.contentLayout.addWidget(contextSaveButton, 3, 1, QtCore.Qt.AlignBottom)
        else:
            self.contentLayout.addWidget(contextSaveButton, 3, 0, QtCore.Qt.AlignBottom)
        
        
        contextLayout.addWidget(contextWidget, 1)
        contextLayout.addWidget(QtGui.QWidget(self), 1)
        
        self.iconPath = None
        
        self.connect(contextSaveButton, QtCore.SIGNAL("clicked()"),self.saveContext)
        self.connect(self.colorButton, QtCore.SIGNAL("clicked()"), self.showPallete)
        self.connect(self.iconButton, QtCore.SIGNAL("clicked()"), self.showIcons)
        self.connect(colorMapper, QtCore.SIGNAL("mapped(const QString &)"), self.colorChoose)
        self.connect(iconMapper, QtCore.SIGNAL("mapped(const QString &)"), self.iconChoose)
        self.connect(noIcon, QtCore.SIGNAL("clicked()"), self.setNoIcon)
                
    def edit(self, context):
        self.context = context
        self.contextLineEdit.setText(context.name)
        self.colorButton.setStyleSheet(context.color)
        if context.icon:
            self.iconButton.setIcon(QtGui.QIcon(context.icon))
            self.iconPath = context.icon
        
    def cancel(self):
        self.parent().setCurrentIndex(self.parent().currentIndex() - 2)
        self.setDefault()
    
    def saveContext(self):
        name = unicode(self.contextLineEdit.text())
        style = self.colorButton.styleSheet()
        iconPath = self.iconPath
        
        if self.editAble:
            self.context.name = name
            self.context.color = style
            self.context.icon = iconPath
            
            buffer.createContext(self.app, self.context, True)
            
            self.mainWidget.statusBar.showMessage("Context updated",2000)
            
            self.cancel() #not cancel but I use function in method
        else:
            context = Context(None, name, style, iconPath, self.app.cursor)
            
            buffer.createContext(self.app, context)
            
            self.mainWidget.statusBar.showMessage("Context created",2000)
            
            self.setDefault()
        
    def setDefault(self):
        self.contextLineEdit.setText("My context")
        self.colorButton.setStyleSheet("* { background-color: #DEDFEF; color: #5A6984 }")
        self.iconButton.setIcon(QtGui.QIcon())
        self.iconButton.setText("No icon")
        self.iconPath = None
            
    def showPallete(self):
        self.parent().setCurrentIndex(self.parent().currentIndex() + 1)
            
    def showIcons(self):
        self.parent().setCurrentIndex(self.parent().currentIndex() + 2)
        
    def colorChoose(self, color):
        self.colorButton.setStyleSheet(color)
        self.parent().setCurrentIndex(self.parent().currentIndex() - 1)
        
    def iconChoose(self, icon):
        self.iconButton.setIcon(QtGui.QIcon(icon))
        self.iconPath = str(icon)
        self.parent().setCurrentIndex(self.parent().currentIndex() - 2)
            
    def setNoIcon(self):
        self.iconButton.setIcon(QtGui.QIcon())
        self.iconButton.setText("No icon")
        self.iconPath = None
        self.parent().setCurrentIndex(self.parent().currentIndex() - 2)
        
class RepositoryForm(QtGui.QWidget):
    
    def __init__(self, parrent, app, mainWidget, repo):
        QtGui.QWidget.__init__(self)
        self.repo = repo
        self.app = app
        self.mainWidget = mainWidget
        
        repLayout=QtGui.QHBoxLayout(self)
        repWidget=QtGui.QWidget(self)
        
        self.contentLayout=QtGui.QGridLayout(repWidget)
        
        self.contentLayout.addWidget(QtGui.QLabel("Name"), 0, 0)
        
        self.repLineEdit = MyLineEdit("My_repository")
        self.contentLayout.addWidget(self.repLineEdit, 0, 1)
        
        self.contentLayout.addWidget(QtGui.QLabel("URI"), 1, 0)
        
        self.uriLineEdit = MyLineEdit("/home/")
        self.contentLayout.addWidget(self.uriLineEdit, 1, 1)
        
        cancelButton=QtGui.QPushButton("Back")
        self.contentLayout.addWidget(cancelButton, 2, 0, QtCore.Qt.AlignBottom)
        
        saveButton=QtGui.QPushButton("Create")
        saveButton.setMaximumSize(QtCore.QSize(80, 30))
        self.contentLayout.addWidget(saveButton, 2, 1, QtCore.Qt.AlignBottom)
        
        repLayout.addWidget(repWidget, 1)
        repLayout.addWidget(QtGui.QWidget(self), 1)
        
        self.connect(cancelButton, QtCore.SIGNAL("clicked()"), self.cancel)
        self.connect(saveButton, QtCore.SIGNAL("clicked()"), self.create)
        
    def cancel(self):
        self.parent().setCurrentIndex(self.parent().currentIndex() - 1)
        self.setDefault()
        
    def create(self):
        name = str(self.repLineEdit.text())
        uri = str(self.uriLineEdit.text())
        if len(name) == 0:
            self.mainWidget.statusBar.showMessage("Repository should have a name",2000)
        elif ' ' in name or ' ' in uri:
            self.mainWidget.statusBar.showMessage("Spaces in the name are not allowed",2000)
        elif len(uri) == 0:
            self.mainWidget.statusBar.showMessage("Not a valid URI",2000)
        else:
            try:
                self.repo.git.execute(["git", "remote", "add", name, uri])
            except git.errors.GitCommandError:
                self.mainWidget.statusBar.showMessage("Remote repository with that name exists",2000)
                return
            try:
                self.mainWidget.statusBar.showMessage("Trying to fetch from remote repository. This may take a while" +
                                                      " depends on size of transfering data.",4000)
                self.repo.git.execute(["git", "fetch", name])
                self.app.syncTab.refresh_sync()
                self.mainWidget.statusBar.showMessage("Remote repository created",2000)
                self.setDefault()
            except git.errors.GitCommandError:
                self.repo.git.execute(["git", "remote", "rm", name])
                QtGui.QMessageBox.warning(self, "An error occurred", "Upps\n" +
                                          "Is entered URI valid? Do you have permission to access" +
                                          " that URI?")
        
    def setDefault(self):
        self.repLineEdit.setText("My_repository")
        self.uriLineEdit.setText("/home/")
        
class MyLineEdit(QtGui.QLineEdit):
    def __init__(self, string, parent=None):
        QtGui.QLineEdit.__init__(self, string)
        
    def mousePressEvent(self, event):
        QtGui.QLineEdit.mousePressEvent(self, event)
        self.selectAll()
