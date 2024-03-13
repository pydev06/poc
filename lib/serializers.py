from rest_framework import serializers
from .models import Author, Book, Publisher


class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Author
        fields = '__all__'


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'email_id']


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        write_only=True,
        source='author'
    )
    publisher_id = serializers.PrimaryKeyRelatedField(
        queryset=Publisher.objects.all(),
        write_only=True,
        source='publisher'
    )
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_date', 'author', 'publisher', 'author_id', 'publisher_id']

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.publication_date = validated_data.get('publication_date', instance.publication_date)
        instance.author = validated_data.get('author', instance.author)
        instance.publisher = validated_data.get('publisher', instance.publisher)
        instance.save()
        return instance
