from django.urls import path
from . import views


urlpatterns = [
    
    path('login/', views.login_view, name='login'),
    path("logout/", views.logout_view, name="logout"),
    path('dashboard/<str:reference_no>/', views.dashboard, name='dashboard'),
    path('manage_consultations', views.manage_consultations, name='manage_consultations'),
    path('sentiment/<str:reference_no>/', views.sentiment_analysis, name='sentiment'),
    path('word-cloud/<str:reference_no>/', views.word_cloud, name='word_cloud'),
    path('summaries/<str:reference_no>/', views.summaries, name='summaries'),
    path('analysis/<str:reference_no>/', views.analysis, name='analysis'),
]