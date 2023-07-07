from rest_framework import serializers

from .models import Category, Author
from .models.book import Book


class BookListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('slug', 'title', 'image', 'author', 'year')


class BookDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ('id',)


class BookCreateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ('id', 'slug', 'page_count')

