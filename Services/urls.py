from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('manage_services/<str:identifier>', views.create_job_profile, name='create_job_profile'),
    path('delete_service/<str:username>/<int:overview_id>/', views.delete_service, name='delete_service'),
    path('edit_service/<str:username>/<int:overview_id>/', views.edit_service, name='edit_service'),
    path('view_service_profile/<int:overview_id>/',views.view_service_profile,name='view_service_profile')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)