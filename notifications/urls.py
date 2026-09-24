from django.urls import path

from .views import (
NotificationListCreateView,
NotificationDetailView,
StudentNotificationView,
StudentNotificationReadView
)

urlpatterns = [


# =====================================================
# TEACHER
# =====================================================

path(
    '',
    NotificationListCreateView.as_view()
),

path(
    '<int:id>/',
    NotificationDetailView.as_view()
),


# =====================================================
# STUDENT
# =====================================================

path(
    'my-notifications/',
    StudentNotificationView.as_view()
),

path(
    'my-notifications/<int:id>/read/',
    StudentNotificationReadView.as_view()
),


]
