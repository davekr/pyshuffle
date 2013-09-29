# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from app.static import contexticons, styles
from app.models import Context
from app.dbmanager import DBManager
from app.utils import SelectAllLineEdit

class ContextForm(QtGui.QStackedWidget):
    
    def __init__(self, edit=False):
        QtGui.QStackedWidget.__init__(self)
        self.editable = edit
        form = self._setup_form()
        colors = self._setup_color_stack()
        icons = self._setup_icon_stack()
        self.addWidget(form)
        self.addWidget(colors)
        self.addWidget(icons)

    def _setup_form(self):
        content = self._setup_content()
        layout = QtGui.QHBoxLayout()
        layout.addWidget(content, 1)
        layout.addWidget(QtGui.QWidget(self), 1)
        widget = QtGui.QWidget()
        widget.setLayout(layout)
        return widget
        
    def _setup_content(self):
        layout = QtGui.QGridLayout()
        self._setup_name(layout)
        self._setup_color(layout)
        self._setup_icon(layout)
        self._setup_buttons(layout)
        widget = QtGui.QWidget()
        widget.setLayout(layout)
        return widget

    def _setup_name(self, layout):
        layout.addWidget(QtGui.QLabel("Name"), 0, 0)
        layout.addWidget(SelectAllLineEdit("My context"), 0, 1)
        
    def _setup_color(self, layout):
        color = QtGui.QToolButton()
        color.setText("Abc")
        color.setStyleSheet("* { background-color: #DEDFEF; color: #5A6984 }")
        self.connect(color, QtCore.SIGNAL("clicked()"), self.show_pallete)
        layout.addWidget(QtGui.QLabel("Color"), 1, 0)
        layout.addWidget(color, 1, 1)
        self._color_button = color

    def _setup_icon(self, layout):
        icon = QtGui.QToolButton()
        icon.setText("No icon")
        icon.setIconSize(QtCore.QSize(30,30))
        self.connect(icon, QtCore.SIGNAL("clicked()"), self.show_icons)
        layout.addWidget(QtGui.QLabel("Icon"), 2, 0)
        layout.addWidget(icon, 2, 1)
        self._icon_button = icon

    def _setup_buttons(self, layout):
        save = QtGui.QPushButton("Save")
        self.connect(save, QtCore.SIGNAL("clicked()"), self.save_context)
        if self.editable:
            cancel = QtGui.QPushButton("Back")
            layout.addWidget(cancel, 3, 0, QtCore.Qt.AlignBottom)
            self.connect(cancel, QtCore.SIGNAL("clicked()"), self.cancel)
            save.setMaximumSize(QtCore.QSize(80, 30))
            layout.addWidget(save, 3, 1, QtCore.Qt.AlignBottom)
        else:
            layout.addWidget(save, 3, 0, QtCore.Qt.AlignBottom)

    def _setup_color_stack(self):
        layout = QtGui.QGridLayout()
        color_mapper = QtCore.QSignalMapper(self.window())
        self.connect(color_mapper, QtCore.SIGNAL("mapped(const QString &)"), self.choose_color)
        for counter, style in enumerate(styles):
            button = QtGui.QToolButton()
            button.setText("Abc")
            button.setStyleSheet(styles[style])
            self.connect(button, QtCore.SIGNAL("clicked()"), color_mapper, QtCore.SLOT("map()"))
            color_mapper.setMapping(button, styles[style])
            layout.addWidget(button, counter / 6, counter % 6)
        widget = QtGui.QWidget()
        widget.setLayout(layout)
        return widget
        
    def _setup_icon_stack(self):
        layout = QtGui.QGridLayout()
        icon_mapper = QtCore.QSignalMapper(self.window())
        self.connect(icon_mapper, QtCore.SIGNAL("mapped(const QString &)"), self.choose_icon)
        for counter, icon in enumerate(contexticons):
            button = QtGui.QToolButton()
            button.setIcon(QtGui.QIcon(contexticons[icon]))
            button.setIconSize(QtCore.QSize(30,30))
            button.setProperty('icon_name', icon)
            self.connect(button, QtCore.SIGNAL("clicked()"), icon_mapper, QtCore.SLOT("map()"))
            icon_mapper.setMapping(button, icon)
            layout.addWidget(button, counter / 6, counter % 6, QtCore.Qt.AlignCenter)
        no_icon = QtGui.QToolButton()
        no_icon.setText("No icon")
        self.connect(no_icon, QtCore.SIGNAL("clicked()"), self.set_no_icon)
        layout.addWidget(no_icon, 4, 1, QtCore.Qt.AlignCenter)
        widget = QtGui.QWidget()
        widget.setLayout(layout)
        return widget

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
    
    def save_context(self):
        print self._icon_button.property('icon_name').toPyObject()
        name = unicode(self.contextLineEdit.text())
        style = self.colorButton.styleSheet()
        iconPath = self.iconPath
        
        if self.editAble:
            self.context.name = name
            self.context.color = style
            self.context.icon = iconPath
            
            DBManager.create_context(self.context)
            
            self.window().show_status("Context updated")
            
            self.cancel() #not cancel but I use function in method
        else:
            context = Context(None, name, style, iconPath)
            
            DBManager.create_context(context)
            
            self.window().show_status("Context created")
            
            self.setDefault()
        
    def setDefault(self):
        self.contextLineEdit.setText("My context")
        self.colorButton.setStyleSheet("* { background-color: #DEDFEF; color: #5A6984 }")
        self.iconButton.setIcon(QtGui.QIcon())
        self.iconButton.setText("No icon")
        self.iconPath = None
            
    def show_pallete(self):
        self.setCurrentIndex(self.currentIndex() + 1)
            
    def show_icons(self):
        self.setCurrentIndex(self.currentIndex() + 2)
        
    def choose_color(self, color):
        self._color_button.setStyleSheet(color)
        self.setCurrentIndex(self.currentIndex() - 1)
        
    def choose_icon(self, icon):
        self._icon_button.setIcon(QtGui.QIcon(contexticons[str(icon)]))
        self._icon_button.setProperty('icon_name', icon)
        self.setCurrentIndex(self.currentIndex() - 2)
            
    def set_no_icon(self):
        self._icon_button.setIcon(QtGui.QIcon())
        self._icon_button.setText("No icon")
        self._icon_button.setProperty('icon_name', None)
        self.setCurrentIndex(self.currentIndex() - 2)
