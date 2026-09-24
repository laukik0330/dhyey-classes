from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Student
from accounts.models import Profile


class StudentSerializer(serializers.ModelSerializer):

    batch_name = serializers.CharField(
        source='batch.name',
        read_only=True
    )

    class Meta:
        model = Student

        fields = [
            'id',
            'name',
            'email',
            'phone',
            'parent_name',
            'parent_phone',
            'batch',
            'batch_name',
            'profile_image',
        ]

        read_only_fields = [
            'id',
            'batch_name',
        ]


# =========================================================
# CREATE STUDENT ACCOUNT
# =========================================================

class StudentAccountSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15)
    parent_name = serializers.CharField(max_length=100)
    parent_phone = serializers.CharField(max_length=15)

    batch = serializers.IntegerField(
        required=False,
        allow_null=True
    )

    username = serializers.CharField(
        max_length=150
    )

    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    def validate_username(self, value):

        if User.objects.filter(
            username=value
        ).exists():

            raise serializers.ValidationError(
                "This username already exists."
            )

        return value

    def validate_email(self, value):

        if Student.objects.filter(
            email=value
        ).exists():

            raise serializers.ValidationError(
                "A student with this email already exists."
            )

        return value