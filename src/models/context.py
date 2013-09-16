# -*- coding: utf-8 -*-

import static
from utils import commit

class Context(object):
    def __init__(self, id=None, name="", color=None, icon=None, cursor=None):
        if id:
            self.id = id
        else:
            cursor.execute('SELECT MAX(_id) FROM Context')
            id = cursor.fetchone()
            if id[0]:
                self.id = id[0] + 1
            else:
                self.id = 1
        self.name = name
        self.color = color
        self.icon = icon
        self.actions = {}
        #self.projects = []  #no use

    def addAction(self, action):
        self.actions[action.id] = action
        
    def removeAction(self, action):
        del self.actions[action.id]
        
    def generateHash(self):
        return hash(self.toString())
    
    def simpleCreate(self, app, update=False):
        icon = None
        color = None
        if self.icon:
            for i in static.icons:
                if static.icons[i] == self.icon:
                    icon = i
        if self.color:
            for i in static.styles:
                if static.styles[i] == self.color:
                    color = i
    
        if update:
            app.cursor.execute('UPDATE context SET name=?, colour=?, iconName=? WHERE _id=?', 
                               [self.name, color, icon, self.id])
        else:
            app.cursor.execute('Insert into context (_id, name, colour, iconName) values(?,?,?,?)',
                                [self.id, self.name, color, icon])
        commit(app, "'create/update context")
        
    def simpleDelete(self, app):
        app.cursor.execute('DELETE From context WHERE _id=?', (self.id,))
        commit(app, "'delete context'")
    
    def toString(self):
        color = self.color or ""
        icon = self.icon or ""
        string = "Name: " + self.name + "\nColor: " + color + "\nIcon: " + icon
        return string
