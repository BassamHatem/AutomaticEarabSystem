import tensorflow as tf
from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.db import models
from rest_framework import generics, mixins, status
from rest_framework.fields import DateTimeField
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from API.models import Sentence, Student, Teacher
from API.serializers import SentenceSerializer, NewSentenceSerializer
from AutomaticEarabSystem import settings
from .constants import SIMILARITY_SCORE_THRESHOLD
from django.forms.models import model_to_dict
from tensorflow import keras
from .utilities import predict


# Create your views here.
class SentenceList(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer

    def get(self, request):
        return self.list(request)


'''
class SentenceCreate(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = NewSentenceSerializer

    def post(self, request):
        return self.create(request)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
'''


class SentenceDetails(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer
    lookup_field = 'id'

    def get(self, request, id):
        return self.retrieve(request, id=id)

    def put(self, request, id):
        return self.update(request, id=id)

    def delete(self, request, id):
        return self.destroy(request, id=id)

    # def perform_update(self, serializer):
    #    serializer.save(author=self.request.user)


class DiacritizationView(generics.GenericAPIView):
    serializer_class = NewSentenceSerializer

    def post(self, request):
        data=request.data
        data['author'] = Student.objects.get(user=self.request.user).id
        serializer = SentenceSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        DNN_input = serializer.validated_data['raw']
        model = keras.models.load_model('Encoder.sav')
        '''
        DNN_output1 = "DIACRITIZED SENTENCE"
        DNN_output2 = "DIACRITIZED SENTENCE"
        DNN_output3 = "DIACRITIZED SENTENCE"
        if DNN_output2 == DNN_output1:
            serializer.validated_data['diacritized'] = DNN_output1
        elif DNN_output3 == DNN_output1:
            serializer.validated_data['diacritized'] = DNN_output1
        elif DNN_output3 == DNN_output2:
            serializer.validated_data['diacritized'] = DNN_output2
        elif DNN_output2 == DNN_output3:
            serializer.validated_data['diacritized'] = DNN_output2
        else:
            # serializer.validated_data['diacritized'] = {DNN_output1, DNN_output2, DNN_output3}
            serializer.save()
            return Response({"Success": "Your request is pending, you will be notified when it is done."}, status=status.HTTP_201_CREATED)
        serializer.save()
        return Response(serializer.validated_data['diacritized'], status=status.HTTP_201_CREATED)
        '''
        DNN_output = predict(DNN_input, model)
        serializer.validated_data['diacritized'] = DNN_output
        serializer.save()
        return Response(serializer.validated_data['diacritized'], status=status.HTTP_201_CREATED)
