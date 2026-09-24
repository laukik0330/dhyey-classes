from django.urls import path

from .views import (
    StudentListCreateView,
    StudentDetailView,
    StudentAccountCreateView
)

urlpatterns = [

    path(
        '',
        StudentListCreateView.as_view()
    ),

    path(
        '<int:id>/',
        StudentDetailView.as_view()
    ),

    path(
        'create-account/',
        StudentAccountCreateView.as_view()
    ),
]