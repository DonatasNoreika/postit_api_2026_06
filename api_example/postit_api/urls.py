from django.contrib import admin
from django.urls import path, include
from .views import PostList, PostDetail, CommentList

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("posts/", PostList.as_view()),
    path("posts/<int:pk>", PostDetail.as_view()),
    path("posts/<int:pk>/comments", CommentList.as_view()),
]
