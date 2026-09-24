from django.contrib.auth.models import User
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Student
from .serializers import (
    StudentSerializer,
    StudentAccountSerializer
)

from accounts.models import Profile
from accounts.permissions import IsTeacher

# =========================================================
# CREATE STUDENT + LOGIN ACCOUNT
# =========================================================

class StudentAccountCreateView(APIView):

    permission_classes = [IsTeacher]

    @transaction.atomic
    def post(self, request):

        serializer = StudentAccountSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data

        try:

            # -----------------------------------------
            # Create Student
            # -----------------------------------------

            student = Student.objects.create(
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                parent_name=data['parent_name'],
                parent_phone=data['parent_phone'],
                batch_id=data.get('batch')
            )

            # -----------------------------------------
            # Create Django User
            # -----------------------------------------

            user = User.objects.create_user(
                username=data['username'],
                password=data['password'],
                email=data['email']
            )

            # -----------------------------------------
            # Create Student Profile
            # -----------------------------------------

            Profile.objects.create(
                user=user,
                role='student',
                student=student
            )

            return Response(
                {
                    "message": "Student account created successfully.",

                    "student": {
                        "id": student.id,
                        "name": student.name,
                        "username": user.username
                    }
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as error:

            return Response(
                {
                    "error": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class StudentListCreateView(APIView):

    permission_classes = [IsTeacher]

    def get(self, request):
        students = Student.objects.all()

        serializer = StudentSerializer(
            students,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=400
        )


class StudentDetailView(APIView):

    permission_classes = [IsTeacher]

    def get(self, request, id):

        student = get_object_or_404(
            Student,
            id=id
        )

        serializer = StudentSerializer(
            student
        )

        return Response(
            serializer.data
        )

    def put(self, request, id):

        student = get_object_or_404(
            Student,
            id=id
        )

        serializer = StudentSerializer(
            student,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=400
        )

    def delete(self, request, id):

        student = get_object_or_404(
            Student,
            id=id
        )

        student.delete()

        return Response({
            "message": "Student deleted successfully"
        })