from django.urls import path
from . import views

urlpatterns = [
    path('get_student_report/',views.get_student_report,name='get_student_report'),
    path('get_class_report/',views.get_class_quizes,name='get_class_report'),
    path('generate_report_class/',views.generate_report_class, name='generate_report_class'),
]