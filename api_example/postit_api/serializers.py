from rest_framework import serializers
from .models import Post, Comment, PostLike, CommentLike

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    user_id = serializers.ReadOnlyField(source="user.id")
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_id', 'post', 'body', 'created']

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    user_id = serializers.ReadOnlyField(source="user.id")
    # comments = CommentSerializer(many=True, allow_null=True)
    comments = serializers.StringRelatedField(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'user_id', 'title', 'body', 'created', "likes_count", "comments_count", 'comments', 'image']

    def get_comments_count(self, post):
        return Comment.objects.filter(post=post).count()

    def get_likes_count(self, post):
        return PostLike.objects.filter(post=post).count()


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['id']