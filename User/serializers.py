# Notes this serializer.py only for registeration

from rest_framework import serializers
from rest_framework.response import Response
from User.models import User, HeadMaster, Teacher, Student, Parent, Subject, ClassRoom
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist


#serializer for register new user
class RegisterationSerializer(serializers.ModelSerializer):
    #make confirm password write only (can not copy or past on it)
    password2 = serializers.CharField(style={'input_type' : 'password'}, write_only=True)
    phone_number = serializers.CharField(max_length=20)
    role = serializers.CharField(max_length=50)
    address = serializers.CharField(max_length=255)
    birth_date = serializers.DateField()

    class Meta:
        model = User
        fields = ['email', 'username', 'phone_number', 'role', 'address', 'birth_date', 'password', 'password2']
        extra_kwargs = {
            #make password write only (can not copy or past on it)
            'password' : {'write_only': True}
        }

    # override finction save to check if confirm password equal password
    def save(self):
        user = User(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
            phone_number = self.validated_data['phone_number'],
            role = self.validated_data['role'],
            address = self.validated_data['address'],
            birth_date = self.validated_data['birth_date']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'password must match'})
        user.set_password(password)
        user.save()
        return user

#serializer for register new head master
class CreateHeadMaster(serializers.ModelSerializer):
    class Meta:
        model = HeadMaster
        fields = ['school_name', 'educational_type', 'educational_level']


#serializer for register new teacher
class CreateTeacher(serializers.ModelSerializer):
    subject = serializers.CharField(style={'input_type' : 'text'}, max_length=100)
    class Meta:
        model = Teacher
        fields = ['uni_code', 'grade', 'level', 'subject']

    def save(self, xyz, **kwargs):
        user = get_object_or_404(User, username=xyz)
        teacher = Teacher(
            grade = self.validated_data['grade'],
            level = self.validated_data['level']
        )
        uni_code = self.validated_data['uni_code']
        subject = self.validated_data['subject']
        all_masters = HeadMaster.objects.all()
        uni_code_list = []
        
        try:
            ddm = Subject.objects.get(name=subject)
        except ObjectDoesNotExist:
            if user:
                user.delete()
            else:
                pass
            raise serializers.ValidationError({'subject': 'subject must be exist'})

        for master in all_masters:
            uni_code_list.append(master.uni_code)

        # check if new uni_code is exist in uni_code_list
        if uni_code not in uni_code_list:
            if user:
                user.delete()
            else:
                pass
            raise serializers.ValidationError({'uni_code': 'uni code must be exist'})

        teacher.set_uni_code(uni_code)
        teacher.set_user(user)
        teacher.set_subject(ddm)
        teacher.save()
        return teacher



#serializer for register new student
class CreateStudent(serializers.ModelSerializer):
    class_room = serializers.CharField(max_length=20)
    class Meta:
        model = Student
        fields = ['uni_code', 'grade', 'level', 'class_room']

    def save(self, xyz, **kwargs):
        user = get_object_or_404(User, username=xyz)
        student = Student(
            grade = self.validated_data['grade'],
            level = self.validated_data['level']
        )
        uni_code = self.validated_data['uni_code']
        class_room = self.validated_data['class_room']
        all_masters = HeadMaster.objects.all()
        uni_code_list = []

        classrom = get_object_or_404(ClassRoom, name=class_room)
        if not classrom:
            if user:
                user.delete()
            else:
                pass
            raise serializers.ValidationError({'class_room': 'class room must be exist'})

        for master in all_masters:
            uni_code_list.append(master.uni_code)

        if uni_code not in uni_code_list:
            if user:
                user.delete()
            else:
                pass
            raise serializers.ValidationError({'uni_code': 'uni code must be exist'})
        
        student.set_uni_code(uni_code)
        student.set_user(user)
        student.set_classrom(classrom)
        student.save()
        return student


#serializer for register new parent
class CreateParent(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['uni_code',]

    def save(self, xyz, **kwargs):
        user = get_object_or_404(User, username=xyz)
        uni_code = self.validated_data['uni_code']
        all_masters = HeadMaster.objects.all()
        uni_code_list = []

        for master in all_masters:
            uni_code_list.append(master.uni_code)

        if uni_code not in uni_code_list:
            if user:
                user.delete()
            else:
                pass
            raise serializers.ValidationError({'uni_code': 'uni code must be exist'})

        parent = Parent()
        parent.set_uni_code(uni_code)
        parent.set_user(user)
        parent.save()
        return parent

# serializer for parent data of student
# class ParentsData(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fileds = ['Father_Info_First_Name', 'Father_Info_Family_Name', 'Father_Info_Email', 'Father_Info_Mobile', 'Mother_Info_First_Name', 'Mother_Info_Family_Name', 'Mother_Info_Email', 'Mother_Info_Mobile']

