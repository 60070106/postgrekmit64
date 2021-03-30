from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import datetime

import base64
from PIL import Image
from io import BytesIO
from pathlib import Path

import shutil
import face_recognition
import requests
import os
import math
import json
from django.conf import settings


User = get_user_model()


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ['imgpath', ]


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=12)
    email = serializers.EmailField(max_length=None)
    image = ImageSerializer(many=True)
    is_camper = serializers.BooleanField(default=False)
    is_organizer = serializers.BooleanField(default=False)
    is_approver = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone', 'email', 'is_camper', 'is_organizer', 'is_approver',  'image']


class RegisterSerializer(serializers.ModelSerializer):
    image = ImageSerializer(many=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'phone',
                  'first_name', 'last_name', 'image', 'email']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        imgdata = attrs['image'][0]['imgpath']
        im = Image.open(BytesIO(base64.b64decode(imgdata)))

        Path('images/'+attrs['username']).mkdir(parents=True, exist_ok=True)
        im.save('images/'+attrs['username']+'/'+'register.png', 'PNG')

        save_path = "%s" % (settings.BASE_DIR)+"\\images\\" + \
            attrs['username']+'\\'+'register.png'
        send_to_check_Pic = face_recognition.load_image_file(save_path)
        send_to_check_face_encoding = face_recognition.face_encodings(
            send_to_check_Pic)

        if len(send_to_check_face_encoding) > 0:
            attrs['password_temp'] = attrs['password']
            return attrs
        else:
            shutil.rmtree("%s" % (settings.BASE_DIR) +
                          "\\images\\"+attrs['username'])
            raise serializers.ValidationError(
                {"detail": "didn't find any facial."})

    def create(self, validated_data):
        if(validated_data['email'][0:8].isdigit()
        and (validated_data['email'][9:] == "kmitl.ac.th"
        or validated_data['email'][9:] == "it.kmitl.ac.th")):
            user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            is_organizer=True
        )

        elif(validated_data['email'][-11:] == "kmitl.ac.th"
        or validated_data['email'][-14:] == "it.kmitl.ac.th"):
            user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            is_approver=True
        )

        else:
           user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            is_camper=True
        ) 
        

        userimage = UserImage.objects.create(
            user=user, imgpath=validated_data['image'][0]['imgpath'])
        user.set_password(validated_data['password'])

        userimage.save()
        user.save()

        return user
        # return "eiei"

    def to_representation(self, instance):
        return {
            "success" : True
        }


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializer(self.user)

        user = User.objects.get(username=self.user.username)
        user.last_login = datetime.datetime.now()
        user.save()

        return {
            "success": True,
            "token": data["access"],
            "user": serializer.data
        }

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDocument
        fields = ['data', ]


