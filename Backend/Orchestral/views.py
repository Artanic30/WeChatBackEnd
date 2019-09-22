from django.shortcuts import render
from .models import Absence, Identity
from .serializers import AbsenceSerializers
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action


# Create your views here.


class AbsenceViewSet(viewsets.ViewSet):
    serializers = AbsenceSerializers

    def create(self, request):
        reason = request.POST.get('reason')
        time = request.POST.get('time')
        applier = Identity.objects.get(name=request.POST.get('name'))
        absence = self.serializers(data={
            'reason': reason,
            'applier': applier,
            'time': time
        })
        test_valid(absence)
        return Response({'msg': 'Information submitted!'}, status=status.HTTP_200_OK)

    def list(self, request):
        # todo: Apply auth system to restrict the returned info are user related
        total_info = self.serializers(Absence.objects.all(), many=True)
        return Response(total_info.data, status=status.HTTP_200_OK)


class ManagerViewSet(viewsets.ViewSet):
    serializers = AbsenceSerializers

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


def test_valid(serializer):
    if serializer.is_valid():
        serializer.save()
    else:
        Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
