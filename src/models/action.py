# -*- coding: utf-8 -*-

import time
from datetime import datetime
from utils import commit

class Action(object):
    def __init__(self, id=None, desc="", project=None, context=None, 
                 sched=None, details=None, completed=0, cursor=None):
        if id:
            self.id = id
        else:
            cursor.execute('SELECT MAX(_id) FROM task')
            id = cursor.fetchone()
            if id[0]:
                self.id = id[0] + 1
            else:
                self.id = 1
        self.desc = desc
        self.project = project
        self.context = context
        self.details = details or ""
        self.sched = sched
        self.completed = completed
        
    def generateHash(self):
        return hash(self.toString(True))
    
    def simpleCreate(self, app, update=False):
        project = None
        context = None
        date = None
    
        if self.context:
            context = self.context.id
        if self.project:
            project = self.project.id
        if self.sched:
            date = time.mktime(datetime.strptime(str(self.sched.toString('yyyy-MM-dd'), 
                                                     "%Y-%m-%d")).timetuple())
        
        if update:
            app.cursor.execute('UPDATE task SET description=?, projectId=?, contextId=?, details=?, ' +
                               'start=?, complete=? WHERE _id=?', [self.desc, project, 
                                context, self.details, date, self.completed,self.id])
        else:
            app.cursor.execute('Insert into task (_id, description, projectId, contextId, start, ' +
                   'details, complete) values(?,?,?,?,?,?,?)', [self.id, 
                                self.desc, project, context, date, self.details,
                                self.completed])
        commit(app, "'create/update action'")
        
    def simpleDelete(self, app):
        app.cursor.execute('DELETE From task WHERE _id=?', (self.id,))
        commit(app, "'delete action'")
    
    def toString(self, hash=False):
        context = ""
        if self.context:
            if hash:
                context = str(self.context.id)
            else:
                context = self.context.name
        project = ""
        if self.project:
            if hash:
                project = str(self.project.id)
            else:
                project = self.project.name
        sched = ""
        if self.sched:
            sched = self.sched.toString('yyyy-MM-dd')
        detail = self.details or ""
        completed = self.completed or "False"
        string = "Name: " + self.desc + "\nProject: " + project + "\nContext: " 
        string = string + context + "\nDate: " + sched + "\nDescription: " + detail
        string = string + "\nCompleted: " + str(completed)
        return string
