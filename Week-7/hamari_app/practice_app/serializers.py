from rest_framework import serializers
from . models import Quiz, Question,Option

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id','question','text','is_correct']



class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only = True)
    class Meta:
        model = Question
        fields = ['id','quiz','text','options']
        

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only = True)
    class Meta:
        model = Quiz
        fields = ['id','title', 'description', 'category', 'created_by', 'created_at','questions']
        


