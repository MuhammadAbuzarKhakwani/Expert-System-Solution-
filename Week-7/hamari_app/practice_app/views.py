from django.shortcuts import render
from .serializers import QuizSerializer, QuestionSerializer, OptionSerializer, UserRegistrationSerializer
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Quiz, Question, Option
from .permissions import IsQuizCreator

# Frontend View
def index(request):
    return render(request, 'index.html')

# Create your views here.

class UserRegistrationView(generics.CreateAPIView):
    """
    Register a new user and return their auth token.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create token for the new user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': serializer.data,
            'token': token.key,
            'message': 'User registered successfully!'
        }, status=status.HTTP_201_CREATED)


class Quizview(generics.ListCreateAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users see only their own quizzes
        return Quiz.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the creator to the current user
        serializer.save(created_by=self.request.user)


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated, IsQuizCreator]


class Question_views(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]



    