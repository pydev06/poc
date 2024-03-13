from django.db import models


# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateTimeField()


class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_date = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
