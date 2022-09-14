from django.contrib import admin

from .models import Categories, Comment, Genres, Review, Title, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'bio',
    )
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'pub_date',
        'author',
        'review',
    )
    search_fields = ('text', )
    empty_value_display = '-пусто-'


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
    )
    search_fields = ('name', 'slug')
    list_filter = ('category', 'genre', 'year')
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'pub_date',
        'author',
        'score',
        'title',
    )
    search_fields = ('text', 'title')
    list_filter = ('author', 'score')
    empty_value_display = '-пусто-'
