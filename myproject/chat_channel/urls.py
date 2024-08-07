from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# router.register(r'channels', views.ChannelViewSet)

urlpatterns = [
    path('<str:workspace__hashed_value>/', views.ChatChannelView.as_view()),
]
