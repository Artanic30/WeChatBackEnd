from rest_framework.response import Response
from rest_framework import status
from .models import Identity
from django.contrib.auth.models import User
from .constants import NAME_LIST
from .serializers import IdentitySerializers
from django.contrib.auth import authenticate


class Service:
    @classmethod
    def test_valid(cls, serializer):
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def match_user_identity(cls, wx_union_id, name):
        # if name and union_id match return True otherwise return False
        if Identity.objects.filter(name=name).exist():
            return Identity.objects.filter(name=name, union_id=wx_union_id).exist()
        else:
            if name in NAME_LIST:
                new_identity = IdentitySerializers(data={
                    'name': name,
                    'union_id': wx_union_id,
                    'user': name
                })
                cls.test_valid(new_identity)
                return True
            else:
                return False

    @classmethod
    def get_or_create_user(cls, name):
        if User.objects.filter(username=name).exist():
            return authenticate(username=name, password='20161103')
        else:
            if name in NAME_LIST:
                User.objects.create_user(username=name, password='20161103')
                return authenticate(username=name, password='20161103')
        return None

