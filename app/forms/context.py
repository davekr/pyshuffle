# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from app.static import contexticons, styles, get_style
from app.models import Context
from app.utils import SelectAllLineEdit, event_register

class ContextForm(QtGui.QStackedWidget):
    
    def __init__(self, editmode = False):
        QtGui.QStackedWidget.__init__(self)
        self.editmode = editmode
        self._context = Context()
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
        name = SelectAllLineEdit("My context")
        layout.addWidget(QtGui.QLabel("Name"), 0, 0)
        layout.addWidget(name, 0, 1)
        self._name = name
        return name
        
    def _setup_color(self, layout):
        color = QtGui.QToolButton()
        color.setText("Abc")
        color.setStyleSheet(get_style(1))
        color.setProperty('color_id', 1)
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
        if self.editmode:
            cancel = QtGui.QPushButton("Back")
            layout.addWidget(cancel, 3, 0, QtCore.Qt.AlignBottom)
            self.connect(cancel, QtCore.SIGNAL("clicked()"), self.hide_form)
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
            button.setStyleSheet(get_style(style))
            button.setProperty('color_id', style)
            self.connect(button, QtCore.SIGNAL("clicked()"), color_mapper, QtCore.SLOT("map()"))
            color_mapper.setMapping(button, str(style))
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

    def set_context(self, context):
        self._context = context
        self._name.setText(context.name)
        self._color_button.setStyleSheet(get_style(context.color))
        self._color_button.setProperty('color_id', context.color)
        self._icon_button.setIcon(QtGui.QIcon(contexticons[context.icon]))
        self._icon_button.setProperty('icon_name', context.icon)
        
    def hide_form(self):
        self.parent().setCurrentIndex(self.parent().currentIndex() - 2)
        self.set_default()
    
    def save_context(self):
        context = self.get_context()
        if self.editmode:
            self.window().show_status("Context updated")
            self.hide_form()
        else:
            self.window().show_status("Context created")
            self.set_default()
        context.save()
        event_register.context_change.emit()
        self._context = Context()

    def get_context(self):
        context = self._context
        context.name = unicode(self._name.text())
        context.color = self._color_button.property('color_id').toPyObject()
        context.icon = str(self._icon_button.property('icon_name').toPyObject())
        return context
        
    def set_default(self):
        self._name.setText("My context")
        self._color_button.setStyleSheet(get_style(1))
        self._icon_button.setProperty('color_id', 1)
        self._icon_button.setIcon(QtGui.QIcon())
        self._icon_button.setText("No icon")
        self._icon_button.setProperty('icon_name', None)
            
    def show_pallete(self):
        self.setCurrentIndex(self.currentIndex() + 1)
            
    def show_icons(self):
        self.setCurrentIndex(self.currentIndex() + 2)
        
    def choose_color(self, color):
        self._color_button.setStyleSheet(get_style(int(color)))
        self._color_button.setProperty('color_id', int(color))
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
