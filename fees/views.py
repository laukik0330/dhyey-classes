
from django.shortcuts import get_object_or_404
from django.db.models import F

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Fee
from .serializers import FeeSerializer
from students.models import Student
from accounts.permissions import IsTeacher


class FeeListCreateView(APIView):

    permission_classes = [IsTeacher]

    def get(self, request):
        fees = Fee.objects.select_related('student').all().order_by('-id')

        serializer = FeeSerializer(
            fees,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = FeeSerializer(
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


class FeeStudentView(APIView):

    permission_classes = [IsTeacher]

    def get(self, request, student_id):

        student = get_object_or_404(
            Student,
            id=student_id
        )

        fees = Fee.objects.filter(
            student=student
        ).order_by('-id')

        serializer = FeeSerializer(
            fees,
            many=True
        )

        return Response(serializer.data)


class OutstandingFeeView(APIView):

    permission_classes = [IsTeacher]

    def get(self, request):

        fees = Fee.objects.filter(
            paid_amount__lt=F('total_amount')
        ).select_related('student').order_by('-id')

        serializer = FeeSerializer(
            fees,
            many=True
        )

        return Response(serializer.data)


class FeeNotificationView(APIView):

    permission_classes = [IsTeacher]

    def get(self, request, id):

        fee = get_object_or_404(
            Fee.objects.select_related('student'),
            id=id
        )

        remaining_amount = (
            fee.total_amount - fee.paid_amount
        )

        message = (
            f"Dhyey Classes\n\n"
            f"Dear {fee.student.parent_name},\n\n"
            f"This is a reminder regarding the pending fee "
            f"of {fee.student.name}.\n"
            f"Total Fee: ₹{fee.total_amount}\n"
            f"Paid Amount: ₹{fee.paid_amount}\n"
            f"Remaining Amount: ₹{remaining_amount}\n"
            f"Due Date: {fee.due_date}\n\n"
            f"Please pay the pending amount before the due date.\n\n"
            f"Thank you,\n"
            f"Dhyey Classes"
        )

        return Response({
            "student_name": fee.student.name,
            "parent_name": fee.student.parent_name,
            "parent_phone": fee.student.parent_phone,
            "remaining_amount": remaining_amount,
            "due_date": fee.due_date,
            "message": message
        })


class FeeDetailView(APIView):

    permission_classes = [IsTeacher]

    def get(self, request, id):

        fee = get_object_or_404(
            Fee,
            id=id
        )

        serializer = FeeSerializer(fee)

        return Response(serializer.data)

    def put(self, request, id):

        fee = get_object_or_404(
            Fee,
            id=id
        )

        serializer = FeeSerializer(
            fee,
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

        fee = get_object_or_404(
            Fee,
            id=id
        )

        serializer = FeeSerializer(
            fee,
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

        fee = get_object_or_404(
            Fee,
            id=id
        )

        fee.delete()

        return Response({
            "message": "Fee deleted successfully"
        })

