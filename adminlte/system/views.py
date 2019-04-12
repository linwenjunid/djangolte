from django.shortcuts import render, redirect, HttpResponse
from .models import MenuInfo
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login, get_user_model, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from functools import wraps

UserModel = get_user_model()


@login_required
def func(request):
    if request.method == 'GET':
        return render(request, 'func.html')
    elif request.method == 'POST':
        user = request.user
        msg = None
        oldPassword = request.POST.get('oldPassword')
        newPassword = request.POST.get("newPassword")
        conPassword = request.POST.get('conPassword')
        if user.check_password(oldPassword):  # 到数据库中验证旧密码通过
            if newPassword is None or conPassword is None:  # 新密码或确认密码为空
                msg = "新密码不能为空"
            elif newPassword != conPassword:  # 新密码与确认密码不一样
                msg = "两次密码不一致"

            else:
                user.set_password(newPassword)  # 修改密码
                user.save()
                msg = '密码修改成功'
        else:
            msg = "旧密码输入错误"
        return render(request, 'func.html', {'msg': msg})


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