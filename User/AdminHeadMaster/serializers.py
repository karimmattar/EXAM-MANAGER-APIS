from rest_framework import serializers
from django.shortcuts import get_object_or_404
from drf_writable_nested.serializers import WritableNestedModelSerializer
from User.models import User, HeadMaster, Teacher, Student, Parent, Subject, ClassRoom


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'username',  'role',  'password']
        

class TeacherSerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Teacher
        fields = ('id','uni_code','grade','level' ,'user','subject','class_rooms')

class StudentSerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Student
        fields = ('id', 'uni_code', 'grade', 'level', 'class_room','subjects','user')
        read_only  = ['id']

class ParentSerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Parent
        fields = ('id', 'uni_code', 'user',)
        read_only  = ['id']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id','name','level' , 'grade',]
        read_only = ['id']

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = ['id', 'number', 'grade','level']
        read_only = ['id']