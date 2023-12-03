
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from .forms import UserProfileForm, CertificationForm, LanguageForm
from Services.models import Overview
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from .models import UserProfile, Certification, Language
from django.forms import inlineformset_factory

def IntroHome(request):

    if request.user.is_authenticated:
        username = request.user.username
        return redirect('home', username)
    else:
        return render(request, 'introHome.html')

@login_required()
def home(request, identifier):
    user = get_object_or_404(User, username=identifier)
    users = User.objects.all()
    usernames = [user.username for user in users]
    user_id = [user.id for user in users]
    user_profile = UserProfile.objects.all()
    user_service_profiles = Overview.objects.all()

    current_user = request.user
    if identifier == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")

    context = {
        'user': user,
        'user_id': user_id,
        'usernames': usernames,
        'user_profile': user_profile,
        'user_service_profiles': user_service_profiles
    }
    return render(request, 'home.html', context)


@login_required()
def edit_profile(request, identifier):
    user = get_object_or_404(User, username=identifier)
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    # Initialize context with common values
    current_user = request.user
    if identifier == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")
    
    context = {
        'user': user,
        'user_profile': user_profile,
    }

    if request.user != user:
        raise PermissionDenied("You are not authorized to edit this profile.")

    user_form = UserProfileForm(
        request.POST or None, request.FILES or None, instance=user_profile)

    CertificationFormSet = inlineformset_factory(
        UserProfile, Certification, form=CertificationForm, extra=1)
    certification_queryset = Certification.objects.filter(
        user_profile=user_profile)
    certification_formset = CertificationFormSet(
        request.POST or None, instance=user_profile, prefix='certifications', queryset=certification_queryset)

    LanguageFormSet = inlineformset_factory(
        UserProfile, Language, form=LanguageForm, extra=1)
    language_queryset = Language.objects.filter(user_profile=user_profile)
    language_formset = LanguageFormSet(
        request.POST or None, instance=user_profile, prefix='languages', queryset=language_queryset)

    username_taken = False
    email_taken = False

    if request.method == 'POST':
        new_username = request.POST['username']
        new_email = request.POST['email']

        username_taken = User.objects.filter(
            username=new_username).exclude(pk=user.pk).exists()
        email_taken = User.objects.filter(
            email=new_email).exclude(pk=user.pk).exists()

        if username_taken or email_taken:
            if username_taken:
                context['username_message'] = "Username is already taken. Please choose another."
            if email_taken:
                context['email_message'] = "email is already taken. Please choose another."
        else:
            user.username = new_username
            user.email = new_email
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()

            if user_form.is_valid() and certification_formset.is_valid() and language_formset.is_valid():
                user_form.save()

                # Delete marked certifications
                for form in certification_formset.deleted_forms:
                    if form.cleaned_data.get('id'):
                        form.instance.delete()

                # Delete marked languages
                for form in language_formset.deleted_forms:
                    if form.cleaned_data.get('id'):
                        form.instance.delete()

                # Save valid certifications
                for form in certification_formset:
                    if form.is_valid() and not form.cleaned_data.get('id'):
                        certification = form.save(commit=False)
                        if certification.title and certification.issuing_organization:
                            certification.user_profile = user_profile
                            certification.save()

                # Save valid languages
                for form in language_formset:
                    if form.is_valid() and not form.cleaned_data.get('id'):
                        language = form.save(commit=False)
                        if language.language and language.proficiency:
                            language.user_profile = user_profile
                            language.save()

                # Redirect to the user's Home page
                return redirect('IntroHome')

    context.update({
        'user_form': user_form,
        'certification_formset': certification_formset,
        'language_formset': language_formset,
        'username_taken': username_taken,
        'email_taken': email_taken,
    })
    return render(request, 'edit_profile.html', context)

@login_required()
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    user_service_profiles = Overview.objects.filter(user=user)
    # print(user_service_profiles)

    current_user = request.user
    if username == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")
    
    context = {
        'user_profile': user_profile,
        'user_service_profiles': user_service_profiles,
    }
    return render(request, 'view_profile.html', context)

@login_required()
def view_profile_public(request,username):
    user = get_object_or_404(User, username=username)
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    user_service_profiles = Overview.objects.filter(user=user)
    print(user_service_profiles)
    context = {
        'user_profile': user_profile,
        'user_service_profiles': user_service_profiles,
    }
    print(user)
    if request.user.is_authenticated and request.user == user:
        return redirect('profile',username=request.user.username)
        
    return render(request,'view_profile_public.html',context)