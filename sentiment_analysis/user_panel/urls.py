from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("consultation/<str:reference_no>/", views.consultation_detail, name="consultation_detail"),
]
