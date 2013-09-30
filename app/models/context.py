# -*- coding: utf-8 -*-

from app.dbmanager import DBManager

class Context(object):

    def __init__(self, id=None, name="", color=None, icon=None, cursor=None):
        self.id = id
        self.name = name
        self.color = color
        self.icon = icon
        self.actions = {}

    def class_name(self):
        return self.__class__.__name__.lower()

    def addAction(self, action):
        self.actions[action.id] = action

    def save(self):
        if not self.id:
            DBManager.create_context(self)
        else:
            DBManager.update_context(self)

    def delete(self):
        DBManager.delete_context(self)
        
    def removeAction(self, action):
        del self.actions[action.id]
        
    def generateHash(self):
        return hash(self.toString())
    
    def toString(self):
        color = self.color or ""
        icon = self.icon or ""
        string = "Name: " + self.name + "\nColor: " + color + "\nIcon: " + icon
        return string
