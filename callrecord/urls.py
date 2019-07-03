from django.urls import path

from . import views

urlpatterns = [
    path('start/', views.CallStartRecordView.as_view(), name='call-start-record'),
]
