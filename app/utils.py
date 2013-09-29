# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from datetime import datetime
import time

from settings import DATE_FORMAT, DATETIME_FORMAT

#from settings import DATABASE
#from git import Repo

class Event(QtCore.QObject):

    action_change = QtCore.pyqtSignal()
    project_change = QtCore.pyqtSignal()
    context_change = QtCore.pyqtSignal()

event_register = Event()

class SelectAllLineEdit(QtGui.QLineEdit):
        
    def mousePressEvent(self, event):
        QtGui.QLineEdit.mousePressEvent(self, event)
        self.selectAll()

class SelectAllTextEdit(QtGui.QTextEdit):

    def mousePressEvent(self, event):
        QtGui.QTextEdit.mousePressEvent(self, event)
        self.selectAll()

class ListItemDelegate(QtGui.QStyledItemDelegate):

    def __init__(self, parent, *args):
        QtGui.QStyledItemDelegate.__init__(self, parent, *args)

    def sizeHint(self, option, index):
        return QtCore.QSize(100,55)

    def paint(self, painter, option, index):
        if(option.state & QtGui.QStyle.State_Selected):
            painter.fillRect(option.rect, option.palette.highlight())

        coords = option.rect.getRect()
        item = index.model().data(index,QtCore.Qt.UserRole).toPyObject()
        painter.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))
        painter.drawText(option.rect,QtCore.Qt.AlignLeft, 
                         index.model().data(index,QtCore.Qt.DisplayRole).toString())
        if item.project:
            painter.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
            painter.drawText(QtCore.QPoint(0, 34+coords[1]), item.project.name)
        
        if item.context:
            context = QtCore.QRectF(coords[2]-202, 2+coords[1], 190, 35)
            painter.setRenderHint(QtGui.QPainter().SmoothPixmapTransform)
            painter.setBrush(QtGui.QColor(item.context.color[22:29]))
            pen = QtGui.QPen(QtGui.QColor(item.context.color[38:45]), 1, QtCore.Qt.SolidLine)
            painter.setPen(pen)
            painter.drawRoundedRect(context,12,9)
            
            if item.context.icon:
                icon = QtGui.QPixmap(item.context.icon)
                painter.drawPixmap(context, icon, QtCore.QRectF(-3.0, -1.0, 190.0, 33.0))
                
            painter.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
            painter.drawText(context, QtCore.Qt.AlignVCenter, "         " + item.context.name)
            painter.setPen(QtGui.QPen())
            painter.setBrush(QtGui.QBrush())
            
        painter.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Normal))
        if item.details:
            painter.drawText(QtCore.QPoint(0, 50+coords[1]), item.details)
        if item.sched:
            painter.drawText(QtCore.QPoint(coords[2]-80, 50+coords[1]), item.sched.toString(DATE_FORMAT))

def commit(app, message):
    pass
    #repo = Repo(DATABASE)
    #repo.git.execute(["git", "add", "shuffle.db"])
    #repo.git.execute(["git","commit","-m", message])

def convert_to_date(timestamp):
    qdate = QtCore.QDate()
    if timestamp:
        date = datetime.fromtimestamp(timestamp).date()
        qdate = qdate.fromString(date.strftime(DATETIME_FORMAT), DATE_FORMAT)
    return qdate

def convert_from_date(date):
    timestamp = None
    if date:
        date_string = str(date.toString(DATE_FORMAT))
        timestamp = time.mktime(datetime.strptime(date_string, DATETIME_FORMAT).timetuple())
    return timestamp

