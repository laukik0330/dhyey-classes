from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Profile
from .serializers import StudentProfileSerializer

from attendance.models import Attendance
from fees.models import Fee


class LoginView(APIView):

    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:

            return Response(
                {
                    "error": "Username and password are required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:

            return Response(
                {
                    "error": "Invalid username or password."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:

            profile = Profile.objects.get(
                user=user
            )

        except Profile.DoesNotExist:

            return Response(
                {
                    "error": "User profile not found."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        token, created = Token.objects.get_or_create(
            user=user
        )

        return Response({

            "message": "Login successful.",

            "token": token.key,

            "username": user.username,

            "role": profile.role

        })


# =========================================================
# HELPER
# =========================================================

def get_student_for_user(request):

    try:

        profile = Profile.objects.get(
            user=request.user
        )

    except Profile.DoesNotExist:

        return None

    if profile.role != 'student':

        return None

    return profile.student


# =========================================================
# STUDENT DASHBOARD
# =========================================================

class StudentDashboardView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        student = get_student_for_user(request)

        if not student:

            return Response(
                {
                    "error": "Student account not found."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        attendance = Attendance.objects.filter(
            student=student
        ).order_by('-date')

        total_attendance = attendance.count()

        present_count = attendance.filter(
            status=True
        ).count()

        absent_count = attendance.filter(
            status=False
        ).count()

        recent_attendance = []

        for record in attendance[:5]:

            recent_attendance.append({

                "id": record.id,

                "date": record.date,

                "status": record.status,

                "status_display":
                    "Present"
                    if record.status
                    else "Absent"

            })

        fees = Fee.objects.filter(
            student=student
        )

        total_fee = sum(
            fee.total_amount
            for fee in fees
        )

        paid_fee = sum(
            fee.paid_amount
            for fee in fees
        )

        remaining_fee = (
            total_fee - paid_fee
        )

        if paid_fee == 0:

            payment_status = "Pending"

        elif paid_fee >= total_fee:

            payment_status = "Paid"

        else:

            payment_status = "Partially Paid"

        profile_image = None

        if student.profile_image:

            profile_image = request.build_absolute_uri(
                student.profile_image.url
            )

        return Response({

            "student": {

                "id": student.id,

                "name": student.name,

                "email": student.email,

                "phone": student.phone,

                "parent_name": student.parent_name,

                "parent_phone": student.parent_phone,

                "profile_image": profile_image

            },

            "attendance": {

                "total": total_attendance,

                "present": present_count,

                "absent": absent_count,

                "recent": recent_attendance

            },

            "fees": {

                "total": total_fee,

                "paid": paid_fee,

                "remaining": remaining_fee,

                "payment_status": payment_status

            }

        })


# =========================================================
# STUDENT PROFILE
# =========================================================

class StudentProfileView(APIView):

    permission_classes = [IsAuthenticated]

    parser_classes = [
        MultiPartParser,
        FormParser
    ]

    def get(self, request):

        student = get_student_for_user(request)

        if not student:

            return Response(
                {
                    "error": "Student account not found."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = StudentProfileSerializer(
            student,
            context={
                'request': request
            }
        )

        return Response(
            serializer.data
        )

    def patch(self, request):

        student = get_student_for_user(request)

        if not student:

            return Response(
                {
                    "error": "Student account not found."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = StudentProfileSerializer(
            student,
            data=request.data,
            partial=True,
            context={
                'request': request
            }
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# =========================================================
# STUDENT ATTENDANCE
# =========================================================

class StudentAttendanceView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        student = get_student_for_user(request)

        if not student:

            return Response(
                {
                    "error": "Student account not found."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        attendance = Attendance.objects.filter(
            student=student
        ).order_by('-date')

        data = []

        for record in attendance:

            data.append({

                "id": record.id,

                "date": record.date,

                "status": record.status,

                "status_display":
                    "Present"
                    if record.status
                    else "Absent"

            })

        return Response(data)


# =========================================================
# STUDENT FEES
# =========================================================

class StudentFeesView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        student = get_student_for_user(request)

        if not student:

            return Response(
                {
                    "error": "Student account not found."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        fees = Fee.objects.filter(
            student=student
        ).order_by('-due_date')

        data = []

        for fee in fees:

            remaining = (
                fee.total_amount -
                fee.paid_amount
            )

            if fee.paid_amount == 0:

                payment_status = "Pending"

            elif fee.paid_amount >= fee.total_amount:

                payment_status = "Paid"

            else:

                payment_status = "Partially Paid"

            data.append({

                "id": fee.id,

                "total_amount":
                    fee.total_amount,

                "paid_amount":
                    fee.paid_amount,

                "remaining_amount":
                    remaining,

                "due_date":
                    fee.due_date,

                "payment_status":
                    payment_status

            })

        return Response(data)