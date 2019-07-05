from django.urls import path

from . import views

urlpatterns = [
    path('start/', views.CallStartRecordView.as_view(),
         name='call-start-record'),
    path('end/', views.CallEndRecordView.as_view(),
         name='call-end-record'),
]
