from django.shortcuts import render, redirect, HttpResponse
from .models import MenuInfo
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login, get_user_model, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from functools import wraps

UserModel = get_user_model()


@login_required
def index(request):
    return render(request, 'cont.html')


def login_view(request):
    return render(request, 'login.html')


def acc_login(request):
    data=request.POST
    print(data)
    username = request.POST.get('username')
    password = request.POST.get("password")
    user = authenticate(username=username, password=password)  # 验证用户名和密码，返回用户对象

    if user:  # 如果用户对象存在
        login(request, user)  # 用户登陆
        return redirect("/index/")
    else:
        return render(request, 'login.html',{'error':'登陆失败'})


def acc_logout(request):
    logout(request)  # 注销用户
    return redirect("/index/")


# 邮箱OR手机号OR用户名认证
class MaxBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get(Q(phone_number=username) | Q(email=username) | Q(username=username))
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user