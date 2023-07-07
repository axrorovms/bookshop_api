from django.urls import path, include
from bookshop import views
urlpatterns = [
    path('book', views.BookCreateApiView.as_view()),
    path('book-list', views.BookListApiView.as_view()),
    path('book-detail/<str:slug>', views.BookRetrieveAPIView.as_view()),
    ]