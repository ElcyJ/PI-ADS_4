from django.urls import path
from . import views

urlpatterns = [
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),
    path('profiles/', views.profiles_list),
    path('profiles/<int:pk>', views.profile_detail),
    path('profile-post', views.profile_posts_list),
    path('profile-post/<int:pk>', views.profile_posts_detail),
    path('post-comment', views.post_comments_list),
    path('post-comment/<int:pk>', views.post_comments_detail),
    path('posts/<int:pk>/comments', views.comments_list),
    path('posts/<int:pk>/comments/<int:pk2>', views.comment_detail),
    path('profile-status', views.profile_status),
]