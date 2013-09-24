from PyQt4 import QtCore, QtGui

from app.forms import ActionForm, ProjectForm, ContextForm
from app.tabs.tab import Tab

class New(Tab):

    ICON = "new"
    LABEL = "New"
        
    def _setup_content(self):
        selection = self._setup_selection()
        forms = self._setup_forms()
        layout = QtGui.QVBoxLayout()
        layout.addWidget(selection, 0)
        layout.addWidget(QtGui.QLabel("<hr />"), 0)
        layout.addWidget(forms, 1)
        self.setLayout(layout)

    def _setup_selection(self):
        select_layout = QtGui.QHBoxLayout()
        select_layout.addWidget(QtGui.QLabel("Choose item to create: "), 0, \
                               QtCore.Qt.AlignRight)
        combobox = self._setup_combobox()
        select_layout.addWidget(combobox, 0, QtCore.Qt.AlignLeft)
        select_layout.addWidget(QtGui.QWidget(), 1)
        select_widget = QtGui.QWidget()
        select_widget.setLayout(select_layout)
        return select_widget 

    def _setup_combobox(self):
        combobox = QtGui.QComboBox()
        combobox.addItem("New action")
        combobox.addItem("New project")
        combobox.addItem("New context")
        self._combobox = combobox
        return combobox

    def _setup_forms(self):
        stack = QtGui.QStackedWidget()
        stack.addWidget(ActionForm())
        stack.addWidget(ProjectForm())
        context = ContextForm()
        stack.addWidget(context)
        stack.addWidget(context.chooseColor)
        stack.addWidget(context.chooseIcon)
        self._stack = stack
        return stack

    def _connect_events(self):
        self.connect(self._combobox, QtCore.SIGNAL("activated(int)"), self._stack, \
                     QtCore.SLOT("setCurrentIndex(int)"))
            
