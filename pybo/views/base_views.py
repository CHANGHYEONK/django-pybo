from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from ..models import Question
from django.db.models import Q, Count


def index(request):
    """
    pybo 목록 출력
    """
    # 각각 목적에 맞는 변수 선언
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')
    
    # 정렬 방법 => so 이용해서 question_list 정의
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else: # recent
        question_list = Question.objects.order_by('-create_date')
        # question_list = Question.objects.order_by('author__username')

    # SQL where xxx like '% yyy %' => kw 이용해서 question_list 정의
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |                  # 제목검색
            Q(content__icontains=kw) |                  # 내용검색
            Q(author__username__icontains=kw) |         # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)   # 답글 글쓴이검색
        ).distinct()

    # 페이지 분할
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    # context 변수 지정
    context = {
        'question_list': page_obj,
        'kw': kw,       # 검색 + 페이지 이동을 위한 처리
        'page': page,   # 검색 + 페이지 이동을 위한 처리
        'so': so        # 정렬을 위한 변수 선언
        }
    
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    '''
    pybo 내용 출력
    '''
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
