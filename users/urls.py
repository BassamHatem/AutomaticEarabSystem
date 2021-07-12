from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from knox import views as knox_views


urlpatterns = [
     path('', views.UserList.as_view(), name='users'),
     path('teachers/', views.TeacherList.as_view(), name='teachers'),
     path('students/', views.StudentList.as_view(), name='students'),
     path('register/', views.RegistrationView.as_view(), name='register'),
     # path('email-verify/', views.VerifyEmail.as_view(), name='email-verify'),
     path('login/', views.LoginView.as_view(), name='login'),
     path('logout/', knox_views.LogoutView.as_view(), name='logout'),
     path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
     path('<int:id>/', views.UserDetails.as_view(), name='user-profile'),
     path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
     path('password-reset/', include('django_rest_passwordreset.urls', namespace='password-reset')),
]
