from rest_framework import serializers

from .models import Notification


class NotificationSerializer(
    serializers.ModelSerializer
):

    student_name = serializers.CharField(
        source='student.name',
        read_only=True
    )

    class Meta:

        model = Notification

        fields = [
            'id',
            'title',
            'message',
            'student',
            'student_name',
            'is_read',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'student_name',
            'created_at',
        ]