from rest_framework import serializers
from .models import Absence
import django.utils.timezone as timezone
import datetime


class AbsenceSerializers(serializers.ModelSerializer):
    applier = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
     )
    processor = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
     )

    class Meta:
        model = Absence
        fields = '__all__'

    def create(self, validated_data):
        # check if the request is less than one hour before the rehearsal
        time_absence = validated_data.get('time_absence')
        formate_time = datetime.datetime.strptime(time_absence, "%y-%m-%dT%H:%M:%S.083Z")
        delta = formate_time - timezone.now()
        if delta.total_seconds() <= 3600:
            raise serializers.ValidationError('Time is less than one hour')
        absence = Absence.objects.create(**validated_data)
        absence.save()
        return absence


