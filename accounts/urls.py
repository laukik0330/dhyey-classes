from django.urls import path

from .views import (
    LoginView,
    StudentDashboardView,
    StudentProfileView,
    StudentAttendanceView,
    StudentFeesView,
    
)

urlpatterns = [

    path(
        'login/',
        LoginView.as_view()
    ),

    

    path(
        'student-dashboard/',
        StudentDashboardView.as_view()
    ),

    path(
        'my-profile/',
        StudentProfileView.as_view()
    ),

    path(
        'my-attendance/',
        StudentAttendanceView.as_view()
    ),

    path(
        'my-fees/',
        StudentFeesView.as_view()
    ),
]