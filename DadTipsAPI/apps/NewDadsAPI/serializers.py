from rest_framework import serializers

from .models import (

    Category, Post
)


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = (
            'id', 'name', 'content', 'posted_at', 'is_public'
        )

class CategorySerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    post = PostSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'description'
        )