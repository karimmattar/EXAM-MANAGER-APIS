from django.shortcuts import render , get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from User.decorators import teacher_role 
from User.models import Teacher ,Student , ClassRoom
from rest_framework import status
from Quiz.models import Quiz , Answers
from django.db.models import Count , Sum
from .serializers import ClassRoomSerilizer , QuizesSerilizer
# Create your views here.

#get the student data from the teacher id and subject
@api_view(['GET',])
@teacher_role
def get_student_report(request):
    student_id = request.query_params.get('student_id',None)
    start_date = request.query_params.get('start_date',None)
    end_date = request.query_params.get('end_date',None)
    user = request.user
    teacher = get_object_or_404(Teacher,user=user)
    subject = teacher.subject
    if student_id and start_date and end_date:
        student = get_object_or_404(Student , id=student_id)
        # student_answares = Answers.objects.filter(answers_author=student, answer_creation_time__gte=start_date)
        # student_quizes = Quiz.objects.filter(id__in=student_answares,quiz_author=teacher)
        
        # student_quizes_grades = Answers.objects.filter(answers_author=student,answer_subject=subject,answer_creation_time__gte=start_date).values('answers_author__id','answers_author__user__username',
        #                         'answer_subject__name','answers_quiz__id','answers_quiz__quiz_author__id','answers_points').annotate(Sum('answers_points'))
        student_quizes_grades = Answers.objects.filter(answers_author=student,answer_subject=subject,answer_creation_time__gte=start_date).values('answers_author__id','answers_author__user__username',
                                 'answer_subject__name','answers_author__class_room__name','answers_quiz__id','answers_quiz__quiz_author__id','answers_points').annotate(Sum('answers_points'))
        
        OverallGrade = student_quizes_grades.aggregate(total_score=Sum('answers_points'))
        print(OverallGrade)
        # student_degress= []
        # for degree in student_quizes_grades:
        #     print(Sum(degree.answers_points))
        
        # print(student_degress)
        # query = Answers.objects.values('answers_points').annotate(Count('answers_points'))
       
        #print(student_quizes)
        return Response({'student_data':student_quizes_grades,'OverallGrade': OverallGrade})
    else:
        return Response({'Error' : 'Data not valid'},status=status.HTTP_400_BAD_REQUEST)


# #get the teacher for class
# @api_view(['GET',])
# @teacher_role
# def get_class_report(request):
#     user = request.user
#     teacher = get_object_or_404(Teacher,user=user)
#     teacher_classes = Teacher.objects.get(id=teacher.id).class_rooms.all()


#     mylist =[]
#     for room in teacher_classes:
#         classes = {}
#         numbers = room.student_class.all().count()
#         quizes = room.quiz_class.all()
#         classes['class'] = room.name
#         classes['Students']= numbers
#         for quiz in quizes:
#             # print(quiz.quiz_id)
#             # print(quiz.quiz_creation_time)
#             # print(quiz.quiz_questions)
#             classes['quiz'] = quiz.quiz_id
#             classes['Date'] = quiz.quiz_creation_time
#             quiestions=quiz.quiz_questions.all().count()
#             classes['questions'] = quiestions
#         mylist.append(classes)
#     # print(mylist)
#     return Response(mylist)



@api_view(['GET',])
@teacher_role
def get_class_quizes(request):
    user = request.user
    teacher = get_object_or_404(Teacher,user=user)
    teacher_classes = teacher.class_rooms.all()
    # quizes = Quiz.objects.filter(id__in=teacher_classes)
    quizes = ClassRoom.objects.all()
    serializer = ClassRoomSerilizer(teacher_classes,many=True)
    # print(quizes)
    return Response(serializer.data)

@api_view(['GET',])
@teacher_role
def generate_report_class(request):
    quiz_id = request.query_params.get('quiz_id',None)
    user = request.user
    teacher = get_object_or_404(Teacher,user=user)
    if quiz:
        quiz = Quiz.objects.get(quiz_id=quiz_id)
        student_answers=quiz.quiz_answers.all()

        student_quizes_grades = Answers.objects.filter(answers_quiz=quiz).values('answers_quiz__quiz_id','answers_author__user__username',
                                    'answer_subject__name','answers_author__class_room__name','answers_points','answers_quiz__quiz_creation_time').annotate(Sum('answers_points'))

        print(student_quizes_grades)
    # serializer = AnswersSerilaizer(student_answers)
    # print(serializer.data)
        return Response({'class_data':student_quizes_grades})
    # if quiz:
    #     class_student = Answers.objects.filter(answers_quiz=1)
    #     print(class_student)
    #     return Response('working')
    else:
        return Response({'Error' : 'Data not valid'},status=status.HTTP_400_BAD_REQUEST)