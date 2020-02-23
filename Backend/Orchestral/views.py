from .models import Absence, Identity
from .serializers import AbsenceSerializers, LoginSerializer, ManagerAbsenceSerializers
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_jwt.settings import api_settings
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin)
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from .service import Service
from django.contrib.auth import login
import django.utils.timezone as timezone
from django.db.models import Q
from .constants import WIND_NAME_LIST, STRINGED_NAME_LIST, PERCUSSION_NAME_LIST, WIND_UPPER_BOUND, PERCUSSION_UPPER_BOUND, STRINGED_UPPER_BOUND
import requests
import json


# Create your views here.

class AbsenceViewSet(viewsets.GenericViewSet,
                     ListModelMixin,
                     CreateModelMixin,
                     DestroyModelMixin,
                     UpdateModelMixin):
    serializer_class = AbsenceSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        identity = Identity.objects.get(current_user=self.request.user)
        return Absence.objects.filter(applier=identity)

    def create(self, request, *args, **kwargs):
        identity = Identity.objects.get(current_user=request.user)
        upper_bound = 0
        name = request.user.username
        for combo_list in [(WIND_NAME_LIST, WIND_UPPER_BOUND),  (STRINGED_NAME_LIST, STRINGED_UPPER_BOUND), (PERCUSSION_NAME_LIST, PERCUSSION_UPPER_BOUND)]:
            if name in combo_list[0]:
                upper_bound = combo_list[1]
        print(upper_bound)
        if identity.absence_times >= upper_bound:
            return Response({'msg': 'You have used up all of your chances.'}, status=status.HTTP_403_FORBIDDEN)
        Service.change_absence_time(identity, identity.absence_times + 1)
        return CreateModelMixin.create(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        identity = Identity.objects.get(current_user=request.user)
        Service.change_absence_time(identity, identity.absence_times - 1)
        return DestroyModelMixin.destroy(self, request, *args, **kwargs)


class ManagerViewSet(viewsets.GenericViewSet,
                     ListModelMixin,
                     CreateModelMixin,
                     DestroyModelMixin,
                     UpdateModelMixin, ):
    serializer_class = ManagerAbsenceSerializers
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Absence.objects.all().order_by('time_absence', 'time_apply')

    @action(methods=['GET'], detail=True)
    def present(self, request, pk=None):
        # return member present in rehearsal
        # pk: YYYY-MM-DD format
        members = Identity.objects.all()
        result = []
        for person in members:
            try:
                if Absence.objects.get(applier=person, time_absence=pk).permission:
                    result.append({
                        'name': person.name,
                        'state': 'absence'
                    })
                else:
                    result.append({
                        'name': person.name,
                        'state': 'present'
                    })
            except Absence.DoesNotExist:
                result.append({
                    'name': person.name,
                    'state': 'present'
                })
        return Response({'members': result, 'time': pk}, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def future(self, request):
        time_now = timezone.now().date()
        result = Absence.objects.filter(time_absence__gt=time_now)
        serializer = self.serializer_class(result, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def next(self, request):
        time_now = timezone.now().date()
        complete_data = Absence.objects.filter(time_absence__gt=time_now)
        next_time = complete_data[0].time_absence
        result = Absence.objects.filter(time_absence=next_time)
        serializer = self.serializer_class(result, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def history(self, request):
        time_now = timezone.now().date()
        result = Absence.objects.filter(~Q(result='Not processed yet!'), time_absence__lt=time_now)
        serializer = self.serializer_class(result, many=True)
        return Response(serializer.data)


class AccountsViewSet(viewsets.ViewSet):
    serializer_class = LoginSerializer

    @action(methods=['POST'], detail=False)
    def login(self, request):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # login user and tie identity with user
        app_id = request.POST.get('app_id')
        app_secret = request.POST.get('app_secret')
        code = request.POST.get('code')
        name = request.POST.get('name')
        """
        url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code".format(app_id, app_secret, code)
        wx_res = json.loads(requests.get(url).text)
        errcode = wx_res['errcode'] if 'errcode' in wx_res else None
        if errcode:
            return Response({'msg': 'wx_auth.code2Session:' + wx_res['errmsg']})
        open_id = wx_res['openid']
        """
        user = Service.get_or_create_user(name)
        if not user:
            return Response({'msg': 'You are not in the member list!'}, status=status.HTTP_401_UNAUTHORIZED)
        """
        if not Service.match_user_identity(name=name, wx_union_id=open_id):
            logout(request)
            return Response({'msg': "Name and wechat doesn't match!"}, status=status.HTTP_403_FORBIDDEN)
        """
        user = authenticate(username=user.username, password='20161103')
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        login(request, user)
        return Response({'msg': 'Login!', 'token': token}, status=status.HTTP_200_OK)
