
from PyQt4 import QtGui
import sqlite3
import os

from app import static
from app.utils import commit, convert_from_date
from app.buffer import Buffer
import settings

class DBManager(object):

    ALL_CONTEXTS = 'SELECT _id, name, colour, iconName FROM context'
    ALL_PROJECTS = 'SELECT _id, name, defaultContextId FROM project'
    ALL_ACTIONS = 'SELECT _id, description, projectId, contextId, details, ' +\
            'start, complete FROM task ORDER BY start desc'
    INSERT_ACTION = 'Insert into task (_id, description, projectId, contextId, ' +\
            ' start, details, complete) values(?,?,?,?,?,?,?)'
    UPDATE_ACTION = 'UPDATE task SET description=?, projectId=?, contextId=?, ' +\
            'details=?, start=?, complete=? WHERE _id=?'
    DELETE_ACTION = 'DELETE From task WHERE _id=?'
    COMPLETE_ACTION = 'UPDATE task SET complete=? WHERE _id=?'
    INSERT_PROJECT = 'Insert into project (_id, name, defaultContextId) values(?,?,?)'
    UPDATE_PROJECT = 'UPDATE project SET name=?, defaultContextId=? WHERE _id=?'
    DELETE_PROJECT = 'DELETE From project WHERE _id=?'
    INSERT_CONTEXT = 'DELETE From context WHERE _id=?'
    UPDATE_CONTEXT = 'UPDATE context SET name=?, colour=?, iconName=? WHERE _id=?'
    DELETE_CONTEXT = 'Insert into context (_id, name, colour, iconName) values(?,?,?,?)'

    @classmethod
    def init_dbmanager(cls):
        cls.init_conn()
        cls.init_db()
        cls.init_buffer()

    @classmethod
    def init_conn(cls):
        if getattr(cls, '_conn', None) is None:
            print 'initializing connection'
            cls._conn = sqlite3.connect(settings.DATABASE)
            cls._conn.row_factory = sqlite3.Row
        return cls._conn

    @classmethod
    def init_db(cls):
        if not os.path.exists(settings.DATABASE):
            cls.setup_demo()

    @classmethod
    def setup_demo(cls):
        with open(os.path.join(settings.DB_PATH, 'demo.sql')) as sql:
            cls._conn.executescript(sql.read())

    @classmethod
    def init_buffer(cls):
        cls._buffer = Buffer()
        contexts = cls.execute_and_fetch(DBManager.ALL_CONTEXTS)
        projects = cls.execute_and_fetch(DBManager.ALL_PROJECTS)
        actions = cls.execute_and_fetch(DBManager.ALL_ACTIONS)
        cls._buffer.init_buffers(contexts, projects, actions)

    @classmethod
    def execute_and_fetch(cls, query):
        try:
            cls._execute(query)
            data = cls._cursor.fetchall()
        finally:
            cls._done()
        return data
    
    @classmethod
    def execute(cls, query, args):
        try:
            cls._execute(query, args)
        finally:
            cls._done()
        
    @classmethod
    def _execute(cls, query, *args):
        cls._cursor = cls._conn.cursor()
        cls._cursor.execute(query, *args)
        
    @classmethod
    def _done(cls):
        cls._cursor.close()
        cls._conn.commit()

    @classmethod
    def get_projects(cls):
        return cls._buffer.get_projects()

    @classmethod
    def get_contexts(cls):
        return cls._buffer.get_contexts()

    @classmethod
    def get_actions(cls):
        return cls._buffer.get_actions()

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

        date = convert_from_date(item.sched)

        app.calendarTab.refresh_calendar()
        app.inboxTab.refresh_inbox()
        app.nextTab.refresh_next()
            
        self.execute(self.INSERT_ACTION, [item.id, item.desc, project, context,\
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
        date = convert_from_date(item.sched)
            
        app.inboxTab.refresh_inbox()
        app.nextTab.refresh_next()
        app.calendarTab.refresh_calendar()
        app.projectTab.refresh_projects()
        app.contextTab.refresh_contexts()
        
        self.execute(self.UPDATE_ACTION, [item.desc, project, context, item.details,\
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
        
        self.execute(self.DELETE_ACTION, (item.id,))
        
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
        
        self.execute(self.COMPLETE_ACTION, [item.completed, item.id])
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
            app.cursor.execute(self.UPDATE_PROJECT, [item.name, context, item.id])
        else:
            app.cursor.execute(self.INSERT_PROJECT, [item.id, item.name, context])
        commit(app, "'create/update project'")
        
    def deleteProject(self, app, item):
        if app.inSync:
            QtGui.QMessageBox.information(QtGui.QWidget(), "Abort", "You are in the middle of "
                                          + "a conflicted merge. Please resolve it first.")
            return
        
        for action in item.actions.values():
            action.project = None
        app.cursor.execute(self.DELETE_PROJECT, (item.id,))
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
        app.cursor.execute(self.DELETE_CONTEXT, (item.id,))
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
            app.cursor.execute(self.UPDATE_CONTEXT, [item.name, color, icon, item.id])
        else:
            app.cursor.execute(self.INSERT_CONTEXT, [item.id, item.name, color, icon])
        commit(app, "'create/update context'")

