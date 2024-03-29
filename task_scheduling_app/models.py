from django.db import models
from account.models import User
import logging
# Create your models here.

class Task(models.Model):
    task_assigned = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=20, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    @staticmethod
    def create_task(user, task_name, status):

        obj = Task.objects.create(task_assigned=user, task_name=task_name, status=status)
        return obj

    @staticmethod
    def get_all_task_list():
        task_list = Task.objects.all().select_related('task_assigned').values('task_name', 'created_on',
                                                                              'task_assigned__username','status')
        formatted_task_list = []
        for task in task_list:
            created_on = task['created_on']
            task_assigned_username = task['task_assigned__username']  # Corrected access to the username
            task['date'] = created_on.date()
            task['time'] = created_on.time()
            task['assigned_by'] = task_assigned_username  # Corrected assignment of the username
            del task['created_on']
            task['status'] = "Pending" if not task['status'] else "Completed"
            formatted_task_list.append(task)
        return formatted_task_list


class CreateTaskManager:
    def __init__(self, requested_data):
        self.requested_data = requested_data

    def save_user_task(self):
        resp_dict = dict(status=False, message="Something went wrong")
        try:
            task_name = self.requested_data.data.get('task_name', None)
            task_assigned = self.requested_data.data.get('task_assigned', None)
            status = self.requested_data.data.get('status', False)
            user = User.get_user_object(task_assigned)
            if task_assigned is not None and task_name is not None:
                Task.create_task(user, task_name,status)
                resp_dict['status'] = True
                resp_dict['message'] = "Task Created Successfully"
        except Exception as e:
            logging.error('getting exception on save_user_task', repr(e))
        return resp_dict


class GetTaskManager:
    def __init__(self):
        self.task_list = Task.get_all_task_list()

    def get_task_list(self):
        resp_dict = dict(status=False, message="Something went wrong", data=dict())
        resp_dict['data'] = self.task_list
        resp_dict['status'] = True
        resp_dict['message'] = "Got Task list Successfully"

        return resp_dict
