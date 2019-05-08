# 모델 폼을 만들려면 2가지가 필요하다.
# 제네릭뷰 : 제네릭뷰, 모델
# 모델 폼 : 모델, 폼

from django.contrib.auth.models import User
from django import forms

class SignupForm(forms.ModelForm):
    # widget을 오버라이드하여 password를 입력할때 *을 찍어준다
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password2', widget=forms.PasswordInput)

    class Meta:
        model = User
        # fields 에는 해당 모델에 대해 입력받을 필드들을 나열한다.
        # + 추가 필드도 포함될 수 있다. -> 필드 목록과 추가 필드가 겹치면 오버라이드
        # fields 에 써준 순서대로 출력된다.
        fields = ['username', 'password', 'password2',]

    # password와 password2중에 password2로 비교를 하겠다
    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd['password'] != cd['password2']:
    #         raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
    #     # 항상 해당 필드의 값을 리턴한다.
    #     return cd['password2']