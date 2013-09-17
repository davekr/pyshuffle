from PyQt4 import QtCore, QtGui
import sqlite3
from datetime import datetime
import time
import os

from models import Action, Project, Context
import static
from utils import commit
import settings

class Buffer(object):

    _ALL_CONTEXTS = 'SELECT _id, name, colour, iconName FROM context'
    _ALL_PROJECTS = 'SELECT _id, name, defaultContextId FROM project'
    _ALL_ACTIONS = 'SELECT _id, description, projectId, contextId, details, ' +\
            'start, complete FROM task ORDER BY start desc'
    _INSERT_ACTION = 'Insert into task (_id, description, projectId, contextId, ' +\
            ' start, details, complete) values(?,?,?,?,?,?,?)'
    _UPDATE_ACTION = 'UPDATE task SET description=?, projectId=?, contextId=?, ' +\
            'details=?, start=?, complete=? WHERE _id=?'
    _DELETE_ACTION = 'DELETE From task WHERE _id=?'
    _COMPLETE_ACTION = 'UPDATE task SET complete=? WHERE _id=?'

    def __init__(self):
        self._actions = {}
        self._projects = {}
        self._contexts = {}
        self.temp_action = {}
        self.temp_project = {}
        self.temp_context = {}

    @property
    def conn(self):
        if getattr(self, '_conn', None) is None:
            print 'initializing connection'
            self._conn = sqlite3.connect(settings.DATABASE)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def execute_and_fetch(self, query):
        try:
            self._execute(query)
            data = self._cursor.fetchall()
        finally:
            self._done()
        return data
    
    def execute(self, query, args):
        try:
            self._execute(query, args)
        finally:
            self._done()
        
    def _execute(self, query, *args):
        self._cursor = self.conn.cursor()
        self._cursor.execute(query, *args)
        
    def _done(self):
        self._cursor.close()
        self.conn.commit()

    def init_db(self):
        if not os.path.exists(settings.DATABASE):
            self.setup_demo()

    def setup_demo(self):
        with open(os.path.join(settings.DB_PATH, 'demo.sql')) as sql:
            self.conn.executescript(sql.read())

    def init_buffer(self):
        self._init_contexts()
        self._init_projects()
        self._init_actions()

    def _init_contexts(self):
        contexts = self.execute_and_fetch(self._ALL_CONTEXTS)
        for row in contexts:
            style = static.styles.get(row['colour'])
            icon = static.contexticons.get(row['iconName'])
            context = Context(row['_id'], row['name'], style, icon)
            self._buffer_context(context)

    def _init_projects(self):
        projects = self.execute_and_fetch(self._ALL_PROJECTS)
        for row in projects:
            context = self._contexts.get(row['defaultContextId'])
            project = Project(row['_id'], row['name'], context)
            self._buffer_project(project)

    def _init_actions(self):
        actions = self.execute_and_fetch(self._ALL_ACTIONS)
        for row in actions:
            project = self._projects.get(row['projectId'])
            context = self._contexts.get(row['contextId'])
            date = self.convert_to_date(row['start'])
            action = Action(row['_id'], row['description'], project, context, \
                            date, row['details'], row['complete'])
            self._buffer_action(action)

    def convert_to_date(self, timestamp):
        qdate = QtCore.QDate()
        if timestamp:
            date = datetime.fromtimestamp(timestamp).date()
            qdate = qdate.fromString(str(date), 'yyyy-MM-dd')
        return qdate

    def convert_from_date(self, date):
        timestamp = None
        if date:
            date_string = str(date.sched.toString('yyyy-MM-dd'))
            timestamp = time.mktime(datetime.strptime(date_string, "%Y-%m-%d").timetuple())
        return timestamp

    def _buffer_context(self, context):
        self._add_buffer(self._contexts, context)

    def _buffer_project(self, project):
        self._add_buffer(self._projects, project)

    def _buffer_action(self, action):
        self._add_buffer(self._actions, action)

    def _add_buffer(self, buffer, item):
        buffer[item.id] = item

    def get_actions(self):
        return self._actions

    def createAction(self, app, item):
        if app.inSync:
            QtGui.QMessageBox.information(QtGui.QWidget(), "Abort", "You are in the middle of "
                                          + "a conflicted merge. Please resolve it first.")
            return
        
        self._buffer_action(item)
        
        project = None
        context = None
        
        if item.context:
            item.context.addAction(item)
            context = item.context.id
            app.contextTab.refresh_contexts()
        if item.project:
            item.project.addAction(item)
            project = item.project.id
            app.projectTab.refresh_projects()

        date = self.convert_from_date(item.sched)

        app.calendarTab.refresh_calendar()
        app.inboxTab.refresh_inbox()
        app.nextTab.refresh_next()
            
        self.execute(self._INSERT_ACTION, [item.id, item.desc, project, context,\
                                           date, item.details, item.completed])
        commit(app, "'create action'")
        
    def updateAction(self, app, item, projId, ctxId):
        if app.inSync:
            QtGui.QMessageBox.information(QtGui.QWidget(), "Abort", "You are in the middle of "
                                          + "a conflicted merge. Please resolve it first.")
            return
        
        self._buffer_action(item)
        
        if projId:
            self._projects[projId].removeAction(item)
            
        if ctxId:
            self._contexts[ctxId].removeAction(item)
        
        project = None
        context = None
        
        if item.context:
            item.context.addAction(item)
            context = item.context.id
        if item.project:
            item.project.addAction(item)
            project = item.project.id
        date = self.convert_from_date(item.sched)
            
        app.inboxTab.refresh_inbox()
        app.nextTab.refresh_next()
        app.calendarTab.refresh_calendar()
        app.projectTab.refresh_projects()
        app.contextTab.refresh_contexts()
        
        self.execute(self._UPDATE_ACTION, [item.desc, project, context, item.details,\
                                           date, item.completed, item.id])
        commit(app, "'update action'")
        
    def deleteAction(self, app, item):
        if app.inSync:
            QtGui.QMessageBox.information(QtGui.QWidget(), "Abort", "You are in the middle of "
                                          + "a conflicted merge. Please resolve it first.")
            return
        
        if item.project:
            del item.project.actions[item.id]
        if item.context:
            del item.context.actions[item.id]
            
        del self._actions[item.id]
        
        app.inboxTab.refresh_inbox()
        app.nextTab.refresh_next()
        app.calendarTab.refresh_calendar()
        app.projectTab.refresh_projects()
        app.contextTab.refresh_contexts()
        app.completeTab.refresh_complete()
        
        self.execute(self._DELETE_ACTION, (item.id,))
        
        commit(app, "'delete action'")
        
    def completeAction(self, app, item, restore=False):
        if app.inSync:
            QtGui.QMessageBox.information(QtGui.QWidget(), "Abort", "You are in the middle of "
                                          + "a conflicted merge. Please resolve it first.")
            return
        
        if restore:
            item.completed = 0
        else:
            item.completed = 1
        self._buffer_action(item)
        
        app.completeTab.refresh_complete()
        app.inboxTab.refresh_inbox()
        app.nextTab.refresh_next()
        app.calendarTab.refresh_calendar()
        app.projectTab.refresh_projects()
        app.contextTab.refresh_contexts()
        
        self.execute(self._COMPLETE_ACTION, [item.completed, item.id])
        commit(app, "'complete action'")
        
    def createProject(self, app, item, update=False):
        if app.inSync:
            QtGui.QMessageBox.information(QtGui.QWidget(), "Abort", "You are in the middle of "
                                          + "a conflicted merge. Please resolve it first.")
            return
        
        self._buffer_project(item)
        
        context = None
        if item.context:
            context = item.context.id
            
        if update:
            for key in item.actions:
                item.actions[key].project = item
            
        app.newTab.refresh_new()
        app.inboxTab.refresh_inbox()
        app.nextTab.refresh_next()
        app.calendarTab.refresh_calendar()
        app.projectTab.refresh_projects()
        app.contextTab.refresh_contexts()
        
        if update:
            app.cursor.execute('UPDATE project SET name=?, defaultContextId=? WHERE _id=?', 
                                   [item.name, context, item.id])
        else:
            app.cursor.execute('Insert into project (_id, name, defaultContextId )' +
                                   'values(?,?,?)', [item.id, item.name, context])
        commit(app, "'create/update project'")
        
    def deleteProject(self, app, item):
        if app.inSync:
            QtGui.QMessageBox.information(QtGui.QWidget(), "Abort", "You are in the middle of "
                                          + "a conflicted merge. Please resolve it first.")
            return
        
        for action in item.actions.values():
            action.project = None
        app.cursor.execute('DELETE From project WHERE _id=?', (item.id,))
        del self._projects[item.id]
        commit(app, "'delete project")
        
        app.newTab.refresh_new()
        app.inboxTab.refresh_inbox()
        app.nextTab.refresh_next()
        app.calendarTab.refresh_calendar()
        app.projectTab.refresh_projects()
        app.contextTab.refresh_contexts()
        
    def deleteContext(self, app, item):
        if app.inSync:
            QtGui.QMessageBox.information(QtGui.QWidget(), "Abort", "You are in the middle of "
                                          + "a conflicted merge. Please resolve it first.")
            return
        
        for action in item.actions.values():
            action.context = None
            
        for project in self._projects.values():
            if project.context and project.context.id == item.id:
                project.context = None
        
        del self._contexts[item.id]
        app.cursor.execute('DELETE From context WHERE _id=?', (item.id,))
        commit(app, "'delete context")
        
        app.newTab.refresh_new()
        app.inboxTab.refresh_inbox()
        app.nextTab.refresh_next()
        app.calendarTab.refresh_calendar()
        app.projectTab.refresh_projects()
        app.contextTab.refresh_contexts()
        
        
    def createContext(self, app, item, update=False):
        if app.inSync:
            QtGui.QMessageBox.information(QtGui.QWidget(), "Abort", "You are in the middle of "
                                          + "a conflicted merge. Please resolve it first.")
            return
        
        self._buffer_context(item)
        
        color = None
        icon = None
        if item.icon:
            for i in static.contexticons:
                if static.contexticons[i] == item.icon:
                    icon = i
        if item.color:
            for i in static.styles:
                if static.styles[i] == item.color:
                    color = i
            
        if update:
            for key in item.actions:
                item.actions[key].context = item
            # pokud bude updatovani contextu delsi kvuli poctu projektu v aplikaci
            # bude treba vytvorit v modelu Context slovnik obsahujici projekty pro
            # dany context
            for project in self._projects.values():
                if project.context:
                    if project.context.id == item.id:
                        project.context = item
            
        app.newTab.refresh_new()
        app.inboxTab.refresh_inbox()
        app.nextTab.refresh_next()
        app.calendarTab.refresh_calendar()
        app.projectTab.refresh_projects()
        app.contextTab.refresh_contexts()
        
        if update:
            app.cursor.execute('UPDATE context SET name=?, colour=?, iconName=? WHERE _id=?', 
                                   [item.name, color, icon, item.id])
        else:
            app.cursor.execute('Insert into context (_id, name, colour, iconName) values(?,?,?,?)',
                                    [item.id, item.name, color, icon])
        commit(app, "'create/update context'")

