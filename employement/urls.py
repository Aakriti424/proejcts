"""
URL configuration for employement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from base.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', Register.as_view(), name='Register'),
    path('', Login, name='Login'),
    path('employer/', EmployerView, name='Employer'),
    path('employerprofile/', EmployerProfileView, name='EmployerProfile'),
    path('vacancy/', VacancyView, name='Vacancy'),
    path('jobseeker/<int:pk>', JobseekerView, name='Jobseeker'),
    path('jobseekerprofile/', JobseekerProfile, name='JobseekerProfile'),
    path('application/', ApplicationView, name='Application'),
    path('appliedby/', ApplicationView, name='Applied'),
    path('accept/<int:pk>', accept, name='Accept')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


