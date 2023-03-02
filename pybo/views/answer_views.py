from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from ..models import Question, Answer
from django.utils import timezone
from ..forms import AnswerForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
            # 앵커 #answer_7 추가
            url = resolve_url('pybo:detail', question_id=question.id)
            url = url + f'#answer_{answer.id}'
            return redirect(url)
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
            url = resolve_url('pybo:detail', question_id=answer.question.id)
            url = url + f'#answer_{answer.id}'
            return redirect(url)
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