class EventSerializer(serializers.ModelSerializer):
    imgpath = serializers.CharField(max_length=None)
    imgevent = serializers.CharField(max_length=None)
    documents = DocumentSerializer(many=True)

    class Meta:
        model = UserEvent
        fields = ['organizer', 'location', 'duration',
                  'event_name', 'detail', 'imgpath', 'imgevent', 'documents']

    def validate(self, attrs):
        amount_pic = 1

        save_path = "%s" % (settings.BASE_DIR) + \
            "\\images\\"+attrs['organizer']+'\\'
        for filename in os.listdir(save_path):
            amount_pic += 1

        save_time = datetime.datetime.now()
        save_time = save_time.strftime("%d%m%y%M%S")

        imgdata = attrs['imgpath']
        im = Image.open(BytesIO(base64.b64decode(imgdata)))
        im.save('images/'+attrs['organizer']+'/' + save_time + '.png', 'PNG')

        send_to_check_Pic = face_recognition.load_image_file(
            save_path + save_time + '.png')
        send_to_check_face_encoding = face_recognition.face_encodings(
            send_to_check_Pic)

        face_encoding_lst = []

        try:
            User.objects.get(username=attrs['organizer'])

            if len(send_to_check_face_encoding) > 0:
                percentage = 0
                for filename in os.listdir(save_path):
                    fileDirectory_Pic = face_recognition.load_image_file(
                        save_path + filename)
                    fileDirectory_encoding = face_recognition.face_encodings(
                        fileDirectory_Pic)

                    face_encoding_lst.append(fileDirectory_encoding[0])

                for face_encoding in face_encoding_lst:
                    face_distance = face_recognition.face_distance(
                        face_encoding, send_to_check_face_encoding)
                    if (face_distance > 0.6):
                        range = (1.0 - 0.6)
                        linear_val = (1.0 - face_distance) / (range * 2.0)
                        percentage += linear_val * 100
                    else:
                        range = 0.6
                        linear_val = 1.0 - (face_distance / (range * 2.0))
                        percentage += (linear_val + ((1.0 - linear_val)
                                                     * math.pow((linear_val - 0.5) * 2, 0.2))) * 100

                percentage /= amount_pic

                if(percentage >= 80):
                    attrs["percentage"] = "%.2f" % (percentage) + "%"
                    user = User.objects.get(username=attrs['organizer'])
                    userimage = UserImage.objects.create(
                        user=user, imgpath=attrs['imgpath'])
                    userimage.save()

                    return attrs
                else:
                    os.remove("%s" % (settings.BASE_DIR)+"\\images\\" +
                              attrs['organizer']+"\\"+save_time+'.png')
                    raise serializers.ValidationError({
                        "error": "Your identity is matching less than 80% \nyour matching :" + "%.2f" % (percentage[0]) + "%"
                    })

            else:
                os.remove("%s" % (settings.BASE_DIR)+"\\images\\" +
                          attrs['organizer']+"\\"+save_time+'.png')
                raise serializers.ValidationError(
                    {"error": "didn't find any facial."})

        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"error": "didn't find your user account."})

    def create(self, validated_data):
        user = User.objects.get(username=validated_data['organizer'])
        event = UserEvent.objects.create(
            user=user,
            organizer=validated_data['organizer'],
            location=validated_data['location'],
            duration=validated_data['duration'],
            event_name=validated_data['event_name'],
            event_image=validated_data['imgevent'],
            detail=validated_data['detail'],
        )

        print(validated_data['percentage'])

        event.save()

        for item in validated_data['documents']:
            doc = EventDocument.objects.create(
                event = event,
                data = item['data'])
            doc.save()

        return event

    def to_representation(self, instance):
        return {"success": True}


class EventRegisterSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)

    class Meta:
        model = UserRegisterEvent
        fields = ['event_name', 'username']

    def validate(self, attrs):
        event = UserEvent.objects.get(event_name=attrs["event_name"])
        user = User.objects.get(username=attrs["username"])

        try:
            UserRegisterEvent.objects.get(event_id=event.id, user_id=user.id)
            raise serializers.ValidationError(
                {"detail": "This account already registered"})

        except UserRegisterEvent.DoesNotExist:
            return attrs

    def create(self, validated_data):
        event = UserEvent.objects.get(event_name=validated_data["event_name"])
        user = User.objects.get(username=validated_data["username"])

        regist_user = UserRegisterEvent.objects.create(
            event=event,
            user=user
        )

        regist_user.save()
        return regist_user

    def to_representation(self, instance):
        return {"success": True}


