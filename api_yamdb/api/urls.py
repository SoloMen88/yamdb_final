from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoriesViewSet, CommentsViewSet, CreateTokenView,
                       GenresViewSet, ReviewsViewSet, SignUp, TitlesViewSet,
                       UserViewSet)

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='account-details')
router_v1.register('categories', CategoriesViewSet)
router_v1.register('genres', GenresViewSet)
router_v1.register('titles', TitlesViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewsViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments')

auth_url = [
    path('signup/', SignUp.as_view(), name='register'),
    path('token/', CreateTokenView.as_view(), name='token'),
]

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_url)),
]
