from django.urls import path, include
from .views import SentenceList, SentenceDetails, DiacritizationView
urlpatterns = [
    path('accounts/', include('users.urls')),
    path('sentences/', SentenceList.as_view()),
    path('sentences/new/', DiacritizationView.as_view()),
    path('sentences/<int:id>/', SentenceDetails.as_view()),
]
