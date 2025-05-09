from django.db import models

class Author(models.Model):
    fullname = models.CharField(max_length=100, null=False, unique=True)
    born_date = models.DateField(max_length=50)
    born_location = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.fullname
    
class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.name
    
class Quote(models.Model):
    quote = models.TextField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)