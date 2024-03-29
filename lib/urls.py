from django.urls import path
from . import views

urlpatterns = [
    path('authors/', views.AuthorListCreateView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
    path('authors/autocomplete/', views.AuthorAutocomplete.as_view(), name='author-autocomplete'),
    path('books/', views.BookListCreateView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('publishers/', views.PublisherListCreateView.as_view(), name='publisher-list'),
    path('publishers/<int:pk>/', views.PublisherDetailView.as_view(), name='publisher-detail'),
    path('publishers/<int:pk>/delete/', views.PublisherDeleteView.as_view(), name='publisher-delete'),
    path('publishers/autocomplete/', views.PublisherAutocomplete.as_view(), name='publisher-autocomplete'),
    path('upload/', views.NumberFileUploadView.as_view(), name='number-file-upload'),
    path('statistics/books_per_year/', views.BooksPerYear.as_view(), name='books-per-year'),
    path('statistics/books_per_author/', views.BooksPerAuthor.as_view(), name='books-per-author'),
]
