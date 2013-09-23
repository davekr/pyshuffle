# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from app.static import contexticons, styles
from app.models import Context
import app.buffer as buffer
from app.utils import SelectAllLineEdit

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
        
        self.contextLineEdit = SelectAllLineEdit("My context")
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
        for (counter, i) in enumerate(contexticons):
            button = QtGui.QToolButton()
            button.setIcon(QtGui.QIcon(contexticons[i]))
            button.setIconSize(QtCore.QSize(30,30))
            app.connect(button, QtCore.SIGNAL("clicked()"), iconMapper, QtCore.SLOT("map()"))
            iconMapper.setMapping(button, contexticons[i])
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
