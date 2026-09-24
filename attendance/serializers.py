from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source='student.name',
        read_only=True
    )

    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = [
            'student_name',
            'status_display'
        ]

    def get_status_display(self, obj):
        if obj.status:
            return "Present"

        return "Absent"

    def validate(self, data):
        student = data.get(
            'student',
            self.instance.student if self.instance else None
        )

        date = data.get(
            'date',
            self.instance.date if self.instance else None
        )

        existing_attendance = Attendance.objects.filter(
            student=student,
            date=date
        )

        if self.instance:
            existing_attendance = existing_attendance.exclude(
                id=self.instance.id
            )

        if existing_attendance.exists():
            raise serializers.ValidationError(
                "Attendance for this student on this date already exists."
            )

        return data