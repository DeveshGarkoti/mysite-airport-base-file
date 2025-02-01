from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
from django.urls import path
from . import views

urlpatterns += [
    path('add-comment/<int:content_type_id>/<int:object_id>/', views.add_comment, name='add_comment'),
]
