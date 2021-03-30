from django.shortcuts import render
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from .models import UserEvent, UserRegisterEvent
from .serializers import *

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
# from django.http import HttpResponse
from rest_framework.views import APIView

from django.core import serializers
import json
import datetime

User = get_user_model()


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class EventView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = EventSerializer


class GetAllEventView(APIView):
    def get(self, request):
        SomeModel_json = serializers.serialize("json", UserEvent.objects.all())
        data = json.loads(SomeModel_json)

        data_lst = []

        for item in data:
            organizer = serializers.serialize(
                "json", [User.objects.get(username=item['fields']['organizer'])])
            organizer_data = json.loads(organizer)

            # print(item['fields']['event_name'])
            event = UserEvent.objects.get(
                event_name=item['fields']['event_name'])
            document_lst = []

            document_data = EventDocument.objects.filter(event=event)

            for document in document_data:
                document_dict = {
                    "data": document.data,
                }

                document_lst.append(document_dict)


            item['fields']['documents'] = document_lst

            # print(document_data)

            item['fields']['organizer'] = {
                "username": organizer_data[0]['fields']['username'],
                "first_name": organizer_data[0]['fields']['first_name'],
                "last_name": organizer_data[0]['fields']['last_name'],
                "email": organizer_data[0]['fields']['email'],
                "phone": organizer_data[0]['fields']['phone']
            }

            data_lst.append(item['fields'])

        return Response(data_lst, content_type='application/json; charset=utf-8')


class GetEventDetail(APIView):
    def post(self, request):
        User_obj = User.objects.get(username=request.data['organizer'])
        data = {
            "first_name": User_obj.first_name,
            "last_name": User_obj.last_name,
            "phone": User_obj.phone,
        }

        return Response(data, content_type='application/json; charset=utf-8')


class RegisterEvent(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = EventRegisterSerializer


class GetEventPeople(APIView):
    def post(self, request):
        event = UserEvent.objects.get(event_name=request.data['event_name'])
        event_register = serializers.serialize("json", UserRegisterEvent.objects.filter(event_id= event.id))
        data = json.loads(event_register)

        user_lst = []
        for item in data:
            user = User.objects.get(id=item['fields']['user'])

            user_data = {
                "first_name": user.first_name,
                "last_name": user.last_name
            }

            user_lst.append(user_data)

        return Response(user_lst, content_type='application/json; charset=utf-8')


class GetEventAttendance(APIView):
    def post(self, request):
        user = User.objects.get(username=request.data['username'])
        event_register = UserRegisterEvent.objects.filter(user_id= user.id)

        event_lst = []
        for item in event_register:
            event = serializers.serialize("json", [UserEvent.objects.get(id= item.event_id)])
            data = json.loads(event)

            event_lst.append(data[0]['fields'])

        return Response(event_lst, content_type='application/json; charset=utf-8')


class GetEventAvaliableCheckin(APIView):
    def post(self, request):
        user = User.objects.get(username=request.data['username'])
        event_register = UserRegisterEvent.objects.filter(user_id= user.id)

        x = datetime.datetime.now()

        event_lst = []
        available_lst = []
        unavailable_lst = []
        coming_lst = []

        for item in event_register:
            event = serializers.serialize("json", [UserEvent.objects.get(id= item.event_id)])
            data = json.loads(event)

            x = datetime.datetime.now()

            if(datetime.datetime(
                int(data[0]['fields']['duration'][0:4]),
                int(data[0]['fields']['duration'][5:7]),
                int(data[0]['fields']['duration'][8:10])
            ) <=
                datetime.datetime(
                int(x.strftime("%Y")),
                int(x.strftime("%m")),
                int(x.strftime("%d")))
                and
                datetime.datetime(
                int(data[0]['fields']['duration'][13:17]),
                int(data[0]['fields']['duration'][18:20]),
                int(data[0]['fields']['duration'][21:23])
            ) >=
                datetime.datetime(
                int(x.strftime("%Y")),
                int(x.strftime("%m")),
                int(x.strftime("%d")))):
                available_lst.append(data[0]['fields'])

            elif(datetime.datetime(
                int(data[0]['fields']['duration'][0:4]),
                int(data[0]['fields']['duration'][5:7]),
                int(data[0]['fields']['duration'][8:10])
            ) <
                datetime.datetime(
                int(x.strftime("%Y")),
                int(x.strftime("%m")),
                int(x.strftime("%d")))
                and
                datetime.datetime(
                int(data[0]['fields']['duration'][13:17]),
                int(data[0]['fields']['duration'][18:20]),
                int(data[0]['fields']['duration'][21:23])
            ) <
                datetime.datetime(
                int(x.strftime("%Y")),
                int(x.strftime("%m")),
                int(x.strftime("%d")))
            ):
                unavailable_lst.append(data[0]['fields'])

            else:
                coming_lst.append(data[0]['fields'])

        available_data = {
            "available": available_lst
        }

        coming_data = {
            "coming": coming_lst
        }

        unavailable_data = {
            "unavailable": unavailable_lst
        }

        event_lst.append(available_data)
        event_lst.append(coming_data)
        event_lst.append(unavailable_data)

        return Response(event_lst, content_type='application/json; charset=utf-8')


class EventCheckView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = EventCheckSerializer

class EventApproverView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ApproveEventSerializer
