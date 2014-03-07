from PyQt4 import QtCore, QtGui

from app.dbmanager import DBManager
from app.tabs import Inbox

class Next(Inbox):

    ICON = "next"
    LABEL = "Next actions"

    def _fill_inbox(self):
        self._inbox.clear()
        projects = {project.id: None for project in DBManager.get_projects().values()}
        for action in DBManager.get_actions().values():
            if action.project and not action.completed and action.sched.isValid():
                if len(projects) > action.project.id:
                    if not projects[action.project.id] or projects[action.project.id].sched < action.sched:
                        projects[action.project.id] = action
        for action in projects.values():
            if action:
                item = QtGui.QListWidgetItem(action.desc)
                item.setData(QtCore.Qt.UserRole, QtCore.QVariant(action))
                self._inbox.addItem(item)
