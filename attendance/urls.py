
from django.urls import path

from .views import (
    AttendanceListCreateView,
    StudentAttendanceView,
    AttendanceDetailView,
    BatchAttendanceView,
    SaveBatchAttendanceView,
)

urlpatterns = [

    # All attendance
    path(
        '',
        AttendanceListCreateView.as_view()
    ),

    # Get attendance for students of a particular batch/date
    path(
        'batch/<int:batch_id>/',
        BatchAttendanceView.as_view()
    ),

    # Save/update attendance for a whole batch
    path(
        'batch/save/',
        SaveBatchAttendanceView.as_view()
    ),

    # Student attendance history
    path(
        'student/<int:student_id>/',
        StudentAttendanceView.as_view()
    ),

    # Single attendance record
    path(
        '<int:id>/',
        AttendanceDetailView.as_view()
    ),
]

