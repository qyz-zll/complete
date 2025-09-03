import os
import sys
import django
# import settings
# 获取项目根目录路径（wsgi.py 所在目录的父目录）
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 若根目录不在 sys.path 中，添加进去
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# 以下是默认的 wsgi.py 代码（保持不变）
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dear_trail.settings')
application = get_wsgi_application()