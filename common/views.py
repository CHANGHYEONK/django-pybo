from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm

# Create your views here.
def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})
    # 유효성 검사 실패 시에도 여기서 return 받아야 해서 return 위치 else 안이 아니라 여기임