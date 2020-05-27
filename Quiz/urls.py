from django.urls import path
from Quiz.student.views import listAllStudentQuizs, quizResponse, checkQuizTime
from Quiz.teacher.views import newQuiz, appendQuestionsToQuiz, listQuestions, saveQuiz, launchQuiz, listLaunchedQuiz, listUnLaunchedQuiz, detailQuiz, createQuestion, createQuestion2, createRate, viewRates


urlpatterns = [
    path('quiz/student/quiz/list/', listAllStudentQuizs, name='quizStudentList'),
    path('quiz/student/quiz/checktime/<int:quiz_id>', checkQuizTime, name='checktime'),
    path('quiz/student/quiz/start/', quizResponse, name='quizstart'),
    # 
    path('quiz/teacher/create/', newQuiz, name='quizTeacherCreate'),
    path('quiz/teacher/questions/list/', listQuestions, name='QuestionsList'),
    path('quiz/teacher/append/<int:quiz_id>/<str:quiz_data>/', appendQuestionsToQuiz, name='quizTeacherAppend'),
    path('quiz/teacher/save/<int:quiz_id>/', saveQuiz, name='quizTeacherSave'),
    path('quiz/teacher/launch/<int:quiz_id>/<str:quiz_launch_time>/<str:quiz_class_room>/', launchQuiz, name='quizTeacherLaunch'),
    path('quiz/teacher/list/past/', listLaunchedQuiz, name='quizTeacherListLaunched'),
    path('quiz/teacher/list/future/', listUnLaunchedQuiz, name='quizTeacherListUnLaunched'),
    path('quiz/teacher/perview/<int:quiz_id>/' ,detailQuiz, name='quizTeacherPerview'),
    # 
    path('questions/create/mcq/', createQuestion, name='qustionCreateMcq'),
    path('questions/create/tfq/', createQuestion2, name='questionCreateTR'),
    path('questions/review/create/<int:question_id>/', createRate, name='createReview'),
    path('questions/review/view/<int:question_id>/', viewRates, name='viewReviews'),
]
