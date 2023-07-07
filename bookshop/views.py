from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Book
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import BookCreateModelSerializer, BookDetailModelSerializer, BookListModelSerializer
from rest_framework.filters import SearchFilter
from .filter import Booksfilter
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class BookCreateApiView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookCreateModelSerializer
    parser_classes = (MultiPartParser, FormParser)


class BookListApiView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = Booksfilter
    search_fields = ('title', 'year', 'category__name', 'author__name')

    def get(self, request, *args, **kwargs):
        obj = super().get(request, *args, **kwargs)
        if not self.request.user.is_authenticated:
            obj.data = obj.data[:10]
            return obj
        return obj


class BookRetrieveAPIView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailModelSerializer
    lookup_field = 'slug'
