"""localDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
# from django.urls import path
from django.conf.urls import url, include
from missions import views
from . import settings  # 为静态文件添加的
from django.conf.urls.static import static  # 为静态文件添加的

urlpatterns = [
    # path('admin/', admin.site.urls), #admin后台的路由
    url('', views.index),
    # path('', views.index),  # 来自服务器的请求为网站根目录时，由视图中的index函数进行处理。
]  # + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)  # 为静态文件添加的

if settings.DEBUG:
    pass
else:
    from django.views.static import serve
    from localDjango.settings import STATIC_ROOT
    urlpatterns.append(url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATICFILES_DIRS}))

    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.contrib import staticfiles
    # urlpatterns += staticfiles_urlpatterns()