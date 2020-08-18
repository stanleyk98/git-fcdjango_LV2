from django.shortcuts import render , redirect
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm, LoginForm
from .models import Fcuser


# Create your views here.

# 회원가입 메뉴


def index(request):
    return render(request, 'index.html', {'email': request.session.get('user')})

# 회원가입 뷰


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        fcuser = Fcuser(
            email = form.data.get('email') , 
            password = make_password(form.data.get('password')) ,
            level = 'user'
            )
        fcuser.save()

        return super().form_valid(form)

        

# 로그인 뷰


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    # 로그인 이후 세션 저장
    def form_valid(self, form):
        self.request.session['user'] = form.data.get('email')

        return super().form_valid(form)


def logout(request):
    if 'user' in request.session:
        del(request.session['user'])
    return redirect('/')