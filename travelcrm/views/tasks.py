# -*-coding: utf-8-*-

import logging
import datetime

import colander
from pyramid.view import view_config

from ..models import DBSession
from ..models.task import Task
from ..lib.qb.tasks import TasksQueryBuilder
from ..lib.utils.common_utils import translate as _
from ..forms.tasks import TaskSchema


log = logging.getLogger(__name__)


class Tasks(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(
        context='..resources.tasks.Tasks',
        request_method='GET',
        renderer='travelcrm:templates/tasks/index.mak',
        permission='view'
    )
    def index(self):
        status = Task.STATUS
        priority = Task.PRIORITY
        return {
            'status': status,
            'priority': priority
        }

    @view_config(
        name='list',
        context='..resources.tasks.Tasks',
        xhr='True',
        request_method='POST',
        renderer='json',
        permission='view'
    )
    def list(self):
        qb = TasksQueryBuilder(self.context)
        qb.search_simple(
            self.request.params.get('q'),
        )
        qb.advanced_search(
            updated_from=self.request.params.get('updated_from'),
            updated_to=self.request.params.get('updated_to'),
            modifier_id=self.request.params.get('modifier_id'),
        )
        id = self.request.params.get('id')
        if id:
            qb.filter_id(id.split(','))
        qb.sort_query(
            self.request.params.get('sort'),
            self.request.params.get('order', 'asc')
        )
        qb.page_query(
            int(self.request.params.get('rows')),
            int(self.request.params.get('page'))
        )
        return {
            'total': qb.get_count(),
            'rows': qb.get_serialized()
        }

    @view_config(
        name='add',
        context='..resources.tasks.Tasks',
        request_method='GET',
        renderer='travelcrm:templates/tasks/form.mak',
        permission='add'
    )
    def add(self):
        return {'title': _(u'Add Task')}

    @view_config(
        name='add',
        context='..resources.tasks.Tasks',
        request_method='POST',
        renderer='json',
        permission='add'
    )
    def _add(self):
        schema = TaskSchema().bind(request=self.request)

        try:
            controls = schema.deserialize(self.request.params)
            if controls.get('reminder_date'):
                reminder = datetime.datetime.combine(
                    controls.get('reminder_date'),
                    controls.get('reminder_time')
                )
            else:
                reminder = None
            task = Task(
                employee_id=controls.get('employee_id'),
                title=controls.get('title'),
                deadline=controls.get('deadline'),
                reminder=reminder,
                descr=controls.get('descr'),
                priority=controls.get('priority'),
                status=controls.get('status'),
                resource=self.context.create_resource()
            )
            DBSession.add(task)
            DBSession.flush()
            return {
                'success_message': _(u'Saved'),
                'response': task.id
            }
        except colander.Invalid, e:
            return {
                'error_message': _(u'Please, check errors'),
                'errors': e.asdict()
            }

    @view_config(
        name='edit',
        context='..resources.tasks.Tasks',
        request_method='GET',
        renderer='travelcrm:templates/tasks/form.mak',
        permission='edit'
    )
    def edit(self):
        task = Task.get(self.request.params.get('id'))
        return {'item': task, 'title': _(u'Edit Task')}

    @view_config(
        name='edit',
        context='..resources.tasks.Tasks',
        request_method='POST',
        renderer='json',
        permission='edit'
    )
    def _edit(self):
        schema = TaskSchema().bind(request=self.request)
        task = Task.get(self.request.params.get('id'))
        try:
            controls = schema.deserialize(self.request.params)
            if controls.get('reminder_date'):
                reminder = datetime.datetime.combine(
                    controls.get('reminder_date'),
                    controls.get('reminder_time')
                )
            else:
                reminder = None
            task.employee_id = controls.get('employee_id')
            task.title = controls.get('title')
            task.deadline = controls.get('deadline')
            task.reminder = reminder
            task.descr = controls.get('descr')
            task.priority = controls.get('priority')
            task.status = controls.get('status')
            return {
                'success_message': _(u'Saved'),
                'response': task.id
            }
        except colander.Invalid, e:
            return {
                'error_message': _(u'Please, check errors'),
                'errors': e.asdict()
            }

    @view_config(
        name='delete',
        context='..resources.tasks.Tasks',
        request_method='GET',
        renderer='travelcrm:templates/tasks/delete.mak',
        permission='delete'
    )
    def delete(self):
        return {
            'title': _(u'Delete Tasks'),
            'rid': self.request.params.get('rid')
        }

    @view_config(
        name='delete',
        context='..resources.tasks.Tasks',
        request_method='POST',
        renderer='json',
        permission='delete'
    )
    def _delete(self):
        errors = 0
        for id in self.request.params.getall('id'):
            item = Task.get(id)
            if item:
                DBSession.begin_nested()
                try:
                    DBSession.delete(item)
                    DBSession.commit()
                except:
                    errors += 1
                    DBSession.rollback()
        if errors > 0:
            return {
                'error_message': _(
                    u'Some objects could not be delete'
                ),
            }
        return {'success_message': _(u'Deleted')}