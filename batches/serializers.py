from rest_framework import serializers
from .models import Batch


class BatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Batch
        fields = [
            'id',
            'name',
            'description',
            'start_time',
            'end_time',
            'created_at'
        ]