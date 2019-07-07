from django.urls import path

from . import views

urlpatterns = [
    path('<str:phone>/', views.TelephoneBillView.as_view(),
         name='telephone-bill'),
]
