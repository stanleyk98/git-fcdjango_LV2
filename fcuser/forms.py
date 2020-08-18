from django import forms
from .models import Fcuser

# 비번 암호화
from django.contrib.auth.hashers import check_password, make_password

# 회원가입 폼


class RegisterForm(forms.Form):
    email = forms.EmailField(
        error_messages={'required': '이메일을 입력해야해요'}, max_length=64, label='이메일')
    password = forms.CharField(
        error_messages={'required': '비번을 입력해야해요'}, widget=forms.PasswordInput, label='비밀번호')
    re_password = forms.CharField(
        error_messages={'required': '비번을 입력해야해요'}, widget=forms.PasswordInput, label='비밀번호 확인')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        if password and re_password:
            if password != re_password:
                self.add_error('password', '비번이 서로 다름')
                self.add_error('re_password', '비번이 서로 다름')
            
            #clean 함수는 유효성 체크만 하게 하고 유효할때 처리로직은 view.py 클래스에서 처리하는게 좋음 

# 로그인 폼


class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={'required': '이메일을 입력해야해요'}, max_length=64, label='이메일')
    password = forms.CharField(
        error_messages={'required': '비번을 입력해야해요'}, widget=forms.PasswordInput, label='비밀번호')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                fcuser = Fcuser.objects.get(email=email)
            except Fcuser.DoesNotExist:
                self.add_error('email', '가입된 ID가 없습니다.')
                return

            if not check_password(password, fcuser.password):
                self.add_error('password', '비번이 다릅니다.')
            # else:
            #     self.email = fcuser.email
 