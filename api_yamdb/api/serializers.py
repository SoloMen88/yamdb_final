from datetime import datetime as dt

from django.shortcuts import get_object_or_404
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import (
    CharField,
    CurrentUserDefault,
    EmailField,
    HiddenField,
    ModelSerializer,
    Serializer,
    ValidationError,
    IntegerField
)

from reviews.models import Categories, Comment, Genres, Review, Title, User


class CategoriesSerializer(ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name', 'slug',)


class GenresSerializer(ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug',)


class TitlesCreateSerializer(ModelSerializer):
    genre = SlugRelatedField(
        queryset=Genres.objects.all(),
        required=False,
        many=True,
        slug_field='slug'
    )
    category = SlugRelatedField(
        queryset=Categories.objects.all(),
        required=False,
        slug_field='slug',
    )
    rating = IntegerField(required=False,)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'category', 'genre')

    def validate_year(self, value):
        """Функция проверки даты"""
        year = dt.now().year
        if value > year:
            raise ValidationError(
                'Произведения из будущего не принимаем!')
        return value


class TitlesSerializer(TitlesCreateSerializer):
    genre = GenresSerializer(
        required=False,
        many=True,
    )
    category = CategoriesSerializer(
        required=False,
    )


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )


class UserRegisterSerializer(Serializer):
    email = EmailField(required=True, write_only=True)
    username = CharField(required=True, write_only=True)

    def validate_username(self, value):
        """Проверка, что username больше 2х символов и != 'me' """
        user = User.objects.filter(username=value)
        if user.exists():
            raise ValidationError('Имя пользователя уже занято')
        if len(value) < 2:
            raise ValidationError('Username too short')
        if value == 'me':
            raise ValidationError('Username cannot be equal to "me"')
        return value

    def validate_email(self, value):
        """Проверка, что email уникальный для нового пользователя"""
        user = User.objects.filter(email=value)
        if user.exists():
            raise ValidationError('Данный email уже используется')
        return value


class UserConfirmationSerializer(Serializer):
    username = CharField(required=True, write_only=True)
    confirmation_code = CharField(required=True, write_only=True)


class CurrentTitle:
    requires_context = True

    def __call__(self, serializer_field):
        c_view = serializer_field.context['view']
        title_id = c_view.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title

    def __repr__(self):
        return f'{self.__class__.__name__}()'


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(
        default=CurrentUserDefault(),
        slug_field='username',
        read_only=True)
    title = HiddenField(default=CurrentTitle())

    class Meta:
        model = Review
        read_only_fields = ('author',)
        fields = '__all__'

    def validate(self, data):
        """Проверка на наличие отзыва у текущего пользователя"""

        if self.context.get('request').method != 'POST':
            return data
        author = self.context['request'].user.id
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if Review.objects.filter(title=title, author=author).exists():
            raise ValidationError(
                'Вы уже оставили Ваш отзыв!'
            )
        return data


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        read_only_fields = ('author',)
        fields = ('id', 'text', 'author', 'pub_date')
