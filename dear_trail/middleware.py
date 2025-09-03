# 正确的 middleware.py 内容（无语法错误）
class StaticFileCharsetMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # 仅对CSS文件添加UTF-8编码头
        if request.path.startswith('/static/') and request.path.endswith('.css'):
            response['Content-Type'] = 'text/css; charset=utf-8'
        return response