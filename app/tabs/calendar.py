from PyQt4 import QtCore, QtGui
import datetime

from app.utils import ListItemDelegate
from app.forms import ActionForm
from app.dbmanager import DBManager
from app.tabs.tab import Tab

class Calendar(QtGui.QStackedWidget, Tab):

    ICON = "calendar"
    LABEL = "Calendar"

    def _setup_content(self):
        calendar = self._setup_calendar()
        detail = self._setup_detail()
        self.addWidget(calendar)
        self.addWidget(detail)
        self.addWidget(ActionForm(True))

    def _setup_calendar(self):
        calendar = QtGui.QCalendarWidget()
        calendar.setGridVisible(True)
        calendar.setToolTip("Double click on a date to see tasks")
        textFormat = QtGui.QTextCharFormat(calendar.dateTextFormat(datetime.date.today()))
        textFormat.setFontUnderline(True)
        calendar.setDateTextFormat(datetime.date.today(),textFormat)
        self._calendar = calendar
        return calendar

    def _setup_detail(self):
        detail_list = self._setup_list()
        bottom = self._setup_bottom()
        layout = QtGui.QVBoxLayout()
        layout.addWidget(detail_list)
        layout.addWidget(bottom)
        detail = QtGui.QWidget()
        detail.setLayout(layout)
        return detail

    def _setup_list(self):
        detail_list = QtGui.QListWidget()
        detail_list.setItemDelegate(ListItemDelegate(detail_list))
        self._detail_list = detail_list
        return detail_list

    def _setup_bottom(self):
        back, edit, complete, delete = self._setup_buttons()
        layout = QtGui.QHBoxLayout()
        layout.addWidget(back, 0)
        layout.addWidget(edit, 0)
        layout.addWidget(complete, 0)
        layout.addWidget(QtGui.QWidget(), 1)
        layout.addWidget(delete, 0, QtCore.Qt.AlignRight)
        widget = QtGui.QWidget()
        widget.setLayout(layout)
        return widget

    def _setup_buttons(self):
        back = QtGui.QPushButton("Back")
        self.connect(back, QtCore.SIGNAL("clicked()"), self.go_back)
        edit = QtGui.QPushButton("Edit")
        self.connect(edit, QtCore.SIGNAL("clicked()"), self.edit_action)
        complete = QtGui.QPushButton("Complete")
        self.connect(complete, QtCore.SIGNAL("clicked()"), self.complete_action)
        delete = QtGui.QPushButton("Delete")
        self.connect(delete, QtCore.SIGNAL("clicked()"), self.delete_action)
        return back, edit, complete, delete

    def _connect_events(self):
        self.connect(self._calendar, QtCore.SIGNAL("activated( const QDate & )"), self.show_detail)
        self.connect(self._detail_list, QtCore.SIGNAL("itemDoubleClicked (QListWidgetItem *)"), self.edit_action)
        
    def go_back(self):
        self.setCurrentWidget(self._calendar)
        
    def show_detail(self, date):
        #self.refresh_detail(date)
        self.setCurrentIndex(1)
        
    def edit_action(self):
        if len(self.detailList.selectedItems()) > 0:
            self.setCurrentIndex(2)
            self.edit.edit(self.detailList.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject())
        else:
            self.window().show_status("Select item first")
            
    def delete_action(self):
        if len(self.detailList.selectedItems()) > 0:
            DBManager.delete_action(self.detailList.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject())
            self.window().show_status("Action deleted")
        else:
            self.window().show_status("Select item first")
    
    def complete_action(self):
        if len(self.detailList.selectedItems()) > 0:
            DBManager.update_action(self.detailList.selectedItems()[0].data(QtCore.Qt.UserRole).toPyObject())
            self.window().show_status("Action completed")
        else:
            self.window().show_status("Select item first")
    
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


