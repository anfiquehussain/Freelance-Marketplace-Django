from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from Home.models import UserProfile

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Overview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titleOverview = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    overall_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    search_tags = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        # Split the comma-separated tags and remove whitespace
        tags = [tag.strip() for tag in self.search_tags.split(',')]
        self.search_tags = ','.join(tags)  # Store cleaned tags
        super().save(*args, **kwargs)
    

class BasicPackage(models.Model):
    DELIVERY_CHOICES1 = [
       (i, f"{i} days") for i in range(1, 91)
    ]
    REVISION_CHOICES1 = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        (6, "6"),
        (7, "7"),
        (8, "8"),
        (9, "9"),
        ("unlimited", "unlimited"),
    ]
    overview = models.ForeignKey(Overview, on_delete=models.CASCADE)
    Basic_title = models.CharField(max_length=100, default="")
    Basic_description = models.TextField(default="")
    Basic_delivery_time = models.PositiveIntegerField(choices=DELIVERY_CHOICES1, default=1)
    Basic_revisions = models.PositiveIntegerField(choices=REVISION_CHOICES1, default=1)
    Basic_source_file = models.BooleanField(default=False)
    Basic_price = models.IntegerField(default=0,validators=[MinValueValidator(50)])

class StandardPackage(models.Model):
    DELIVERY_CHOICES2 = [
        (i, f"{i} days") for i in range(1, 91)
    ]
    REVISION_CHOICES2 = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        (6, "6"),
        (7, "7"),
        (8, "8"),
        (9, "9"),
        ("unlimited", "unlimited"),
    ]
    overview = models.ForeignKey(Overview, on_delete=models.CASCADE)
    Standard_title = models.CharField(max_length=100, default="")
    Standard_description = models.TextField(default="")
    Standard_delivery_time = models.PositiveIntegerField(choices=DELIVERY_CHOICES2, default=1)
    Standard_revisions = models.PositiveIntegerField(choices=REVISION_CHOICES2, default=1)
    Standard_source_file = models.BooleanField(default=False)
    Standard_price = models.IntegerField(default=0,validators=[MinValueValidator(100)])

class PremiumPackage(models.Model):
    DELIVERY_CHOICES3 = [
        (i, f"{i} days") for i in range(1, 91)
    ]
    REVISION_CHOICES3 = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        (6, "6"),
        (7, "7"),
        (8, "8"),
        (9, "9"),
        ("unlimited", "unlimited"),
    ]
    overview = models.ForeignKey(Overview, on_delete=models.CASCADE)
    Premium_title = models.CharField(max_length=100, default="")
    Premium_description = models.TextField(default="")
    Premium_delivery_time = models.PositiveIntegerField(choices=DELIVERY_CHOICES3, default=1)
    Premium_revisions = models.PositiveIntegerField(choices=REVISION_CHOICES3, default=1)
    Premium_source_file = models.BooleanField(default=False)
    Premium_price = models.IntegerField(default=0,validators=[MinValueValidator(150)])

class Description(models.Model):
    overview = models.ForeignKey(Overview, on_delete=models.CASCADE)
    description = models.TextField(default="")

class Question(models.Model):
    QUESTION_TYPES = [
        ('text', 'Text Answer'),
        ('textarea', 'Text Area'),
        ('choices', 'Multiple Choice'),
    ]

    overview = models.ForeignKey(Overview, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200, default="")
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    text = models.TextField(max_length=200, default="")
    choices = models.CharField(max_length=10, default="")
    allow_multiple_selection = models.BooleanField(default=False)

    def is_multiple_choice(self):
        return self.question_type == 'choices'

class Gallery(models.Model):
    overview = models.ForeignKey(Overview, on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='image/',blank=True, null=True)
    image2 = models.ImageField(upload_to='image/',blank=True, null=True)
    image3 = models.ImageField(upload_to='image/',blank=True, null=True)
    video = models.FileField(upload_to='videos/',blank=True, null=True)

class RatingService(models.Model):
    overview = models.ForeignKey(Overview, on_delete=models.CASCADE, default=None)
    review_rating = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    reviewer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ratings_giver_service')
    title = models.CharField(max_length=50)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['overview', 'reviewer']

