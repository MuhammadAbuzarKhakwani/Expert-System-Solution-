from rest_framework import serializers
from . models import Quiz, Question, Option
from django.contrib.auth.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': True}
        }
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


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
    questions = QuestionSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Quiz
        fields = ['id','title', 'description', 'category', 'created_by', 'created_at','questions']




