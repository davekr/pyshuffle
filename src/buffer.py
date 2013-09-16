from PyQt4 import QtCore, QtGui
import sqlite3
from datetime import datetime
import time
import os

from models import Action, Project, Context
import static
from utils import commit

actionsBuffer={}
projectsBuffer={}
contextsBuffer={}
tempActionBuffer = {}
tempProjectBuffer = {}
tempContextBuffer = {}

def clearBuffer():
    actionsBuffer.clear()
    projectsBuffer.clear()
    contextsBuffer.clear()
    
def clearTempBuffer():
    tempActionBuffer.clear()
    tempContextBuffer.clear()
    tempProjectBuffer.clear()

def appendAction(item, temp=False):
    if temp:
        tempActionBuffer[item.id] = item
    else:
        actionsBuffer[item.id] = item
    
def appendProject(item, temp=False):
    if temp:
        tempProjectBuffer[item.id] = item
    else:
        projectsBuffer[item.id] = item
    
def appendContext(item, temp=False):
    if temp:
        tempContextBuffer[item.id] = item
    else:
        contextsBuffer[item.id] = item
    
def createAction(app, item):
    if app.inSync:
        QtGui.QMessageBox.information(QtGui.QWidget(), "Abort", "You are in the middle of "
                                      + "a conflicted merge. Please resolve it first.")
        return
    
    appendAction(item)
    
    project = None
    context = None
    date = None
    
    if item.context:
        item.context.addAction(item)
        context = item.context.id
        app.contextTab.refresh_contexts()
    if item.project:
        item.project.addAction(item)
        project = item.project.id
        app.projectTab.refresh_projects()
    if item.sched:
        date = time.mktime(datetime.strptime(str(item.sched.toString('yyyy-MM-dd')), 
                                             "%Y-%m-%d").timetuple())
        app.calendarTab.refresh_calendar()
    app.inboxTab.refresh_inbox()
    app.nextTab.refresh_next()
        
    app.cursor.execute('Insert into task (_id, description, projectId, contextId, start, ' +
                   'details, complete) values(?,?,?,?,?,?,?)', [item.id, 
                                item.desc, project, context, date, item.details,
                                item.completed])
    commit(app, "'create action'")
    
def updateAction(app, item, projId, ctxId):
    if app.inSync:
        QtGui.QMessageBox.information(QtGui.QWidget(), "Abort", "You are in the middle of "
                                      + "a conflicted merge. Please resolve it first.")
        return
    
    appendAction(item)
    
    if projId:
        projectsBuffer[projId].removeAction(item)
        
    if ctxId:
        contextsBuffer[ctxId].removeAction(item)
    
    project = None
    context = None
    date = None
    
    if item.context:
        item.context.addAction(item)
        context = item.context.id
    if item.project:
        item.project.addAction(item)
        project = item.project.id
    if item.sched:
        date = time.mktime(datetime.strptime(str(item.sched.toString('yyyy-MM-dd')), 
                                             "%Y-%m-%d").timetuple())
        
    app.inboxTab.refresh_inbox()
    app.nextTab.refresh_next()
    app.calendarTab.refresh_calendar()
    app.projectTab.refresh_projects()
    app.contextTab.refresh_contexts()
    
    app.cursor.execute('UPDATE task SET description=?, projectId=?, contextId=?, details=?, ' +
                               'start=?, complete=? WHERE _id=?', [item.desc, project, 
                                context, item.details, date, item.completed, item.id])
    commit(app, "'update action'")
    
def deleteAction(app, item):
    if app.inSync:
        QtGui.QMessageBox.information(QtGui.QWidget(), "Abort", "You are in the middle of "
                                      + "a conflicted merge. Please resolve it first.")
        return
    
    if item.project:
        del item.project.actions[item.id]
    if item.context:
        del item.context.actions[item.id]
        
    del actionsBuffer[item.id]
    
    app.inboxTab.refresh_inbox()
    app.nextTab.refresh_next()
    app.calendarTab.refresh_calendar()
    app.projectTab.refresh_projects()
    app.contextTab.refresh_contexts()
    app.completeTab.refresh_complete()
    
    app.cursor.execute('DELETE From task WHERE _id=?', (item.id,))
    
    commit(app, "'delete action'")
    
def completeAction(app, item, restore=False):
    if app.inSync:
        QtGui.QMessageBox.information(QtGui.QWidget(), "Abort", "You are in the middle of "
                                      + "a conflicted merge. Please resolve it first.")
        return
    
    if restore:
        item.completed = 0
    else:
        item.completed = 1
    appendAction(item)
    
    app.completeTab.refresh_complete()
    app.inboxTab.refresh_inbox()
    app.nextTab.refresh_next()
    app.calendarTab.refresh_calendar()
    app.projectTab.refresh_projects()
    app.contextTab.refresh_contexts()
    
    app.cursor.execute('UPDATE task SET complete=? WHERE _id=?',
                        [item.completed, item.id])
    commit(app, "'complete action'")
    
def createProject(app, item, update=False):
    if app.inSync:
        QtGui.QMessageBox.information(QtGui.QWidget(), "Abort", "You are in the middle of "
                                      + "a conflicted merge. Please resolve it first.")
        return
    
    appendProject(item)
    
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
    
def deleteProject(app, item):
    if app.inSync:
        QtGui.QMessageBox.information(QtGui.QWidget(), "Abort", "You are in the middle of "
                                      + "a conflicted merge. Please resolve it first.")
        return
    
    for action in item.actions.values():
        action.project = None
    app.cursor.execute('DELETE From project WHERE _id=?', (item.id,))
    del projectsBuffer[item.id]
    commit(app, "'delete project")
    
    app.newTab.refresh_new()
    app.inboxTab.refresh_inbox()
    app.nextTab.refresh_next()
    app.calendarTab.refresh_calendar()
    app.projectTab.refresh_projects()
    app.contextTab.refresh_contexts()
    
