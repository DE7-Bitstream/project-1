from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# 요청을 받아 hitmakers/index.html 템플릿을 렌더링하는 함수입니다.
def index(request: HttpRequest) -> HttpResponse:
    """
    hitmakers 앱의 루트 페이지를 렌더링합니다.
    """
    # templates/hitmakers/index.html 파일을 렌더링합니다.
    return render(request, 'hitmakers/index.html', {})