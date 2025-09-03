from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),          # 仪表盘首页
    path('location/', views.location_view, name='location'),   # 地址管理
    path('checkin/', views.checkin_view, name='checkin'),      # 每日打卡
    path('activity/', views.activity_view, name='activity'),   # 活动记录
    path('music/', views.music_view, name='music'),  # 音乐库页面
    path('music/upload/', views.upload_music, name='upload_music'),  # 上传音乐
    path('music/delete/<int:music_id>/', views.delete_music, name='delete_music'),

]
