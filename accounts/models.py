from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """用户个人资料模型，扩展Django内置用户模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="用户")
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="手机号")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="头像")
    bio = models.TextField(blank=True, null=True, verbose_name="个人简介")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "用户资料"
        verbose_name_plural = "用户资料"

    def __str__(self):
        return f"{self.user.username}的个人资料"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.phone and (len(self.phone) != 11 or not self.phone.isdigit()):
            raise ValidationError({"phone": "手机号必须是11位数字"})

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except Exception as e:
            print(f"保存用户资料失败: {e}")
            raise

# 信号：当用户创建时自动创建个人资料
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created,** kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Exception:
        UserProfile.objects.create(user=instance)
