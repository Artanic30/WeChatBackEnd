from rest_framework import serializers
from .models import Absence, Identity
import django.utils.timezone as timezone
import datetime
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
        if delta.total_seconds() <= 3600:
            raise serializers.ValidationError('Time is less than one hour')
        identity = Identity.objects.get(current_user=user)
        validated_data['applier'] = identity
        absence = Absence.objects.create(**validated_data)
        absence.save()
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


class LoginSerializer(serializers.Serializer):
    name = serializers.CharField()
    app_id = serializers.CharField()
    app_secret = serializers.CharField()
    code = serializers.CharField()


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

    class Meta:
        model = Absence
        fields = '__all__'
