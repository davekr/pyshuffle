#import uuid
from git import *
import time
from datetime import datetime
import static

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
                                                     "%Y-%m-%d")).timetuple()) * 1000
        
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
    
    
def commit(app, message):
    app.con.commit()
    repo = Repo(app.db)
    repo.git.execute(["git", "add", "shuffle.db"])
    repo.git.execute(["git","commit","-m", message])
