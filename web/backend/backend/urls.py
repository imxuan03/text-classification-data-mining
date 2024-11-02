from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from .views import TextDetectAPI

urlpatterns = [
    path('api/detect/', TextDetectAPI.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)