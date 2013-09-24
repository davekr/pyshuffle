from PyQt4 import QtCore, QtGui

from app.dbmanager import DBManager
from app.tabs import Inbox

class Next(Inbox):

    ICON = "next"
    LABEL = "Next actions"

    def refresh_next(self):
        self.nextList.clear()
        for project in DBManager.get_projects().values():
            if len(project.actions) > 0:
                earliest = QtCore.QDate().fromString('2999.12.31','yyyy.MM.dd')
                eAction = None
                for action in project.actions.values():
                    if not action.completed and action.sched.isValid() and earliest > action.sched:
                            earliest = action.sched
                            eAction = action
                if eAction:            
                    listItem = QtGui.QListWidgetItem(eAction.desc)
                    listItem.setData(QtCore.Qt.UserRole, QtCore.QVariant(eAction))
                    self.nextList.addItem(listItem)
        self.edit.refreshAction()