class EventCheckSerializer(serializers.ModelSerializer):
    imgpath = serializers.CharField(max_length=None)
    event_name = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)

    class Meta:
        model = EventHistory
        fields = ['event_name', 'username', 'status', 'imgpath']

    def validate(self, attrs):
        amount_pic = 0

        save_path = "%s" % (settings.BASE_DIR) + \
            "\\images\\"+attrs['username']+'\\'

        save_time = datetime.datetime.now()
        save_time = save_time.strftime("%d%m%y%M%S")

        imgdata = attrs['imgpath']
        im = Image.open(BytesIO(base64.b64decode(imgdata)))
        print("writing file...")
        im.save('images/'+attrs['username']+'/' + save_time + '.png', 'PNG')
        print("finish writing file")

        send_to_check_Pic = face_recognition.load_image_file(
            save_path + save_time + '.png')
        print("loading image...")
        send_to_check_face_encoding = face_recognition.face_encodings(
            send_to_check_Pic)
        print("encoding image...")

        face_encoding_lst = []

        for filename in os.listdir(save_path):
            amount_pic += 1
            fileDirectory_Pic = face_recognition.load_image_file(save_path + filename)
            fileDirectory_encoding = face_recognition.face_encodings(fileDirectory_Pic)
            face_encoding_lst.append(fileDirectory_encoding[0])
            print("encoding with file: ",  filename)
        

        try:
            user_for_check = User.objects.get(username=attrs['username'])
            print("get user object")

            if len(send_to_check_face_encoding) > 0:
                percentage = 0

                for face_encoding in face_encoding_lst:
                    face_distance = face_recognition.face_distance(
                        face_encoding, send_to_check_face_encoding)
                    if (face_distance > 0.6):
                        range = (1.0 - 0.6)
                        linear_val = (1.0 - face_distance) / (range * 2.0)
                        percentage += linear_val * 100
                    else:
                        range = 0.6
                        linear_val = 1.0 - (face_distance / (range * 2.0))
                        percentage += (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
                    print("find matching percentage with face encoding: ",face_encoding)

                percentage /= amount_pic
                print("calculate average percentage with all file")

                if(percentage >= 80):
                    print("percentage is much or equal than 80: ", percentage, "%")

                    event = UserEvent.objects.get(
                        event_name=attrs["event_name"])
                    print("get user event object")
                    regist_event = UserRegisterEvent.objects.get(
                        event=event,
                        user=user_for_check
                    )
                    print("get user register event object")

                    try:
                        regist_event = EventHistory.objects.filter(
                            event=regist_event).latest('time')
                        print("get lastest event history object")
                        if(attrs["status"] == "Check in" and regist_event.status == "Check in"):
                            print("already check in")
                            raise serializers.ValidationError(
                                {"detail": "You're already check in."})
                                

                        elif(attrs["status"] == "Check out" and regist_event.status == "Check out"):
                            print("already check out")
                            raise serializers.ValidationError(
                                {"detail": "You're already check out."})

                        else:
                            attrs["percentage"] = "%.2f" % (percentage) + "%"
                            user = User.objects.get(username=attrs['username'])
                            userimage = UserImage.objects.create(
                                user=user, imgpath=attrs['imgpath'])
                            userimage.save()
                            print("save image into device storage")
                            return attrs

                    except EventHistory.DoesNotExist:
                        attrs["percentage"] = "%.2f" % (percentage) + "%"
                        user = User.objects.get(username=attrs['username'])
                        userimage = UserImage.objects.create(
                            user=user, imgpath=attrs['imgpath'])
                        userimage.save()
                        print("save image into device storage")
                        return attrs

                    except AttributeError:
                        attrs["percentage"] = "%.2f" % (percentage) + "%"
                        user = User.objects.get(username=attrs['username'])
                        userimage = UserImage.objects.create(
                            user=user, imgpath=attrs['imgpath'])
                        userimage.save()
                        print("save image into device storage")
                        return attrs

                else:
                    os.remove("%s" % (settings.BASE_DIR)+"\\images\\" +
                        attrs['username']+"\\"+save_time+'.png')
                    print("matching below than 80% : ", percentage, "%")
                    raise serializers.ValidationError({
                        "detail": "Your identity is matching less than 80% \nyour matching :" + "%.2f" % (percentage[0]) + "%"
                    })

            else:
                os.remove("%s" % (settings.BASE_DIR)+"\\images\\" +
                          attrs['username']+"\\"+save_time+'.png')
                raise serializers.ValidationError(
                    {"detail": "didn't find any facial."})

        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "didn't find your user account."})

    def create(self, validated_data):
        user_for_check = User.objects.get(username=validated_data["username"])
        event = UserEvent.objects.get(event_name=validated_data["event_name"])

        regist_event = UserRegisterEvent.objects.get(
            event=event,
            user=user_for_check
        )

        event_history = EventHistory.objects.create(
            event=regist_event,
            status=validated_data["status"]
        )

        event_history.save()
        return event_history

    def to_representation(self, instance):
        return {"success": True}

class ApproveEventSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(max_length=255)
    approver = serializers.CharField(max_length=255)

    class Meta:
        model = EventAppovedLog
        fields = ['agreed', 'detail', 'event_name', 'approver']

    # def validate(self, attrs):
    #     event = UserEvent.objects.get(event_name=attrs["event_name"])
    #     user = User.objects.get(username=attrs["username"])

    #     try:
    #         UserRegisterEvent.objects.get(event_id=event.id, user_id=user.id)
    #         raise serializers.ValidationError(
    #             {"detail": "This account already registered"})

    #     except UserRegisterEvent.DoesNotExist:
    #         return attrs

    def create(self, validated_data):
        event = UserEvent.objects.get(event_name=validated_data["event_name"])
        user = User.objects.get(username=validated_data["approver"])

        # detail = ""

        # if (validated_data["detail"] != ""):
        #     detail = validated_data["detail"]


        eventlog = EventAppovedLog.objects.create(
            event=event,
            user=user,
            agreed=validated_data["agreed"],
            detail=validated_data["detail"],
        )
        eventlog.save()
        event.approved_by = user.username
        event.is_approved = validated_data["agreed"]
        event.save()

        return eventlog

    def to_representation(self, instance):
        return {"success": True}
