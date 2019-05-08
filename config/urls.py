"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('',include('photo.urls')),
]

# 특정 리소스를 static형태로 응답
from django.conf.urls.static import static

# 장고의 셋팅값을 불러다 주는 역할
from django.conf import settings

# 개발 상태일 때만 사용 -> Deploy, Live 일 때는 사용하지 않는다.
# 1) 웹 서버가 해줘야 할일
# 2) 파일 서버를 별도로 셋팅
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

