from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.exceptions import (
    PermissionDenied, ValidationError
)

from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import (
    Category, Post
)

from .serializers import (
    CategorySerializer, PostSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Category.objects.all().filter(owner = self.request.user)

        return queryset

    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        category = Category.objects.filter(
            name = request.data.get('name'),
            owner = request.user
        )
        if category:
            msg = 'Category with name already exists'
            raise ValidationError(msg)
        return super().create(request)

    def destroy(self, request, *args, **kwargs):
        category = Category.objects.get(pk=self.kwargs['pk'])
        if not request.user == category.owner:
            raise PermissionDenied('Permission Denied')
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)

class PostCategories(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.kwargs.get('category_pk'):
            category = Category.objects.get(pk = self.kwargs["pk"])
            queryset = Post.objects.filter(
                owner = self.request.user,
                category = category
            )
            return queryset

        serializer_class = PostSerializer

        def perform_create(self, serializer):
            serializer.save(owner =self.request.user)


class PostViewSets(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Post.objects.all().filter(
            owner=self.request.user
        )
        return queryset

    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied(
                'Only valid users allowed to post'
            )
        return super().create(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        if not request.user == post.owner:
            raise PermissionDenied(
                'Only the user who owns this content can delete this post'
            )
        return super().destroy(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        if not request.user == post.owner:
            raise PermissionDenied(
                'The user who posted this has permission to update it'
            )
        return super().update(request, *args, **kwargs)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)