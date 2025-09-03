from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import date


class Location(models.Model):
    """地址记录模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locations', verbose_name="用户")
    name = models.CharField(max_length=100, verbose_name="地点名称")
    address = models.TextField(verbose_name="详细地址")
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True, verbose_name="纬度")
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True, verbose_name="经度")
    is_default = models.BooleanField(default=False, verbose_name="是否默认地址")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "地址记录"
        verbose_name_plural = "地址记录"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name}（{self.user.username}）"

    def clean(self):
        # 验证经纬度范围
        if self.latitude:
            if not (-90 <= float(self.latitude) <= 90):
                raise ValidationError({"latitude": "纬度必须在-90到90之间"})

        if self.longitude:
            if not (-180 <= float(self.longitude) <= 180):
                raise ValidationError({"longitude": "经度必须在-180到180之间"})

        # 确保每个用户最多只有一个默认地址
        if self.is_default:
            existing_default = Location.objects.filter(
                user=self.user,
                is_default=True
            ).exclude(id=self.id if self.id else None)

            if existing_default.exists():
                raise ValidationError({"is_default": "每个用户只能有一个默认地址"})

    def save(self, *args, **kwargs):
        from django.db import transaction
        try:
            with transaction.atomic():
                self.full_clean()
                if self.is_default:
                    Location.objects.filter(user=self.user, is_default=True).exclude(
                        id=self.id if self.id else None
                    ).update(is_default=False)
                super().save(*args, **kwargs)
        except ValidationError as e:
            print(f"保存地址失败: {e}")
            raise


class CheckIn(models.Model):
    """打卡记录模型"""
    STATUS_CHOICES = (
        ('completed', '已完成'),
        ('late', '迟到'),
        ('absent', '缺席'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkins', verbose_name="用户")
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='checkins',
        verbose_name="打卡地点"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='completed',
        verbose_name="打卡状态"
    )
    notes = models.TextField(blank=True, null=True, verbose_name="备注")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="打卡时间")

    class Meta:
        verbose_name = "打卡记录"
        verbose_name_plural = "打卡记录"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} {self.created_at.strftime('%Y-%m-%d')} {self.get_status_display()}"

    def clean(self):
        # 检查是否重复打卡
        today = date.today()
        if not self.pk:  # 新记录才检查
            if CheckIn.objects.filter(
                    user=self.user,
                    created_at__date=today
            ).exists():
                raise ValidationError("今天已经打卡，不能重复打卡")

        # 检查打卡地点是否属于当前用户
        if self.location and self.location.user != self.user:
            raise ValidationError("打卡地点必须是用户自己创建的地址")

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            print(f"打卡记录保存失败: {e}")
            raise


class Activity(models.Model):
    """活动记录模型"""
    CATEGORY_CHOICES = (
        ('work', '工作'),
        ('life', '生活'),
        ('travel', '旅行'),
        ('study', '学习'),
        ('other', '其他'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities', verbose_name="用户")
    title = models.CharField(max_length=200, verbose_name="活动标题")
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other',
        verbose_name="活动类别"
    )
    description = models.TextField(blank=True, null=True, verbose_name="活动描述")
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activities',
        verbose_name="活动地点"
    )
    start_time = models.DateTimeField(verbose_name="开始时间")
    end_time = models.DateTimeField(verbose_name="结束时间")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="创建时间")

    class Meta:
        verbose_name = "活动记录"
        verbose_name_plural = "活动记录"
        ordering = ['-start_time']

    def __str__(self):
        return self.title

    def clean(self):
        # 验证时间逻辑
        if self.start_time and self.end_time and self.start_time > self.end_time:
            raise ValidationError("开始时间不能晚于结束时间")

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            print(f"活动记录保存失败: {e}")
            raise


class Music(models.Model):
    """音乐模型，用于存储用户上传的音乐"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='musics')
    title = models.CharField(max_length=200, verbose_name="音乐标题")
    artist = models.CharField(max_length=200, blank=True, verbose_name="艺术家")
    audio_file = models.FileField(upload_to='music/', verbose_name="音频文件")
    cover_image = models.ImageField(upload_to='music_covers/', blank=True, null=True, verbose_name="封面图片")
    uploaded_at = models.DateTimeField(default=timezone.now, verbose_name="上传时间")

    class Meta:
        verbose_name = "音乐"
        verbose_name_plural = "音乐"
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title
