# this views.py for only users profiles

from User.models import User, Teacher, Student, Parent, Student, ClassRoom, Subject, HeadMaster
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from User.Profile.factfun import QuestionRank, ReviewRank, LaunchRank, ReportRank
from User.Profile.studfun import ClassRank
from User.serializers import CreateStudent, CreateTeacher, RegisterationSerializer
from User.decorators import student_role, teacher_role, headMaster_role



# teacher profile
@api_view(['GET'])
@teacher_role
def profileTeacher(request):
    user=request.user
    teacher = get_object_or_404(Teacher, user=user)
    data0 = RegisterationSerializer(user)
    data1 = CreateTeacher(teacher)
    data2 = QuestionRank(user=user.username, subject=teacher.subject.name)
    data3 = ReviewRank(user=user.username, subject=teacher.subject.name)
    data4 = LaunchRank(user=user.username, subject=teacher.subject.name)
    data5 = ReportRank(user=user.username, subject=teacher.subject.name)

    return Response({'user': data0.data,
                'teacher': data1.data,
                'questions': data2,
                'reviews': data3,
                'launchs': data4,
                'reports': data5
            }  
        )

# student profile
@api_view(['GET'])
@student_role
def profileStudent(request):
    user = request.user
    student = get_object_or_404(Student, user=user)
    data0 = RegisterationSerializer(user)
    data1 = CreateStudent(student)
    data2 = {}
    nested_data = []
    for a in student.subjects.all():
        nested_data.append(ClassRank(user=user.username, theclass=student.class_room.name, subject=a.name))

    return Response(
        {
            'user': data0.data,
            'student': data1.data,
            'ranks': nested_data
        }
    )

    