def deleteContext(app, item):
    if app.inSync:
        QtGui.QMessageBox.information(QtGui.QWidget(), "Abort", "You are in the middle of "
                                      + "a conflicted merge. Please resolve it first.")
        return
    
    for action in item.actions.values():
        action.context = None
        
    for project in projectsBuffer.values():
        if project.context and project.context.id == item.id:
            project.context = None
    
    del contextsBuffer[item.id]
    app.cursor.execute('DELETE From context WHERE _id=?', (item.id,))
    commit(app, "'delete context")
    
    app.newTab.refresh_new()
    app.inboxTab.refresh_inbox()
    app.nextTab.refresh_next()
    app.calendarTab.refresh_calendar()
    app.projectTab.refresh_projects()
    app.contextTab.refresh_contexts()
    
    
def createContext(app, item, update=False):
    if app.inSync:
        QtGui.QMessageBox.information(QtGui.QWidget(), "Abort", "You are in the middle of "
                                      + "a conflicted merge. Please resolve it first.")
        return
    
    appendContext(item)
    
    color = None
    icon = None
    if item.icon:
        for i in static.icons:
            if static.icons[i] == item.icon:
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
        for project in projectsBuffer.values():
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
    
def init_sql(app):
    app.cursor.execute("CREATE TABLE IF NOT EXISTS "
                       + "context" 
                       + " ("
                       + "_id INTEGER PRIMARY KEY," 
                       + "name TEXT,"
                       + "colour INTEGER," 
                       + "iconName TEXT," 
                       + "tracks_id INTEGER," 
                       + "modified INTEGER"
                       + ");")
    app.cursor.execute("CREATE TABLE IF NOT EXISTS " 
                       + "project"
                       + " ("
                       + "_id INTEGER PRIMARY KEY," 
                       + "name TEXT,"
                       + "archived INTEGER," 
                       + "defaultContextId INTEGER," 
                       + "tracks_id INTEGER," 
                       + "modified INTEGER," 
                       + "parallel INTEGER NOT NULL DEFAULT 0"
                       + ");")
    app.cursor.execute("CREATE TABLE IF NOT EXISTS "
                       + "task" 
                       + " ("
                       + "_id INTEGER PRIMARY KEY," 
                       + "description TEXT,"
                       + "details TEXT," 
                       + "contextId INTEGER,"
                       + "projectId INTEGER," 
                       + "created INTEGER,"
                       + "modified INTEGER," 
                       + "due INTEGER,"
                       + "start INTEGER," 
                       + "timezone TEXT,"
                       + "allDay INTEGER NOT NULL DEFAULT 0,"
                       + "hasAlarm INTEGER NOT NULL DEFAULT 0,"
                       + "calEventId INTEGER,"
                       + "displayOrder INTEGER," 
                       + "complete INTEGER," 
                       + "tracks_id INTEGER"
                       + ");")

def init_buffer(app, temp=False):
    cursor = app.cursor
    #context
    cursor.execute('SELECT _id, name, colour, iconName FROM context')
    contexts = cursor.fetchall()
    for row in contexts:
        style = None
        icon = None
        if(row[2]):
            style = static.styles[row[2]]
        if(row[3]):
            icon = static.icons[row[3]]
        context = Context(row[0], row[1], style, icon)
        appendContext(context, temp)
    #project    
    cursor.execute('SELECT _id, name, defaultContextId FROM project')
    projects = cursor.fetchall()
    for row in projects:
        context = None
        if temp:
            for ctx in tempContextBuffer:
                if ctx == row[2]:
                    context = tempContextBuffer[ctx]
        else:
            for ctx in contextsBuffer:
                if ctx == row[2]:
                    context = contextsBuffer[ctx]
        proj = Project(row[0], row[1], context)
        appendProject(proj, temp)
    #action
    cursor.execute('SELECT _id, description, projectId, contextId, details, ' +
                   'start, complete FROM task ORDER BY start desc')
    actions = cursor.fetchall()
    for row in actions:
        project = None
        context = None
        if temp:
            for proj in tempProjectBuffer:
                if proj == row[2]:
                    project = tempProjectBuffer[proj]
            for ctx in tempContextBuffer:
                if ctx == row[3]:
                    context = tempContextBuffer[ctx]
        else:
            for proj in projectsBuffer:
                if proj == row[2]:
                    project = projectsBuffer[proj]
            for ctx in contextsBuffer:
                if ctx == row[3]:
                    context = contextsBuffer[ctx]
        date = QtCore.QDate()
        if row[5]:
            date = date.fromString(str(datetime.fromtimestamp(row[5]).date()), 
                                   'yyyy-MM-dd')
        action = Action(row[0], row[1], project, context, date, row[4], row[6])
        appendAction(action, temp)
        if action.project:
            project.addAction(action)
        if action.context:
            context.addAction(action)
            
def closeConn(app):
    app.cursor.close()
    app.con.close()
    
def init_db(app):
    db = os.path.join(app.db, 'shuffle.db')
    if not os.path.exists(db):
        app.con = sqlite3.connect(db)
        init_backup(app)
    else:
        app.con = sqlite3.connect(db)
    app.cursor = app.con.cursor()

def init_backup(app):
    with open(os.path.join(app.db, 'demo.sql')) as sql:
        app.con.executescript(sql.read())
