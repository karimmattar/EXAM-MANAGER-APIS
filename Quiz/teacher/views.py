# Teacher Work with Quiz view

from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from User.decorators import teacher_role
from Quiz.teacher.serializers import CreateNewQuiz, CreateMCQ, CreateQuestion, CreateTR, CreateRate
from User.models import User, Teacher, Subject, ClassRoom
from Quiz.models import Quiz
from Question.models import Question, MCQ, TR, Rate


# This view contain:
    # 1- create new quiz
    # 2- add questions to quiz
    # 3- save quiz
    # 4- launch quiz (add launch date -- add class room)
    # 5- list all questions (filters will work on this function)
    # 6- perview quiz
    # 7- list all past quizs (which has been launched)
    # 8- list all future quizes (which not launched yet)

# 1
@api_view(['POST'])
@teacher_role
def newQuiz(request):
    user = request.user
    teacher = get_object_or_404(Teacher, user=user)
    serializer = CreateNewQuiz(data=request.data)
    if serializer.is_valid():
        new_serializer = serializer.save(subject=teacher.subject.name, author=user)

        return Response(new_serializer.data)


# 2
@api_view(['POST'])
@teacher_role
def appendQuestionsToQuiz(request, quiz_id, quiz_data):
    user = request.user
    teacher = get_object_or_404(Teacher, user=user)
    myData = quiz_data.split('&')
    quiz = get_object_or_404(Quiz, quiz_id=int(quiz_id))
    for element in range (0, len(myData)):
        question = get_object_or_404(Question, question_id=int(myData[element]))
        if (not question):
            data['Error{}'.format(element)] = 'question with id({}) not found'.format(myData[element])
        quiz.quiz_questions.add(question)
        
    return Response({'response': 'success'})


# 3
@api_view(['POST'])
@teacher_role
def saveQuiz(request, quiz_id):
    user = request.user
    teacher = get_object_or_404(Teacher, user=user)
    quiz = get_object_or_404(Quiz, quiz_id=int(quiz_id))
    if quiz.quiz_author != teacher:
        return Response({'user': 'user not authorized'})
    qustions = quiz.quiz_questions.all()
    QTime = 0
    for e in qustions:
          QTime += e.question_customization_time 
    quiz.set_quiz_real_time(QTime)
    quiz.set_quiz_setion_time(QTime+5)
    quiz.save()

    return Response(CreateNewQuiz(quiz).data)
    

# 4
@api_view(['POST'])
@teacher_role
def launchQuiz(request, quiz_id, quiz_launch_time, quiz_class_room):
    user = request.user
    teacher = get_object_or_404(Teacher, user=user)
    quiz = get_object_or_404(Quiz, quiz_id=int(quiz_id))
    if quiz.quiz_author != teacher:
        return Response({'user': 'user not authorized'})
    quiz.set_quiz_is_launched(True)
    quiz.set_quiz_launch_time(quiz_launch_time)
    class_rooms = quiz_class_room.split('&')
    for room in class_rooms:
        class_room = get_object_or_404(ClassRoom, id=int(room))
        if (not class_room):
            return Response({'class_room': 'class room not exist'})
        quiz.quiz_class_room.add(class_room)
    quiz.save()

    return Response(CreateNewQuiz(quiz).data)


# 5
@api_view(['GET'])
@teacher_role
def listQuestions(request):
    user = request.user
    teacher = get_object_or_404(Teacher, user=user)
    questions = Question.objects.filter(question_subject=teacher.subject)
    questions_serializer = CreateQuestion(questions, many=True)
    Qlist = [e for e in questions]
    mcq = MCQ.objects.filter(question__in=Qlist)
    mcq_serializer = CreateMCQ(mcq, many=True)
    tr = TR.objects.filter(question__in=Qlist)
    tr_serializer = CreateTR(tr, many=True)

    return Response(
        {
            'Q': questions_serializer.data,
            'MCQ': mcq_serializer.data,
            'TR': tr_serializer.data
        }
    )


# 7
@api_view(['GET'])
@teacher_role
def listLaunchedQuiz(request):
    user = request.user
    teacher = get_object_or_404(Teacher, user=user)
    quizs = Quiz.objects.filter(quiz_author=teacher, quiz_is_launched=True)
    serializer = CreateNewQuiz(quizs, many=True)

    return Response(serializer.data)

# 8

@api_view(['GET'])
@teacher_role
def listUnLaunchedQuiz(request):
    user = request.user
    teacher = get_object_or_404(Teacher, user=user)
    quizs = Quiz.objects.filter(quiz_author=teacher, quiz_is_launched=False)
    serializer = CreateNewQuiz(quizs, many=True)

    return Response(serializer.data)


# 6
@api_view(['GET'])
@teacher_role
def detailQuiz(request, quiz_id):
    user = request.user
    teacher = get_object_or_404(Teacher, user=user)
    quiz = get_object_or_404(Quiz, quiz_id=int(quiz_id))
    serializer = CreateNewQuiz(quiz)
    questions = quiz.quiz_questions.all()
    questions_serializer = CreateQuestion(questions, many=True)
    Qlist = [e for e in questions]
    mcq = MCQ.objects.filter(question__in=Qlist)
    mcq_serializer = CreateMCQ(mcq, many=True)
    tr = TR.objects.filter(question__in=Qlist)
    tr_serializer = CreateTR(tr, many=True)

    return Response(
        {
            'quiz': serializer.data,
            'Q': questions_serializer.data,
            'mcq': mcq_serializer.data,
            'tr': tr_serializer.data
        }
    )


@api_view(['POST'])
@teacher_role
def createQuestion(request):
    user = request.user
    teacher = get_object_or_404(Teacher, user=user)
    question = CreateQuestion(data=request.data)
    mcq = CreateMCQ(data=request.data)
    if question.is_valid() and mcq.is_valid():
        q_serializer = question.save(author=user, subject=teacher.subject.name)
        mcq_serializer = mcq.save(question=q_serializer)
        return Response(
            {
                'Q': question.data,
                'MCQ': mcq.data
            }
        )
    return Response(
        {
            'Q': question.errors,
            'MCQ': mcq.errors
        }
    )


@api_view(['POST'])
@teacher_role
def createQuestion2(request):
    user = request.user
    teacher = get_object_or_404(Teacher, user=user)
    question = CreateQuestion(data=request.data)
    mcq = CreateTR(data=request.data)
    if question.is_valid() and mcq.is_valid():
        q_serializer = question.save(author=user, subject=teacher.subject.name)
        mcq_serializer = mcq.save(question=q_serializer)
        return Response(
            {
                'Q': question.data,
                'TR': mcq.data
            }
        )
    return Response(
        {
            'Q': question.errors,
            'TR': mcq.errors
        }
    )


@api_view(['POST'])
@teacher_role
def createRate(request, question_id):
    user = request.user
    teacher = get_object_or_404(Teacher, user=user)
    question = get_object_or_404(Question, question_id=question_id)
    serializer = CreateRate(data=request.data)
    if serializer.is_valid():
        new_serializer = serializer.save(question=question, author=teacher, subject=teacher.subject)

        return Response({'data': serializer.data})



@api_view(['GET'])
@teacher_role
def viewRates(request, question_id):
    user = request.user
    teacher = get_object_or_404(Teacher, user=user)
    question = get_object_or_404(Question, question_id=question_id)
    rates = Rate.objects.filter(question=question)
    serializer = CreateRate(rates, many=True)
    return Response({'data': serializer.data})


