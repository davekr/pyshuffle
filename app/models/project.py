# -*- coding: utf-8 -*-

from app.dbmanager import DBManager

class Project(object):

    def __init__(self, id=None, name="", context=None):
        self.id = id
        self.name = name
        self.context = context
        self.actions = {}

    def save(self):
        if not self.id:
            DBManager.create_project(self)
        else:
            DBManager.update_project(self)

    def delete(self):
        DBManager.delete_project(self)

    def addAction(self, action):
        self.actions[action.id] = action
        
    def removeAction(self, action):
        del self.actions[action.id]
        
    def generateHash(self):
        return hash(self.toString(True))
    
    def toString(self, hash=False):
        context = ""
        if self.context:
            if hash:
                context = str(self.context.id)
            else:
                context = self.context.name
        string = "Name: " + self.name + "\nContext: " + context
        return string
