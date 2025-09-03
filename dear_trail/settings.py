import os
from pathlib import Path
import static
import staticfiles

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 安全密钥（实际部署时更换）
SECRET_KEY = 'django-insecure-example-key-for-development-only'

# 开发模式
DEBUG = True
print(f"当前DEBUG值：{DEBUG}")

# 允许访问的主机
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# 应用配置
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',  # 用户认证应用
    'dashboard', # 核心功能应用
]

# 中间件配置
MIDDLEWARE = [
    # 'dear_trail.middleware.StaticFileCharsetMiddleware'
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.contrib.staticfiles.middleware.StaticFilesMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dear_trail.urls'

# 模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dear_trail.wsgi.application'

# 数据库配置（MySQL）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dear_trail',
        'USER': 'root',
        'PASSWORD': 'zll200205',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}

# 密码验证
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 国际化配置
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# 静态文件配置
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # 假设你的CSS文件在项目根目录的"static/css/"下
    # 若静态文件在其他目录（如app内的static），无需额外添加，Django会自动检索app内的static目录
]
# STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# 媒体文件配置（用户上传的文件）
MEDIA_URL = './media/'
MEDIA_ROOT = BASE_DIR / 'templates/media'


# 登录配置
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# 默认主键类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
