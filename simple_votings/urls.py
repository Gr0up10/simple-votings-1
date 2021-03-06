"""simple_votings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from main import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('new_voting/', views.new_voting, name='new_voting'),
    path('new_report/', views.new_report, name='new_report'),
    path('vote/', views.vote, name='vote'),
    path('element/<str:name>', views.element, name='element'),
    path('login/', views.login_req, name='login'),
    path('register/', views.register_req, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
                  path('profile/', views.profile_page, {'content_type': 0}, name='profile'),
    path('profile/liked/', views.profile_page, {'content_type': 1}),
    path('profile/reports/', views.profile_page, {'content_type': 2}),
    path('leavelike/', views.like, name="like"),
    path('change_language/', views.change_language)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
