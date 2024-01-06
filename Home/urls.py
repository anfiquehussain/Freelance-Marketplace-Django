from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.IntroHome, name='IntroHome'),
    path('<str:identifier>/',views.home, name='home'),
    path('edit_profile/<str:identifier>/', views.edit_profile, name='edit_profile'),
    # path('profile/<str:username>/', views.view_profile, name='profile'),
    path('view_profile/<str:username>/',views.view_profile_public,name='view_profile_public'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)