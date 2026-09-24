
from django.urls import path

from .views import (
    FeeListCreateView,
    FeeStudentView,
    OutstandingFeeView,
    FeeNotificationView,
    FeeDetailView,
)

urlpatterns = [
    path('', FeeListCreateView.as_view(), name='fee-list-create'),

    path(
        'student/<int:student_id>/',
        FeeStudentView.as_view(),
        name='fee-student'
    ),

    path(
        'outstanding/',
        OutstandingFeeView.as_view(),
        name='outstanding-fees'
    ),

    path(
        '<int:id>/notification/',
        FeeNotificationView.as_view(),
        name='fee-notification'
    ),

    path(
        '<int:id>/',
        FeeDetailView.as_view(),
        name='fee-detail'
    ),
]

