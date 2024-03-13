from rest_framework import generics, status, filters

from .models import Author, Book, Publisher
from .serializers import AuthorSerializer, BookSerializer, PublisherSerializer

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import render
from django.db.models import Q


# ListCreateAPIView for GET list and POST new entry
class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    print(serializer_class)


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
            elif len(name_parts) >=2:
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


class PublisherAutocomplete(generics.ListAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email_id']


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# RetrieveUpdateDestroyAPIView for GET detail, PUT update, PATCH partial_update, and DELETE delete
class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


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


def search_author(request):
    query_set = Author.objects.all()
    # print(query_set)
    print({"authors": query_set})
    return render(request, 'C:\\Users\\SII147\\POC Project - Django\\poc\\templates\\logs.html', {"authors": query_set})
