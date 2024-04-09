from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/' , blank=True)
    country = models.CharField(max_length=50)  # For storing country information
    state = models.CharField(max_length=50)    # For storing state information
    website_link = models.URLField(blank=True, null=True)
    about_me = models.TextField()
    overall_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    skills = models.ManyToManyField('Skill', related_name='user_profiles')

    def __str__(self):
        return self.user.username

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Certification(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='certifications')
    title = models.CharField(max_length=100)
    issuing_organization = models.CharField(max_length=100)
    issue_date = models.DateField()

class Language(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='languages')
    language = models.CharField(max_length=50)
    PROFICIENCY_CHOICES = (
        ('novice', 'Novice'),
        ('basic', 'Basic'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('proficient', 'Proficient'),
    )
    proficiency = models.CharField(max_length=12, choices=PROFICIENCY_CHOICES)

class RatingSeller(models.Model):
    review_rating = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    reviewer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ratings_given')
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ratings_received')
    title = models.CharField(max_length=50)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ['seller', 'reviewer']


    




