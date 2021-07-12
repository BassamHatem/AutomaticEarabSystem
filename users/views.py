from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from rest_framework import generics, mixins, status, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import Student, Teacher
from .serializers import UserSerializer, UserDetailsSerializer, StudentSerializer, TeacherSerializer, ChangePasswordSerializer
from .models import User
from .permissions import UpdateProfile
from django.urls import reverse
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView


# Create your views here.
class UserList(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('full_name', 'email',)

    def get(self, request):
        return self.list(request)


class UserDetails(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = (UpdateProfile,)
    lookup_field = 'id'

    def get(self, request, id):
        return self.retrieve(request, id=id)

    def put(self, request, id):
        return self.update(request, id=id)

    def delete(self, request, id):
        return self.destroy(request, id=id)


class StudentList(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request):
        return self.list(request)


class TeacherList(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get(self, request):
        return self.list(request)


class RegistrationView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['password'] = make_password(password=serializer.validated_data['password'])
        user = serializer.save()
        user = User.objects.get(email=serializer.validated_data['email'])
        
        # _mutable = data._mutable
        # data._mutable = True
        
        data['user'] = user.id
        # data._mutable = _mutable
        
        is_teacher = request.data.get('is_teacher', False)
        serializer = StudentSerializer(data=data) if not is_teacher else TeacherSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None) 


class ChangePasswordView(generics.UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
