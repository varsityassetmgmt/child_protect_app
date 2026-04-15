from django.urls import path
from . import views

urlpatterns = [
    # path('', views.login_view),
    # path('logout/', views.logout_view, name='logout'),

    path('', views.login_view, name='login'),   # ✅ ADD name='login'
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard),
    path('check-url/', views.check_url),
 



    path('restricted-urls/', views.restricted_urls, name='restricted_urls'),
    path('add-url/', views.add_url, name='add_url'),
    path('edit-url/<int:id>/', views.edit_url, name='edit_url'),






    path('users/', views.user_list, name='user_list'),
    path('add-user/', views.add_user, name='add_user'),
    path('edit-user/<int:id>/', views.edit_user, name='edit_user'),
    path('change-password/<int:id>/', views.change_password, name='change_password'),



]