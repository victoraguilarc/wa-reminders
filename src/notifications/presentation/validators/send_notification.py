# -*- coding: utf-8 -*-

from rest_framework import serializers

from src.notifications.enums import NotificationStrategy, NotificationTargetType


class NotificationTargetValidator(serializers.Serializer):
    id = serializers.UUIDField()
    type = serializers.ChoiceField(choices=NotificationTargetType.choices())


class PreNotificationValidator(serializers.Serializer):
    strategies = serializers.ListSerializer(
        child=serializers.ChoiceField(choices=NotificationStrategy.choices()),
        default=[],
    )
    subject = serializers.CharField()
    message = serializers.CharField()


class SendNotificationValidator(PreNotificationValidator):
    targets = serializers.ListSerializer(
        child=NotificationTargetValidator(),
        default=[],
    )
