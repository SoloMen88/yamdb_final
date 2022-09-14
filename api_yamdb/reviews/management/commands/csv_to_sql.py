import csv
import os

from django.core.management import BaseCommand

from reviews.models import (Categories, Comment, Genres, GenresTitles, Review,
                            Title, User)

TABLES_DICT = {
    User: 'users.csv',
    Categories: 'category.csv',
    Genres: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    GenresTitles: 'genre_title.csv'
}


class Command(BaseCommand):
    help = 'Load data from csv to sql'

    def handle(self, *args, **kwargs):
        path_csv = os.path.abspath('./static/data')
        for model, file in TABLES_DICT.items():
            with open(f'{path_csv}/{file}', 'r', encoding='utf-8') as csv_file:
                dict = csv.DictReader(csv_file)
                model.objects.bulk_create(model(**data) for data in dict)
