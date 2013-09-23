
import sqlite3
import os
import time

from app.utils import convert_from_date
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

    @classmethod
    def create_action(cls, action):
        project_id = action.project.id if action.project else None
        context_id = action.context.id if action.context else None
        start = convert_from_date(action.sched)
        action_id = cls.generate_id()
        cls.execute(cls.INSERT_ACTION, [action_id, action.desc, project_id, \
                                        context_id, action.details, start, action.completed])
        action.id = action_id
        cls._buffer._buffer_action(action)

    @classmethod
    def update_action(cls, action):
        project_id = action.project.id if action.project else None
        context_id = action.context.id if action.context else None
        start = convert_from_date(action.sched)
        cls.execute(cls.UPDATE_ACTION, [action.desc, project_id, context_id, \
                                        action.details, start, action.completed, action.id])
        cls._buffer._buffer_action(action)

    @classmethod
    def delete_action(cls, action):
        cls.execute(cls.DELETE_ACTION, [action.id])
        cls._buffer._del_action(action)

    @classmethod
    def create_project(cls, project):
        context_id = project.context.id if project.context else None
        project_id = cls.generate_id()
        cls.execute(cls.INSERT_PROJECT, [project_id, project.name, context_id])
        project.id = project_id
        cls._buffer._buffer_project(project)

    @classmethod
    def update_project(cls, project):
        context_id = project.context.id if project.context else None
        cls.execute(cls.UPDATE_PROJECT, [project.name, context_id, project.id])
        cls._buffer._buffer_project(project)

    @classmethod
    def delete_project(cls, project):
        cls.execute(cls.DELETE_PROJECT, [project.id])
        cls._buffer._del_action(project)

    @classmethod
    def create_context(cls, context):
        context_id = cls.generate_id()
        cls.execute(cls.INSERT_CONTEXT, [context_id, context.color, context.icon])
        context.id = context_id
        cls._buffer._buffer_action(context)

    @classmethod
    def update_context(cls, context):
        cls.execute(cls.UPDATE_CONTEXT, [context.color, context.icon, context.id])
        cls._buffer._buffer_action(context)

    @classmethod
    def delete_context(cls, context):
        cls.execute(cls.DELETE_ACTION, [context.id])
        cls._buffer._del_action(context)

    @classmethod
    def generate_id(cls):
        """Because of the compatibility with Android Shuffle, 
        we cannot use autoincrement and have to generate our own
        unique id."""
        return int(time.time() * 1000000)
        
