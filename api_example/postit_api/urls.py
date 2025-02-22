from django.contrib import admin
from django.urls import path, include
from .views import (PostList,
                    PostDetail,
                    CommentList,
                    CommentDetail,
                    PostLikeCreate,
                    UserCreate)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("posts/", PostList.as_view()),
    path("posts/<int:pk>", PostDetail.as_view()),
    path("posts/<int:pk>/comments", CommentList.as_view()),
    path("comments/<int:pk>", CommentDetail.as_view()),
    path("posts/<int:pk>/like", PostLikeCreate.as_view()),
    path("signup/", UserCreate.as_view()),
]
