from django.urls import path
from django.contrib.auth import views as auth_views     # 별칭 줌으로써 충돌 피함
from . import views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup')
]