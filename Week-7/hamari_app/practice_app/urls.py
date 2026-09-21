from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from .views import Quizview, QuizDetailView, Question_views, QuestionDetailView, UserRegistrationView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('auth/register/', UserRegistrationView.as_view(), name='api_register'),
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
    path('quizzes/', Quizview.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('questions/', Question_views.as_view(), name='question-list'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
]
