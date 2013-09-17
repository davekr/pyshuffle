from PyQt4 import QtCore, QtGui

from app.forms import ActionForm, ProjectForm, ContextForm

class New(object):

    def setup_new(self, app, mainWidget):
        
        newWidget=QtGui.QWidget(mainWidget.tab)
        newLayout=QtGui.QVBoxLayout(newWidget)

        selectWidget=QtGui.QWidget(newWidget)
        selectLayout=QtGui.QHBoxLayout(selectWidget)
        selectLabel=QtGui.QLabel("Choose item to create: ",selectWidget)
        pageComboBox = QtGui.QComboBox(selectWidget)
        pageComboBox.addItem("New action")
        pageComboBox.addItem("New project")
        pageComboBox.addItem("New context")
        selectLayout.addWidget(selectLabel, 0, QtCore.Qt.AlignRight)
        selectLayout.addWidget(pageComboBox, 0, QtCore.Qt.AlignLeft)
        selectLayout.addWidget(QtGui.QWidget(), 1)

        stack=QtGui.QStackedWidget(newWidget)
        
        self.action = ActionForm(stack, app, mainWidget)
        stack.addWidget(self.action)
        self.project = ProjectForm(stack, app, mainWidget)
        stack.addWidget(self.project)
        context = ContextForm(stack, app, mainWidget)
        stack.addWidget(context)
        stack.addWidget(context.chooseColor)
        stack.addWidget(context.chooseIcon)
        
        newLayout.addWidget(selectWidget, 0)
        newLayout.addWidget(QtGui.QLabel("<hr />"), 0)
        newLayout.addWidget(stack, 1)
        
        app.connect(pageComboBox, QtCore.SIGNAL("activated(int)"),stack, 
                    QtCore.SLOT("setCurrentIndex(int)"))
        
        return newWidget
    
    def refresh_new(self):
        self.action.refreshAction()
        self.project.refreshProject()
            
