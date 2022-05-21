"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

from manga.views import *

schema_view = get_schema_view(
    openapi.Info(
        title='Fullstack',
        default_version='v1',
        description='chto-to',
    ),
    public = True
)


router = DefaultRouter()
router.register('novella', NovellaViewSet)
router.register('novella', NovellaImageViewSet)
router.register('genres', GenreViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('api/v1/', include('account.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/novella/<int:id>/toggle_like/', toggle_like),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
