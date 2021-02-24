from django.db import models
from django.urls import reverse
import uuid

# Create your models here.

class Language(models.Model):
    name = models.CharField(max_length=200,
    help_text="Enter the book/'s natural language(eg english,kiswahili,french)")

    def __str__(self):
        return self.name

class Genre(models.Model):
    #model representing the book genre
    name = models.CharField(max_length=200, help_text="Enter a book genre(eg science fiction)")

    def __str__(self):
        #string representing the model object
        return self.name

class Book(models.Model):
    #model representing book's title
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief explanation of the book")
    isbn = models.CharField("ISBN", max_length=20, unique=True,
    help_text="20 character <a href='https://www.isbin-international.org/content/what-isbn'>ISBN number")
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")

    def __str__(self):
        #representing the model object
        return self.title

    def get_absolute_url(self):
        #returns a url to access a detailed record of this book
        return reverse("book-detail", args=[str(self.id)])
class BookInstance(models.Model):
    #model representing a specific copy of the book
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
    help_text="Unique id for this book")
    book = models.ForeignKey("Book", on_delete=models.PROTECT)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ("m", "Maintenance"),
        ("o", "On loan"),
        ("a", "Available"),
        ("r", "Reserved")


    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default="m",
        help_text="Book availability",
    )

    class Meta:
        ordering = ["due_back"]
    def __str__(self):
        return f"{self.id} ({self.book.title})"

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("Died", null=True, blank=True)
    
    class Meta:
        ordering = ["last_name", "first_name"]
    
    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.last_name}, {self.last_name}"