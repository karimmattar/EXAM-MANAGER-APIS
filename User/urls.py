from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from User.Profile.views import profileTeacher, profileStudent
from User.AdminHeadMaster.views import ( 
        add_subject_view , subject_list_view ,subject_detail_view , 
        add_class_room_view ,class_list_view,  class_room_detail_view,
        add_teacher_view ,list_teachers_view , teacher_detail_view ,
        add_student_view , list_students_view ,student_detail_view ,
        add_parent_view , list_parents_view , parent_detail_view
        )


urlpatterns = [
    # Allow any User to register
    path('register/headmaster/', views.registration_headmaster_view, name='headmasterR'),
    path('register/teacher/', views.registration_teacher_view, name='teacherR'),
    path('register/student/', views.registration_student_view, name='studentR'),
    path('register/parent/', views.registration_parent_view, name='parentR'),

    # login pase
    path('login/', views.login_view, name='login'),

    # Profiles (teacher & Student & Parent)
    path('profile/teacher/', profileTeacher, name='profileTeacher'),
    path('profile/student/', profileStudent, name='profileStudent'),

    # Head master create Users
    path('headmaster/subject/add/',add_subject_view, name='add_subject'),
    path('headmaster/subject/list/',subject_list_view, name='subject_list'),
    path('headmaster/subject/<int:id>/',subject_detail_view, name='subject_detail'),
    path('headmaster/class/add/',add_class_room_view, name='add_class'),
    path('headmaster/class/list/',class_list_view, name='list_classes'),
    path('headmaster/class/<int:id>/',class_room_detail_view, name='class_room_detail'),
    path('headmaster/teacher/add/',add_teacher_view, name='add_teacher'),
    path('headmaster/teacher/list/',list_teachers_view, name='add_teacher'),
    path('headmaster/teacher/<int:id>/',teacher_detail_view, name='teacher_detail'),
    path('headmaster/student/add/',add_student_view, name='add_student'),
    path('headmaster/student/list/',list_students_view, name='list_student'),
    path('headmaster/student/<int:id>/',student_detail_view, name='student_detail'),
    path('headmaster/parent/add/',add_parent_view, name='add_parent'),
    path('headmaster/parent/list/',list_parents_view, name='list_parent'),
    path('headmaster/parent/<int:id>/',parent_detail_view, name='parent_detail'),
    
    # Refresh token to recreate access token
    path('xxxx-xxxx-xxxx-xxxx-xxxx/', views.refresh_token_view, name='xxxx-xxxx-xxxx-xxxx'),
]