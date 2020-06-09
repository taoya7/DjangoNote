from django.shortcuts import render,reverse, redirect

from django.http import HttpResponse
from django.views.generic import View

# 引入
from django.contrib import messages



class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username=='admin' and password=='admin':
            messages.success(request, '登录成功, 正在跳转。')
            return redirect(reverse('login'))
        else:
            messages.error(request, '登录失败，可能用户名或密码错误。')
            return redirect(reverse('login'))
