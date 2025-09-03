from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


def login_view(request):
    """用户登录视图"""
    if request.user.is_authenticated:
        return redirect('dashboard')  # 已登录用户直接跳转到仪表盘

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 验证用户
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, '登录成功！')
            return redirect('dashboard')
        else:
            messages.error(request, '用户名或密码错误')

    return render(request, 'index.html', {'page': 'login'})


def register_view(request):
    """用户注册视图"""
    if request.user.is_authenticated:
        return redirect('dashboard')  # 已登录用户直接跳转到仪表盘

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # 表单验证
        if password1 != password2:
            messages.error(request, '两次密码输入不一致')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, '用户名已存在')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, '邮箱已被注册')
            return redirect('register')

        # 创建用户（使用create_user避免last_login错误）
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            messages.success(request, '注册成功，请登录')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'注册失败：{str(e)}')

    return render(request, 'index.html', {'page': 'register'})


def logout_view(request):
    """用户退出视图"""
    logout(request)
    messages.success(request, '已成功退出登录')
    return redirect('login')


# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User


@login_required
def profile_view(request):
    """用户个人资料视图"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        # 验证用户名
        if username and username != request.user.username:
            if User.objects.filter(username=username).exists():
                messages.error(request, '用户名已被使用')
                return redirect('profile')
            request.user.username = username

        # 验证邮箱
        if email and email != request.user.email:
            if User.objects.filter(email=email).exists():
                messages.error(request, '邮箱已被注册')
                return redirect('profile')
            request.user.email = email

        # 保存修改
        try:
            request.user.save()
            messages.success(request, '个人资料更新成功')
        except Exception as e:
            messages.error(request, f'更新失败：{str(e)}')

        return redirect('profile')

    return render(request, 'index.html', {'page': 'profile'})