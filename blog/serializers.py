from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class postSerializer(serializers.ModelSerializer):
    author = userSerializer(many=False, read_only=True)
    class Meta:
        model = Post
        fields = ['title', 'author', 'content', 'created_at']