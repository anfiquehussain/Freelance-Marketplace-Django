from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('chat/<int:order_id>/<str:username>/', views.Userchat, name='userchat'),
    path('get_messages/<int:order_id>/', views.get_messages, name='get_messages'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)