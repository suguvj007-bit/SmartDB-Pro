from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('records/', views.records, name='records'),
    path('add-record/', views.add_record, name='add-record'),
    path('delete-record/<str:record_id>/', views.delete_record, name='delete_record'),
    path('search/', views.search_record, name='search'),
    path('analytics/', views.analytics, name='analytics'),
    path('edit-record/<str:record_id>/', views.edit_record, name='edit_record'),
    path('activity-logs/', views.activity_logs, name='activity_logs'),
]