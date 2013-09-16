# -*- coding: utf-8 -*-

from utils import commit

class Project(object):
    def __init__(self, id=None, name="", context=None, cursor=None):
        if id:
            self.id = id
        else:
            cursor.execute('SELECT MAX(_id) FROM project')
            id = cursor.fetchone()
            if id[0]:
                self.id = id[0] + 1
            else:
                self.id = 1
        self.name = name
        self.context = context
        self.actions = {}

    def addAction(self, action):
        self.actions[action.id] = action
        
    def removeAction(self, action):
        del self.actions[action.id]
        
    def generateHash(self):
        return hash(self.toString(True))
    
    def simpleCreate(self, app, update=False):
        context = None
        if self.context:
            context = self.context.id
    
        if update:
            app.cursor.execute('UPDATE project SET name=?, defaultContextId=? WHERE _id=?', 
                               [self.name, context, self.id])
        else:
            app.cursor.execute('Insert into project (_id, name, defaultContextId )' +
                               'values(?,?,?)', [self.id, self.name, context])
        commit(app, "'create/update project")
        
    def simpleDelete(self, app):
        app.cursor.execute('DELETE From project WHERE _id=?', (self.id,))
        commit(app, "'delete project")
    
    def toString(self, hash=False):
        context = ""
        if self.context:
            if hash:
                context = str(self.context.id)
            else:
                context = self.context.name
        string = "Name: " + self.name + "\nContext: " + context
        return string
