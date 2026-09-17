from django.urls import path
from .views import Quizview,QuizDetailView,Question_views,QuestionDetailView

urlpatterns = [
    path('quizzes/', Quizview.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('questions/', Question_views.as_view(), name='question-list'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
]
