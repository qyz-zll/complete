from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import date, timedelta

from .forms import MusicForm
from .models import Location, CheckIn, Activity, Music


@login_required
def dashboard_view(request):
    """仪表盘首页视图"""
    today = date.today()
    # 获取今日打卡状态
    checkin_status = "已完成" if CheckIn.objects.filter(
        user=request.user,
        created_at__date=today
    ).exists() else "未完成"

    # 获取最近的地址记录
    recent_location = Location.objects.filter(user=request.user).order_by('-created_at').first()

    # 获取最近的3条活动记录
    recent_activities = Activity.objects.filter(user=request.user).order_by('-start_time')[:3]

    return render(request, 'dashboard.html', {
        'user': request.user,
        'page': 'dashboard',
        'checkin_status': checkin_status,
        'recent_location': recent_location,
        'recent_activities': recent_activities
    })


@login_required
def location_view(request):
    """地址管理视图"""
    if request.method == 'POST':
        try:
            # 处理地址创建
            location = Location(
                user=request.user,
                name=request.POST.get('name'),
                address=request.POST.get('address'),
                latitude=request.POST.get('latitude') or None,
                longitude=request.POST.get('longitude') or None,
                is_default=request.POST.get('is_default') == 'on'
            )
            location.save()
            messages.success(request, '地址添加成功！')
            return redirect('location')
        except Exception as e:
            messages.error(request, f'添加失败: {str(e)}')

    # 获取用户所有地址
    locations = Location.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'dashboard.html', {
        'user': request.user,
        'page': 'location',
        'locations': locations
    })


@login_required
def checkin_view(request):
    """打卡视图"""
    today = date.today()

    # 检查今天是否已经打卡
    if CheckIn.objects.filter(user=request.user, created_at__date=today).exists():
        messages.info(request, '您今天已经打卡了！')
        return redirect('dashboard')

    if request.method == 'POST':
        try:
            checkin = CheckIn(
                user=request.user,
                location_id=request.POST.get('location_id') or None,
                status=request.POST.get('status', 'completed'),
                notes=request.POST.get('notes')
            )
            checkin.save()
            messages.success(request, '今日打卡成功！')
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f'打卡失败: {str(e)}')

    # 获取用户的地址列表供选择
    locations = Location.objects.filter(user=request.user)

    return render(request, 'dashboard.html', {
        'user': request.user,
        'page': 'checkin',
        'locations': locations
    })


@login_required
def activity_view(request):
    """活动记录视图"""
    if request.method == 'POST':
        try:
            activity = Activity(
                user=request.user,
                title=request.POST.get('title'),
                category=request.POST.get('category', 'other'),
                description=request.POST.get('description'),
                location_id=request.POST.get('location_id') or None,
                start_time=request.POST.get('start_time'),
                end_time=request.POST.get('end_time')
            )
            activity.save()
            messages.success(request, '活动记录添加成功！')
            return redirect('activity')
        except Exception as e:
            messages.error(request, f'添加失败: {str(e)}')

    # 获取用户所有活动
    activities = Activity.objects.filter(user=request.user).order_by('-start_time')

    return render(request, 'dashboard.html', {
        'user': request.user,
        'page': 'activity',
        'activities': activities
    })
# dashboard/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Music
from .forms import MusicForm

@login_required
def music_view(request):
    """音乐库页面，展示所有音乐"""
    musics = Music.objects.filter(user=request.user).order_by('-uploaded_at')
    music_form = MusicForm()
    return render(request, 'index.html', {
        'page': 'music',
        'musics': musics,
        'music_form': music_form
    })

@login_required
def upload_music(request):
    """处理音乐上传"""
    if request.method == 'POST':
        form = MusicForm(request.POST, request.FILES)
        if form.is_valid():
            music = form.save(commit=False)
            music.user = request.user  # 关联当前用户
            music.save()
            messages.success(request, '音乐上传成功！')
        else:
            messages.error(request, '上传失败，请检查文件格式和大小')
    return redirect('music')

@login_required
def delete_music(request, music_id):
    """删除音乐"""
    music = get_object_or_404(Music, id=music_id, user=request.user)
    try:
        music.delete()
        messages.success(request, '音乐已删除')
    except Exception as e:
        messages.error(request, f'删除失败：{str(e)}')
    return redirect('music')