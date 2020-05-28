from rest_framework import serializers
from User.models import Teacher , Subject , Student , ClassRoom
from Quiz.models import Quiz , Answers
from django.shortcuts import get_object_or_404


class QuizesSerilizer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()

    def get_questions_count(self,obj):
        if obj:
            return obj.quiz_questions.all().count()

    class Meta:
        model = Quiz
        fields = ('quiz_id','questions_count','quiz_creation_time')



class ClassRoomSerilizer(serializers.ModelSerializer):
    quiz = QuizesSerilizer(source='quiz_class', many=True)
    student_count = serializers.SerializerMethodField()
    
    def get_student_count(self,obj):
        if obj:
            return obj.student_class.all().count()

    class Meta:
        model = ClassRoom
        fields = ('id','name','quiz','student_count')
