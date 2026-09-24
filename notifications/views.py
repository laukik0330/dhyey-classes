from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer

from accounts.permissions import IsTeacher
from accounts.models import Profile


# =========================================================
# TEACHER NOTIFICATIONS
# =========================================================

class NotificationListCreateView(APIView):

    permission_classes = [IsTeacher]

    def get(self, request):

        notifications = Notification.objects.all().order_by(
            '-created_at'
        )

        serializer = NotificationSerializer(
            notifications,
            many=True
        )

        return Response(
            serializer.data
        )

    def post(self, request):

        serializer = NotificationSerializer(
            data=request.data
        )

        if serializer.is_valid():

            notification = serializer.save(
                created_by=request.user
            )

            return Response(
                NotificationSerializer(
                    notification
                ).data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )


# =========================================================
# TEACHER DELETE
# =========================================================

class NotificationDetailView(APIView):

    permission_classes = [IsTeacher]

    def delete(self, request, id):

        try:

            notification = Notification.objects.get(
                id=id
            )

        except Notification.DoesNotExist:

            return Response(
                {
                    "error": "Notification not found."
                },
                status=404
            )

        notification.delete()

        return Response(
            {
                "message":
                    "Notification deleted successfully."
            }
        )


# =========================================================
# STUDENT NOTIFICATIONS
# =========================================================

class StudentNotificationView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:

            profile = Profile.objects.get(
                user=request.user
            )

        except Profile.DoesNotExist:

            return Response(
                {
                    "error": "Profile not found."
                },
                status=403
            )

        if profile.role != 'student':

            return Response(
                {
                    "error":
                        "Only students can access this API."
                },
                status=403
            )

        if not profile.student:

            return Response(
                {
                    "error":
                        "No student is linked to this account."
                },
                status=404
            )

        student = profile.student

        notifications = Notification.objects.filter(
            student=student
        ) | Notification.objects.filter(
            student__isnull=True
        )

        notifications = notifications.order_by(
            '-created_at'
        )

        serializer = NotificationSerializer(
            notifications,
            many=True
        )

        return Response(
            serializer.data
        )


# =========================================================
# MARK AS READ
# =========================================================

class StudentNotificationReadView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, id):

        try:

            profile = Profile.objects.get(
                user=request.user
            )

        except Profile.DoesNotExist:

            return Response(
                {"error": "Profile not found."},
                status=403
            )

        if profile.role != 'student' or not profile.student:

            return Response(
                {"error": "Student access required."},
                status=403
            )

        try:

            notification = Notification.objects.get(
                id=id
            )

        except Notification.DoesNotExist:

            return Response(
                {"error": "Notification not found."},
                status=404
            )

        # Student can only mark:
        # their own notification OR a global notification

        if (
            notification.student is not None
            and notification.student != profile.student
        ):

            return Response(
                {"error": "Access denied."},
                status=403
            )

        notification.is_read = True

        notification.save(
            update_fields=['is_read']
        )

        return Response(
            {
                "message":
                    "Notification marked as read."
            }
        )