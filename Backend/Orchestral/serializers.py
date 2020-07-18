from rest_framework import serializers
from .models import Absence, Identity
import django.utils.timezone as timezone
import datetime
from .service import Service
from django.contrib.auth.models import User


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
    result = serializers.CharField(
        read_only=True
    )
    permission = serializers.BooleanField(
        read_only=True
    )

    class Meta:
        model = Absence
        fields = '__all__'

    def create(self, validated_data):
        # check if the request is less than one hour before the rehearsal
        time_absence = validated_data.get('time_absence')
        user = self.context.get('request').user
        if not user.is_authenticated:
            raise serializers.ValidationError('You need to login first')
        delta = time_absence - timezone.now().date()

        identity = Identity.objects.get(current_user=user)
        if delta.total_seconds() <= 3600:
            # before call create function, absence time is added to current identity,
            # however, error is caught later here so we need to deduct absence time here.
            Service.change_absence_time(identity, identity.absence_times - 1)
            raise serializers.ValidationError('Time is less than one hour')

        validated_data['applier'] = identity
        absence = Absence.objects.create(**validated_data)
        return absence


class IdentitySerializers(serializers.ModelSerializer):
    current_user = serializers.SlugRelatedField(
        many=False,
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Identity
        fields = '__all__'


class ManagerAbsenceSerializers(serializers.ModelSerializer):
    applier = serializers.SlugRelatedField(
        many=False,
        slug_field='name',
        read_only=True
    )
    processor = serializers.SlugRelatedField(
        many=False,
        slug_field='name',
        queryset=Identity.objects.all()
    )
    reason = serializers.CharField(
        read_only=True
    )
    time_absence = serializers.TimeField(
        read_only=True
    )
    type = serializers.CharField(
        read_only=True
    )

    class Meta:
        model = Absence
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    name = serializers.CharField()
    app_id = serializers.CharField()
    app_secret = serializers.CharField()
    code = serializers.CharField()
