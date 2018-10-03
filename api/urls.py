from django.urls import path
from api import views


urlpatterns = [
    path('group/', views.GroupListAPIView.as_view(), name='group-list'),
    path('group/<int:id>/element/add', views.ElementCreateAPIView.as_view(), name='create-element')
]
