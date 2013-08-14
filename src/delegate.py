from PyQt4 import QtCore, QtGui

'''
class MyListDelegate(QtGui.QStyledItemDelegate):
    def __init__(self, parent, *args):
        QtGui.QStyledItemDelegate.__init__(self, parent, *args)

    def sizeHint(self, option, index):
        return QtCore.QSize(100,40)

    def paint(self, painter, option, index):
        if(option.state & QtGui.QStyle.State_Selected):
            painter.fillRect(option.rect, option.palette.highlight())

        coords = option.rect.getRect()
        painter.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))
        painter.drawText(option.rect,QtCore.Qt.AlignLeft, 
                         index.model().data(index,QtCore.Qt.DisplayRole).toString())
        painter.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Normal))
        painter.drawText(QtCore.QPoint(0, 34+coords[1]), "Description")
        icon = QtGui.QPixmap("../../img/context/go_home_small.png")
        painter.setRenderHint(QtGui.QPainter().SmoothPixmapTransform)
        
        string = "Project"
        painter.drawText(QtCore.QPoint(coords[2]-200, 18+coords[1]), string)
        context = QtCore.QRectF(coords[2]-202, 22+coords[1], 190, 15)
        painter.setBrush(QtGui.QColor(255, 0, 0, 255))
        pen = QtGui.QPen(QtCore.Qt.white, 1, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        painter.drawRect(context)
        painter.drawText(context, QtCore.Qt.AlignLeft, "    Context")
        painter.setPen(QtGui.QPen())
        painter.setBrush(QtGui.QBrush())
        painter.drawPixmap(context, icon, QtCore.QRectF(-3.0, -1.0, 250.0, 20.0))
'''
        
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
            painter.drawText(QtCore.QPoint(coords[2]-80, 50+coords[1]), item.sched.toString('yyyy-MM-dd'))
        
