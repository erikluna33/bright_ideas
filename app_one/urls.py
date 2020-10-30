from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('admin', views.admin_page),
    path('register_user', views.register_user),
    path('login_user', views.login_user),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('add_user_page', views.add_user_page),
    path('add_new_user', views.add_new_user),
    path('user/update/<int:uid>', views.update_user_page),
    path('update_user/<int:uid>', views.update_user),
    path('delete/<int:uid>', views.delete_user),
    path('ideas', views.ideas_page),
    path('post_idea', views.post_idea),
    path('post_comment/<int:iid>', views.post_comment),
    path('user/<int:uid>', views.user_profile),
    path('delete_idea/<int:iid>', views.delete_idea),
    
]