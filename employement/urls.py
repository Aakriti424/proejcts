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
    ###✅login, register###
    path('admin/', admin.site.urls),
    path('register/', Register.as_view(), name='Register'),
    path('', Login, name='Login'),

    ####✅EmployerProfile, Create Vacancy, View Application, View Vacancy, Accept Applicant, Edit and Delete Vacancy####
    path('employer/', EmployerView, name='Employer'),
    path('employerprofile/', EmployerProfileView, name='EmployerProfile'),
    path('vacancy/', VacancyView, name='Vacancy'),
    path('accept/<int:pk>', accept, name='Accept'),
    path('application/', ApplicationView, name='Application'),
    path('edit/<int:pk>', edit, name='Edit'),
    path('delete/<int:pk>', delete, name='Delete'),


    ###✅Jobseeker profile, application create, applied to, accepted, rejected ####
    path('jobseeker/<int:pk>', JobseekerView, name='Jobseeker'),
    path('jobseekerprofile/', JobseekerProfile, name='JobseekerProfile'),
    path('appliedby/', ApplicationView, name='Applied'),
    path('jobseekeraccept/', jobseekeraccept, name='jobseekeraccept' ),
    path('jobseekerreject', jobseekerreject,name='jobseekerreject')

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


