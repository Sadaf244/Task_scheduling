from rest_framework.views import APIView
from django.http import JsonResponse
import logging
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from task_scheduling_app.models import CreateTaskManager, GetTaskManager


class CreateTask(APIView):

    def post(self, request):
        resp_dict = dict()
        resp_dict['status'] = False
        resp_dict['message'] = "Something went wrong. Please try again after sometime"
        try:
            create_note_manager = CreateTaskManager(request)
            save_user_history_resp = create_note_manager.save_user_task()
            resp_dict['status'] = save_user_history_resp['status']
            resp_dict['message'] = save_user_history_resp['message']
        except Exception as e:
            logging.error('getting exception on CreateNote', repr(e))
        return JsonResponse(resp_dict, status=200)


class GetTask(APIView):

    def get(self, request):  # <-- Add request parameter here
        resp_dict = dict()
        resp_dict['status'] = False
        resp_dict['message'] = "Something went wrong. Please try again after sometime"
        try:
            get_note_manager_resp = GetTaskManager().get_task_list()  # <-- Initialize GetTaskManager object
            resp_dict['data'] = get_note_manager_resp['data']
            resp_dict['status'] = get_note_manager_resp['status']
            resp_dict['message'] = get_note_manager_resp['message']
        except Exception as e:
            logging.error('getting exception on GetNote', repr(e))
        return JsonResponse(resp_dict, status=200)