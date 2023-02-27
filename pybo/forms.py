from django import forms
from pybo.models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']

        widgets = {
           'subject': forms.TextInput(attrs={'placeholder': '제목을 입력하세요.'}),
           'content': forms.Textarea(attrs={'placeholder': '내용을 입력하세요.'}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        