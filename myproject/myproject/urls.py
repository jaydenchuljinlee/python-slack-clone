"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Jlack",
        default_version="2.0.0",
        description="Jlack Backend API Documentation.",
        contact=openapi.Contact(email="ironjin92@gmail.com"),
        license=openapi.License(name="MIT"),
    ),
    url="https://api.Jlack.ironjin.com/docs/"
    if not os.getenv("DJANGO_DEBUG")
    else "http://127.0.0.1:8000",
    public=False,
    permission_classes=[permissions.IsAuthenticated],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger_documentation",
    ),
    path("channel/", include("chat_channel.urls")),
]
