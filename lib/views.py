from rest_framework import generics, status, filters

from .models import Author, Book, Publisher
from .serializers import AuthorSerializer, BookSerializer, PublisherSerializer

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Q, Count
from django.db.models.deletion import ProtectedError


# ListCreateAPIView for GET list and POST new entry
class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    print(serializer_class)


# RetrieveUpdateDestroyAPIView for GET detail, PUT update, PATCH partial_update, and DELETE delete
class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError as e:
            # You can customize the error message or use the default one
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class AuthorDeleteView(APIView):
    def delete(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
            author.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Author.DoesNotExist:
            return Response({'error': 'Author not found.'}, status=status.HTTP_404_NOT_FOUND)
        except ProtectedError:
            return Response({'error': 'Cannot delete author because it is referenced by books.'},
                            status=status.HTTP_400_BAD_REQUEST)


class AuthorAutocomplete(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search_parm = self.request.query_params.get('search', None)

        if search_parm:
            name_parts = search_parm.split()

            if len(name_parts) == 1:
                queryset = queryset.filter(
                    Q(first_name__istartswith=name_parts[0]) |
                    Q(last_name__istartswith=name_parts[0])
                )
            elif len(name_parts) >= 2:
                queryset = queryset.filter(
                    Q(first_name__istartswith=name_parts[0]) |
                    Q(last_name__istartswith=name_parts[1])
                )

        return queryset

    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']


class PublisherListCreateView(generics.ListCreateAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class PublisherDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError as e:
            # You can customize the error message or use the default one
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class PublisherDeleteView(APIView):
    def delete(self, request, pk):
        try:
            publisher = Publisher.objects.get(pk=pk)
            publisher.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Publisher.DoesNotExist:
            return Response({'error': 'Publisher not found.'}, status=status.HTTP_404_NOT_FOUND)
        except ProtectedError:
            return Response({'error': 'Cannot delete publisher because it is referenced by books.'},
                            status=status.HTTP_400_BAD_REQUEST)


class PublisherAutocomplete(generics.ListAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email_id']


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BooksPerYear(APIView):
    def get(self, request):
        books_per_year = (Book.objects
                          .values('publication_date')
                          .annotate(count=Count('id'))
                          .order_by('publication_date'))
        return Response(books_per_year)


class BooksPerAuthor(APIView):
    def get(self, request):
        books_per_author = Author.objects \
            .annotate(book_count=Count('books')) \
            .values('first_name', 'last_name', 'book_count') \
            .order_by('-book_count')
        return Response(books_per_author)


class NumberFileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file_obj = request.FILES.get('file', None)
        print(file_obj)
        if not file_obj:
            return Response({
                "error": "No file was submitted,"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Read and parse the file content
        content = file_obj.read().decode('utf-8')

        number_list = [num.strip() for num in content.split(',') if num.strip().isdigit()]
        if not number_list:
            return Response({
                "error": "The file contains non-numeric values"
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response(number_list, status=status.HTTP_200_OK)
