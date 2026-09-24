
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

from .models import Attendance
from .serializers import AttendanceSerializer
from students.models import Student
from batches.models import Batch
from accounts.permissions import IsTeacher


class AttendanceListCreateView(APIView):

    permission_classes = [IsTeacher]

    def get(self, request):

        batch_id = request.query_params.get('batch')
        date = request.query_params.get('date')

        attendance = Attendance.objects.all().select_related('student')

        if batch_id:
            attendance = attendance.filter(
                student__batch_id=batch_id
            )

        if date:
            attendance = attendance.filter(
                date=date
            )

        attendance = attendance.order_by('student__name')

        serializer = AttendanceSerializer(
            attendance,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = AttendanceSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class BatchAttendanceView(APIView):

    permission_classes = [IsTeacher]

    def get(self, request, batch_id):

        batch = get_object_or_404(
            Batch,
            id=batch_id
        )

        date = request.query_params.get('date')

        if not date:
            return Response(
                {
                    "detail": "Date is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        students = Student.objects.filter(
            batch=batch
        ).order_by('name')

        result = []

        for student in students:

            attendance = Attendance.objects.filter(
                student=student,
                date=date
            ).first()

            result.append({
                "student_id": student.id,
                "student_name": student.name,
                "phone": student.phone,
                "attendance_id": attendance.id if attendance else None,
                "status": attendance.status if attendance else False
            })

        return Response({
            "batch_id": batch.id,
            "batch_name": batch.name,
            "date": date,
            "students": result
        })


class SaveBatchAttendanceView(APIView):

    permission_classes = [IsTeacher]

    def post(self, request):

        batch_id = request.data.get('batch_id')
        date = request.data.get('date')
        records = request.data.get('records', [])

        if not batch_id:
            return Response(
                {"detail": "batch_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not date:
            return Response(
                {"detail": "date is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not isinstance(records, list):
            return Response(
                {"detail": "records must be a list."},
                status=status.HTTP_400_BAD_REQUEST
            )

        batch = get_object_or_404(
            Batch,
            id=batch_id
        )

        batch_students = Student.objects.filter(
            batch=batch
        )

        batch_student_ids = set(
            batch_students.values_list('id', flat=True)
        )

        saved_records = []

        for record in records:

            student_id = record.get('student_id')
            student_status = record.get('status', False)

            if student_id not in batch_student_ids:
                return Response(
                    {
                        "detail": (
                            f"Student {student_id} "
                            "does not belong to this batch."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            attendance, created = Attendance.objects.update_or_create(
                student_id=student_id,
                date=date,
                defaults={
                    "status": bool(student_status)
                }
            )

            saved_records.append(attendance)

        serializer = AttendanceSerializer(
            saved_records,
            many=True
        )

        return Response(
            {
                "message": "Attendance saved successfully.",
                "batch_id": batch.id,
                "batch_name": batch.name,
                "date": date,
                "records": serializer.data
            },
            status=status.HTTP_200_OK
        )


class StudentAttendanceView(APIView):

    permission_classes = [IsTeacher]

    def get(self, request, student_id):

        student = get_object_or_404(
            Student,
            id=student_id
        )

        attendance = Attendance.objects.filter(
            student=student
        ).order_by('-date')

        serializer = AttendanceSerializer(
            attendance,
            many=True
        )

        return Response(serializer.data)


class AttendanceDetailView(APIView):

    permission_classes = [IsTeacher]

    def get(self, request, id):

        attendance = get_object_or_404(
            Attendance,
            id=id
        )

        serializer = AttendanceSerializer(
            attendance
        )

        return Response(serializer.data)

    def put(self, request, id):

        attendance = get_object_or_404(
            Attendance,
            id=id
        )

        serializer = AttendanceSerializer(
            attendance,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, id):

        attendance = get_object_or_404(
            Attendance,
            id=id
        )

        serializer = AttendanceSerializer(
            attendance,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, id):

        attendance = get_object_or_404(
            Attendance,
            id=id
        )

        attendance.delete()

        return Response({
            "message": "Attendance deleted successfully"
        })

