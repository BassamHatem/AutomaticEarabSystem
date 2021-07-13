from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from knox import views as knox_views


urlpatterns = [
     path('', views.UserList.as_view(), name='users'),
     path('teachers/', views.TeacherList.as_view(), name='teachers'),
     path('students/', views.StudentList.as_view(), name='students'),
     path('students/<int:id>/', views.StudentDetails.as_view(), name='student-profile'),
     path('teachers/<int:id>/', views.TeacherDetails.as_view(), name='teacher-profile'),
     path('register/student/', views.StudentRegistration.as_view(), name='student-register'),
     path('register/teacher/', views.TeacherRegistration.as_view(), name='teacher-register'),
     path('login/', views.LoginView.as_view(), name='login'),
     path('logout/', knox_views.LogoutView.as_view(), name='logout'),
     path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
     path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
     path('password-reset/', include('django_rest_passwordreset.urls', namespace='password-reset')),
]
