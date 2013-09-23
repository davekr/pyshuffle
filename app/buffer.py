# -*- coding: utf-8 -*- 

from app.models import Action, Project, Context 
from app.utils import convert_to_date
from app import static

class Buffer(object):

    def __init__(self):
        self._actions = {}
        self._projects = {}
        self._contexts = {}

    def init_buffers(self, contexts, projects, actions):
        self._init_contexts(contexts)
        self._init_projects(projects)
        self._init_actions(actions)

    def _init_contexts(self, contexts):
        for row in contexts:
            style = static.styles.get(row['colour'])
            icon = static.contexticons.get(row['iconName'])
            context = Context(row['_id'], row['name'], style, icon)
            self._buffer_context(context)

    def _init_projects(self, projects):
        for row in projects:
            context = self._contexts.get(row['defaultContextId'])
            project = Project(row['_id'], row['name'], context)
            self._buffer_project(project)

    def _init_actions(self, actions):
        for row in actions:
            project = self._projects.get(row['projectId'])
            context = self._contexts.get(row['contextId'])
            date = convert_to_date(row['start'])
            action = Action(row['_id'], row['description'], project, context, \
                            date, row['details'], row['complete'])
            self._buffer_action(action)

    def _buffer_context(self, context):
        self._add_buffer(self._contexts, context)

    def _buffer_project(self, project):
        self._add_buffer(self._projects, project)

    def _buffer_action(self, action):
        self._add_buffer(self._actions, action)

    def _add_buffer(self, buffer, item):
        buffer[item.id] = item

    def get_actions(self):
        return self._actions

    def get_projects(self):
        return self._projects

    def get_contexts(self):
        return self._contexts

