from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FundingEvent, Categorization, Profile, Application


class FundingEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundingEvent
        fields = '_all_'


class CategorizationSerializer(serializers.ModelSerializer):
    event = FundingEventSerializer(read_only=True)

    class Meta:
        model = Categorization
        fields = '_all_'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = '_all_'


class ApplicationSerializer(serializers.ModelSerializer):
    event = FundingEventSerializer(read_only=True)
    applicant = UserSerializer(read_only=True)

    class Meta:
        model = Application
        fields = '_all_'