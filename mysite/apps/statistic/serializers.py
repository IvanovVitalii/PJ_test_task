from rest_framework import serializers
from .models import User, Statistic


class UsersSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    gender = serializers.CharField()
    ip_address = serializers.CharField()

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.ip_address = validated_data.get('ip_address', instance.ip_address)
        instance.save()
        return instance


class StatisticUsersSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    date = serializers.DateTimeField()
    page_views = serializers.IntegerField()
    clicks = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def create(self, validated_data):
        return Statistic.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.date = validated_data.get('date', instance.date)
        instance.page_views = validated_data.get('page_views', instance.page_views)
        instance.clicks = validated_data.get('clicks', instance.clicks)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.save()
        return instance
