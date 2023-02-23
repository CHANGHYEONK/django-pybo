from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator

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
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


def question_create(request):
    '''
    pybo 질문등록
    '''
    if request.method == 'POST':    # submit을 통한 POST 요청
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:                           # GET 요청
        form = QuestionForm()
    
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)