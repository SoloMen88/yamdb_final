import django_filters
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (
    AllowAny, IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from django.db.models import Avg

from reviews.models import Categories, Comment, Genres, Title, User, Review
from .permissions import IsAdmin, IsAdminModeratorAuthorOrReadOnly, IsReadOnly
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenresSerializer, ReviewSerializer,
                          TitlesCreateSerializer, TitlesSerializer,
                          UserConfirmationSerializer,
                          UserRegisterSerializer, UserSerializer)
from .utils import send_confirmation_email


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoriesViewSet(CreateListDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdmin | IsReadOnly]
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class GenresViewSet(ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [IsAdmin | IsReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug', url_name='category_slug'
    )
    def get_genre(self, request, slug):
        category = self.get_object()
        serializer = CategoriesSerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class GenreFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(
        field_name='genre__slug', method='filter_genre')
    category = django_filters.CharFilter(
        field_name='category__slug', method='filter_category')
    year = django_filters.CharFilter(field_name='year', method='filter_year')
    name = django_filters.CharFilter(field_name='name', method='filter_name')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'name', 'year',)

    def filter_genre(self, queryset, name, genre):
        return Title.objects.filter(genre__slug__contains=genre)

    def filter_category(self, queryset, name, category):
        return Title.objects.filter(category__slug__contains=category)

    def filter_year(self, queryset, name, year):
        return Title.objects.filter(year__contains=year)

    def filter_name(self, queryset, names, name):
        return Title.objects.filter(name__contains=name)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitlesCreateSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_class = GenreFilter
    filterset_fields = ('name', 'year')
    permission_classes = [IsAdmin | IsReadOnly]

    def get_serializer_class(self):
        if (self.request.method == 'POST'
                or self.request.method == 'PATCH'
                or self.request.method == 'PUT'):
            return TitlesCreateSerializer
        return TitlesSerializer


class CreateTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']

        user = get_object_or_404(User, username=username)

        if user.confirmation_code == confirmation_code:
            access_token = AccessToken.for_user(user=user)
            return Response({"access_token": str(access_token)},
                            status=status.HTTP_200_OK)
        return Response('Please check your credentials',
                        status=status.HTTP_400_BAD_REQUEST)


class SignUp(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        user, created = User.objects.get_or_create(
            email=email,
            username=username
        )

        if created:
            user.confirmation_code = self._generate_code(user)
            send_confirmation_email(user.confirmation_code, email)
            return Response({"email": email, "username": username},
                            status=status.HTTP_200_OK)
        if not created and not user.confirmation_code:
            user.confirmation_code = self._generate_code(user)
            send_confirmation_email(user.confirmation_code, email)
            return Response({"email": email, "username": username},
                            status=status.HTTP_200_OK)
        return Response('user already exists',
                        status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def _generate_code(user):
        return default_token_generator.make_token(user)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    lookup_field = 'username'
    search_fields = ['username', ]

    @action(
        detail=False,
        methods=('get', 'patch',),
        permission_classes=[IsAuthenticated | IsAdmin]
    )
    def me(self, request):
        serializer = UserSerializer(request.user,
                                    data=request.data,
                                    partial=True)

        if request.user.is_admin or request.user.is_moderator:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        serializer.save(role='user')
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminModeratorAuthorOrReadOnly, ]

    def get_queryset(self):
        queryset = Review.objects.all()
        title_id = self.kwargs.get('title_id')
        queryset = queryset.filter(title_id=title_id)
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review = title.reviews.filter(author_id=self.request.user.id,
                                      title_id=title.id)
        if review.exists():
            raise ValidationError('Вы уже оставили Ваш отзыв!')
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminModeratorAuthorOrReadOnly, ]

    def get_queryset(self):
        queryset = Comment.objects.all()
        review_id = self.kwargs.get('review_id')
        queryset = queryset.filter(review_id=review_id)
        return queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
