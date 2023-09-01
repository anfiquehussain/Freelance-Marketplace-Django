from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Overview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titleOverview = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True,default=0)
    search_tags = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        # Split the comma-separated tags and remove whitespace
        tags = [tag.strip() for tag in self.search_tags.split(',')]
        self.search_tags = ','.join(tags)  # Store cleaned tags
        super().save(*args, **kwargs)

class BasicPackage(models.Model):
    DELIVERY_CHOICES1 = [
        (1, "1 day"),
        (2, "2 days"),
        (3, "3 days"),
    ]
    REVISION_CHOICES1 = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
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
        (1, "1 day"),
        (2, "2 days"),
        (3, "3 days"),
    ]
    REVISION_CHOICES2 = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
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
        (1, "1 day"),
        (2, "2 days"),
        (3, "3 days"),
    ]
    REVISION_CHOICES3 = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
    ]
    overview = models.ForeignKey(Overview, on_delete=models.CASCADE)
    Premium_title = models.CharField(max_length=100, default="")
    Premium_description = models.TextField(default="")
    Premium_delivery_time = models.PositiveIntegerField(choices=DELIVERY_CHOICES3, default=1)
    Premium_revisions = models.PositiveIntegerField(choices=REVISION_CHOICES3, default=1)
    Premium_source_file = models.BooleanField(default=False)
    Premium_price = models.IntegerField(default=0,validators=[MinValueValidator(150)])

# class ExtraService(models.Model):
#     DELIVERY_CHOICES4 = [
#         (1, "1 day"),
#         (2, "2 days"),
#         (3, "3 days"),
#     ]
#     overview = models.ForeignKey(Overview, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100, default="2")
#     pricing = models.DecimalField(max_digits=10, decimal_places=2)
#     delivery_time = models.PositiveIntegerField(choices=DELIVERY_CHOICES4, default=1)

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
