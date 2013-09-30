# -*- coding: utf-8 -*-

from app.dbmanager import DBManager
from settings import DATE_FORMAT

class Action(object):

    def __init__(self, id=None, desc="", project=None, context=None, 
                 sched=None, details="", completed=0, cursor=None):
        self.id = id
        self.desc = desc
        self.project = project
        self.context = context
        self.details = details or ""
        self.sched = sched
        self.completed = completed
        if self.project:
            project.addAction(self)
        if self.context:
            context.addAction(self)

    def class_name(self):
        return self.__class__.__name__.lower()
        
    def generateHash(self):
        return hash(self.toString(True))

    def save(self):
        if not self.id:
            DBManager.create_action(self)
        else:
            DBManager.update_action(self)

    def delete(self):
        DBManager.delete_action(self)
    
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
            sched = self.sched.toString(DATE_FORMAT)
        detail = self.details or ""
        completed = self.completed or "False"
        string = "Name: " + self.desc + "\nProject: " + project + "\nContext: " 
        string = string + context + "\nDate: " + sched + "\nDescription: " + detail
        string = string + "\nCompleted: " + str(completed)
        return string
