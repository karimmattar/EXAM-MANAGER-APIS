from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from Quiz.models import Quiz, Answers
from User.models import Student, ClassRoom
from Question.models import Question, MCQ, TR
from django.utils import timezone
from django.db.models import Q
import calendar
from Quiz.teacher.serializers import CreateNewQuiz
from Quiz.student.serializers import CreateNewAnswer
from User.decorators import student_role


@api_view(['GET'])
@student_role
def listAllStudentQuizs(request):
    user = request.user
    student = get_object_or_404(Student, user=user)
    class_room = student.class_room
    past_quizs = Quiz.objects.filter(quiz_is_launched=True, quiz_launch_time__lt=timezone.now(), quiz_class_room=class_room)
    past_quizs_serializer = CreateNewQuiz(past_quizs, many=True)
    future_quizs = Quiz.objects.filter(quiz_is_launched=True, quiz_launch_time__gt=timezone.now(), quiz_class_room=class_room)
    future_quizs_serializer = CreateNewQuiz(future_quizs, many=True)

    return Response(
        {
            'past': past_quizs_serializer.data,
            'future': future_quizs_serializer.data,
        }
    )

@api_view(['POST'])
@student_role
def quizResponse(request):
    user = request.user
    student = get_object_or_404(Student, user=user)
    serializer = CreateNewAnswer(data=request.data, many=True)
    data = []
    for e in serializer:
        if e.is_valid():
            quiz = get_object_or_404(Quiz, quiz_id=e['answers_quiz'])
            question = get_object_or_404(Question, question_id=e['answers_questions'])
            questionType = None
            point = 0
            if question.question_type == 'MCQ':
                questionType = get_object_or_404(MCQ, question=question)
            else:
                questionType = get_object_or_404(TR, question=question)
            if e['answer'] == questionType.answer:
                    point = 1
            else:
                point = 0

            new_e = e.save(amswers_author=student, answers_quiz=quiz, answers_questions=question, answer_class_room=student.class_room, answer_grade=student.grade, answer_subject=quiz.quiz_subject, answers_points=point)
            data.append(e.data)
        else:
            data.append({'error': e.errors})
    return Response(data)


@api_view(['GET'])
@student_role
def getQuizReport(request, quiz_id):
    user = request.user
    student = get_object_or_404(Student, user=user)
    quiz = get_object_or_404(Quiz, quiz_id=quiz_id)
    answers = Answers.objects.filter(answers_quiz=quiz, amswers_author=student)
    serializer = CreateNewAnswer(answers, many=True)
    return Response({'data': serializer.data})



@api_view(['GET'])
@student_role
def checkQuizTime(request, quiz_id):
    quiz = Quiz.objects.get(quiz_id=quiz_id, quiz_is_launched=True)
    if not quiz:
        return Response({'error': 'quiz not exist'})
    if quiz.quiz_launch_time > timezone.now():
        return Response({'quiz': 'quiz not apened yet'})
    return Response({'quiz': 'url should be here'})