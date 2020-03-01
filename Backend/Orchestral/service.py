from rest_framework.response import Response
from rest_framework import status
from .models import Identity
from django.contrib.auth.models import User
from .constants import NAME_LIST
from django.contrib.auth import authenticate, login
from .constants import WIND_NAME_LIST, STRINGED_NAME_LIST, PERCUSSION_NAME_LIST, WIND_UPPER_BOUND, STRINGED_UPPER_BOUND, PERCUSSION_UPPER_BOUND, ADMIN_EMAILS
from django.core.mail import send_mail


class Service:
    @classmethod
    def test_valid(cls, serializer):
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def match_user_identity(cls, wx_union_id, name):
        from .serializers import IdentitySerializers
        if name not in NAME_LIST:
            return False
        # if name and union_id match return True otherwise return False
        identity = None
        if len(Identity.objects.filter(name=name)) != 0:
            identity = Identity.objects.get(name=name)
        mem_type = cls.define_member_type(name)
        if identity:
            if identity.union_id:
                pass
            else:
                complete_identity = IdentitySerializers(identity, data={
                        'union_id': wx_union_id,
                    }, partial=True)
                cls.test_valid(complete_identity)
        else:
            new_identity = IdentitySerializers(data={
                'name': name,
                'union_id': wx_union_id,
                'current_user': name,
                'absence_times': 0,
                'type': mem_type
            })
            cls.test_valid(new_identity)
            authenticate(username=name, password='20161103')
        return True

    @classmethod
    def get_or_create_user(cls, name):
        if name and len(User.objects.filter(username=name)) != 0:
            return User.objects.get(username=name)
        elif name in NAME_LIST:
            user = User.objects.create_user(username=name, password='20161103')
            return user
        return None

    @classmethod
    def change_absence_time(cls, identity, times):
        from .serializers import IdentitySerializers
        updated_identity = IdentitySerializers(identity, data={
            'absence_times': times
        }, partial=True)
        cls.test_valid(updated_identity)

    @classmethod
    def define_member_type(cls, name):
        mem_type = 'S'
        for key, name_list in {'W': WIND_NAME_LIST, 'S': STRINGED_NAME_LIST, 'P': PERCUSSION_NAME_LIST}.items():
            if name in name_list:
                mem_type = key
        return mem_type

    @classmethod
    def get_upper_bound(cls, mem_type):
        if mem_type == 'S':
            return STRINGED_UPPER_BOUND
        elif mem_type == 'W':
            return WIND_UPPER_BOUND
        return PERCUSSION_UPPER_BOUND

    @classmethod
    def send_email(cls, name, time, reason):
        if ADMIN_EMAILS:
            send_mail('有人请假了啊啊啊啊啊',
                      '{}在{}请假了, 理由是{},请在小程序或服务器处理.'.format(name, time, reason)
                      , 'qiulongtian@skdgxlq.onexmail.com',
                      ADMIN_EMAILS, fail_silently=False)
