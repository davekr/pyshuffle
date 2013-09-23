from PyQt4 import QtCore, QtGui
import datetime

from app.utils import ListItemDelegate
from app.forms import ActionForm
from app.dbmanager import DBManager

class Calendar(object):
    def setup_calendar(self, app, mainWidget):
        self.app = app
        
        calendarWidget=QtGui.QWidget(mainWidget.tab)
        calendarLayout=QtGui.QGridLayout(calendarWidget)

        stack=QtGui.QStackedWidget(calendarWidget)
        
        self.calendar=QtGui.QCalendarWidget(stack)
        self.calendar.setGridVisible(True)
        self.calendar.setToolTip("Double click on a date to see tasks")
        textFormat = QtGui.QTextCharFormat(self.calendar.dateTextFormat(datetime.date.today()))
        textFormat.setFontUnderline(True)
        self.calendar.setDateTextFormat(datetime.date.today(),textFormat)

        self.detailWidget=QtGui.QWidget(stack)
        detailLayout=QtGui.QVBoxLayout(self.detailWidget)
        
        helpWidget=QtGui.QWidget(self.detailWidget)
        helpLayout=QtGui.QHBoxLayout(helpWidget)
        
        self.detailList=QtGui.QListWidget()
        deleg = ListItemDelegate(self.detailWidget)
        self.detailList.setItemDelegate(deleg)
        detailLayout.addWidget(self.detailList)
        
        backButton=QtGui.QPushButton("Back")
        editButton = QtGui.QPushButton("Edit", helpWidget)
        completeButton = QtGui.QPushButton("Complete", helpWidget)
        deleteButton = QtGui.QPushButton("Delete", helpWidget)
        
        helpLayout.addWidget(backButton, 0)
        helpLayout.addWidget(editButton, 0)
        helpLayout.addWidget(completeButton, 0)
        helpLayout.addWidget(QtGui.QWidget(), 1)
        helpLayout.addWidget(deleteButton, 0, QtCore.Qt.AlignRight)
        detailLayout.addWidget(helpWidget)
        
        stack.addWidget(self.calendar)
        stack.addWidget(self.detailWidget)
        
        self.edit = ActionForm(True)
        stack.addWidget(self.edit)

        calendarLayout.addWidget(stack)
        
        def back():
            stack.setCurrentWidget(self.calendar)
            
        def showDetail(date):
            self.refresh_detail(date)
            stack.setCurrentWidget(self.detailWidget)
            
        def editAction():
            if len(self.detailList.selectedItems()) > 0:
                stack.setCurrentIndex(2)
                self.edit.edit(self.detailList.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject())
            else:
                mainWidget.statusBar.showMessage("Select item first",2000)
                
        def deleteAction():
            if len(self.detailList.selectedItems()) > 0:
                DBManager.deleteAction(app, (self.detailList.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject()))
                mainWidget.statusBar.showMessage("Action deleted",2000)
            else:
                mainWidget.statusBar.showMessage("Select item first",2000)
        
        def completeAction():
            if len(self.detailList.selectedItems()) > 0:
                DBManager.completeAction(app, (self.detailList.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject()))
                mainWidget.statusBar.showMessage("Action completed",2000)
            else:
                mainWidget.statusBar.showMessage("Select item first",2000)
                
        
        app.connect(self.calendar, QtCore.SIGNAL("activated( const QDate & )"), showDetail)
        app.connect(backButton, QtCore.SIGNAL("clicked()"),back)
        app.connect(editButton, QtCore.SIGNAL("clicked()"),editAction)
        app.connect(deleteButton, QtCore.SIGNAL("clicked()"),deleteAction)
        app.connect(completeButton, QtCore.SIGNAL("clicked()"),completeAction)
        app.connect(self.detailList, QtCore.SIGNAL("itemDoubleClicked (QListWidgetItem *)"), editAction)
        
        return calendarWidget
    
    
    def refresh_detail(self, date):
        self.detailList.clear()
        for item in DBManager.get_actions().values():
            if item.sched == date and not item.completed:
                listItem = QtGui.QListWidgetItem(item.desc)
                listItem.setData(QtCore.Qt.UserRole, QtCore.QVariant(item))
                self.detailList.addItem(listItem)

    def refresh_calendar(self):
        brush=QtGui.QBrush(QtGui.QColor("#C8C8C8"))
        for item in DBManager.get_actions().values():
            if item.sched.isValid() and not item.completed:
                textFormat = QtGui.QTextCharFormat(self.calendar.dateTextFormat(item.sched))
                textFormat.setBackground(brush)
                self.calendar.setDateTextFormat(item.sched,textFormat)
                self.refresh_detail(item.sched)
        self.edit.refreshAction()


