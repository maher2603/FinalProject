#URLs for frontend to communicate with the backend

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.main_spa, name='main_spa'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user-api/', views.user_api, name='user_api'),
    path('update_user_profile/', views.update_user_profile, name='update_user_profile'),
    path('vehicle-search/', views.vehicle_search, name='vehicle_search'),
    path('add-vehicle/', views.add_vehicle, name='add_vehicle'),
    path('get-vehicles/', views.get_vehicles, name='get_vehicles'),
    path('get-vehicle/<int:vehicle_id>/', views.get_vehicle, name='get_vehicle'),
    path('remove-vehicle/<int:vehicle_id>/', views.remove_vehicle, name='remove_vehicle'),
    path('add-vehicle-log/<int:vehicle_id>/', views.add_vehicle_log, name='add_vehicle_log'), 
    path('get-vehicle-logs/<int:vehicle_id>/', views.get_vehicle_logs, name='get_vehicle_logs'),
    path('delete-vehicle-log/<int:log_id>/', views.delete_vehicle_log, name='delete_vehicle_log'),
    path('add-post/', views.add_post, name='add_post'),  
    path('get-posts/', views.get_posts, name='get_posts'),
    path('get-post/<int:post_id>/', views.get_post, name='get_post'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('add-comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('get-comments/<int:post_id>/', views.get_comments, name='get_comments'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('add-reply/<int:comment_id>/', views.add_reply, name='add_reply'),
    path('get-replies/<int:comment_id>/', views.get_replies, name='get_replies'),
    path('delete-reply/<int:reply_id>/', views.delete_reply, name='delete_reply'),
    path('send-email/', views.send_email, name='send_email'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
