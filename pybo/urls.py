from django.urls import path
from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.index, name='index'),                       # 목록 보기
    path('<int:question_id>/', views.detail, name='detail'),   # 상세 보기
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
]
