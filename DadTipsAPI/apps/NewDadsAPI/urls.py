from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import (
    PostCategories,PostViewSets,CategoryViewSet
)


router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('posts', PostViewSets, basename='post')

custom_urlpatterns = [
    url(r'categories/(?P<category_pk>d+)/posts$', PostCategories.as_view(), name='post_categories'),
    url(r'categories/(?P<category_pk>\d+)/posts/(?P<pk>\d+)$', PostCategories.as_view(), name='single_post_category')
]

urlpatterns = router.urls
urlpatterns += custom_urlpatterns