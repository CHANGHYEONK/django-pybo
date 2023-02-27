from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
# def index(request):
#     return HttpResponse('''
#     <h1>안녕하세요.</h1>
#     pybo에 오신것을 환영합니다.
#     ''')

def index(request):
    """
    pybo 목록 출력
    """
    page = request.GET.get('page', '1')
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    '''
    pybo 내용 출력
    '''
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)




@login_required(login_url='common:login')
def question_create(request):
    '''
    pybo 질문등록
    '''
    if request.method == 'POST':    # submit을 통한 POST 요청
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:                           # GET 요청
        form = QuestionForm()
    
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo 질문수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST":
        # 질문 수정을 위해 값 덮어쓰기
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            # question.author = request.user
            question.modify_date = timezone.now() # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        # 질문 수정 화면에 기존 제목, 내용 반영
        form = QuestionForm(instance=question)

    context = {'form': form}

    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')




@login_required(login_url='common:login')
def answer_create(request, question_id):
    '''
    pybo 답변 등록
    '''
    # print(request.method)
    # print(request.GET)   #dict
    # print(request.POST)  #dict
    # content = request.POST['content']         # 1) 키가 없으면, 예외 발생
    # print('[content]', content)
    # content = request.POST.get('content', '') # 2) 키가 없으면 None 반환 or ,뒤에 있는 값 반환
    # print('get(content)', content)
    question = get_object_or_404(Question, pk=question_id)
    # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    pybo 답변수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    if request.method == "POST":
        # 답변 수정을 위해 값 덮어쓰기
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            # answer.author = request.user
            answer.modify_date = timezone.now() # 수정일시 저장
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        # 답변 수정 화면에 기존 내용 반영
        form = AnswerForm(instance=answer)

    context = {'answer': answer, 'form': form}

    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    pybo 답변삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)
    