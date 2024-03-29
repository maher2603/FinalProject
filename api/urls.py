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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
