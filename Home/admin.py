from django.contrib import admin
from .models import UserProfile, Skill, Certification, Language

class CertificationInline(admin.TabularInline):
    model = Certification
    extra = 1

class LanguageInline(admin.TabularInline):
    model = Language
    extra = 1

class UserProfileAdmin(admin.ModelAdmin):
    inlines = [CertificationInline, LanguageInline]
    list_display = ('user', 'country', 'state', 'website_link', 'overall_rating')
    list_filter = ('country', 'state', 'skills')
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'country', 'state']

class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

class CertificationAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'title', 'issuing_organization', 'issue_date')
    list_filter = ('user_profile', 'issue_date')
    search_fields = ['user_profile__user__username', 'title', 'issuing_organization']

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'language', 'proficiency')
    list_filter = ('user_profile', 'proficiency')
    search_fields = ['user_profile__user__username', 'language']

# Register the admin classes
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Certification, CertificationAdmin)
admin.site.register(Language, LanguageAdmin)
