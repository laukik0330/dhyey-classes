from rest_framework import serializers
from .models import Fee


class FeeSerializer(serializers.ModelSerializer):

    student_name = serializers.CharField(
        source='student.name',
        read_only=True
    )

    remaining_amount = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()

    class Meta:
        model = Fee
        fields = [
            'id',
            'student',
            'student_name',
            'total_amount',
            'paid_amount',
            'due_date',
            'remaining_amount',
            'payment_status',
        ]

        read_only_fields = [
            'id',
            'student_name',
            'remaining_amount',
            'payment_status',
        ]

    def get_remaining_amount(self, obj):
        return obj.total_amount - obj.paid_amount

    def get_payment_status(self, obj):
        if obj.paid_amount == 0:
            return "Pending"

        if obj.paid_amount == obj.total_amount:
            return "Paid"

        return "Partially Paid"

    def validate_total_amount(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Total amount cannot be negative."
            )

        return value

    def validate_paid_amount(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Paid amount cannot be negative."
            )

        return value

    def validate(self, data):

        total_amount = data.get(
            'total_amount',
            self.instance.total_amount if self.instance else None
        )

        paid_amount = data.get(
            'paid_amount',
            self.instance.paid_amount if self.instance else None
        )

        if paid_amount > total_amount:
            raise serializers.ValidationError(
                "Paid amount cannot be greater than total amount."
            )

        return data