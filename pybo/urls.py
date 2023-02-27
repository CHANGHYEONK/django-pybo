from django.urls import path
from . import views

app_name = 'pybo'

# 관리의 편의상 grouping 하는게 좋음
urlpatterns = [
    path('', views.index, name='index'),                       # 목록 보기
    path('<int:question_id>/', views.detail, name='detail'),   # 상세 보기

    path('question/create/', views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),

    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
]
