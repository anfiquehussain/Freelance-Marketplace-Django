
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import OverviewForm, BasicPackageForm,StandardPackageForm,PremiumPackageForm, DescriptionForm, QuestionForm, GalleryForm
from Home.models import UserProfile
from django.shortcuts import render, redirect, get_object_or_404
from .models import Overview, BasicPackage, StandardPackage, PremiumPackage, Description, Question, Gallery




@login_required()
def create_job_profile(request, identifier):
    user = get_object_or_404(User, username=identifier)
    
    if request.method == 'POST':
        overview_form = OverviewForm(request.POST)
        basic_package_form = BasicPackageForm(request.POST, prefix='basic')
        standard_package_form = StandardPackageForm(request.POST, prefix='standard')
        premium_package_form = PremiumPackageForm(request.POST, prefix='premium')
        
        # Uncomment these lines if you have additional forms for description, question, and gallery
        description_form = DescriptionForm(request.POST)
        question_form = QuestionForm(request.POST)
        gallery_form = GalleryForm(request.POST,request.FILES)

        if (overview_form.is_valid() and basic_package_form.is_valid() and
            standard_package_form.is_valid() and premium_package_form.is_valid() and
            description_form.is_valid() and 
            question_form.is_valid() and
            gallery_form.is_valid()):
            
            overview = overview_form.save(commit=False)
            overview.user = request.user
            overview.save()

            basic_package = basic_package_form.save(commit=False)
            basic_package.overview = overview
            basic_package.save()

            standard_package = standard_package_form.save(commit=False)
            standard_package.overview = overview
            standard_package.save()

            premium_package = premium_package_form.save(commit=False)
            premium_package.overview = overview
            premium_package.save()

            # extra_service = extra_service_form.save(commit=False)
            # extra_service.overview = overview 
            # extra_service.save()

            # Uncomment these sections if you have forms for description, question, and gallery
            description = description_form.save(commit=False)
            description.overview = overview
            description.save()

            question = question_form.save(commit=False)
            question.overview = overview
            question.save()

            
            gallery = gallery_form.save(commit=False)
            gallery.overview = overview
            gallery.save()

            print("Data saved successfully!")
            return redirect('IntroHome')  # Replace with your actual URL name
    
    else:
        overview_form = OverviewForm()
        basic_package_form = BasicPackageForm(prefix='basic')
        standard_package_form = StandardPackageForm(prefix='standard')
        premium_package_form = PremiumPackageForm(prefix='premium')
        # Uncomment these lines if you have forms for description, question, and gallery
        description_form = DescriptionForm()
        question_form = QuestionForm()
        gallery_form = GalleryForm()

    context = {
        'overview_form': overview_form,
        'basic_package_form': basic_package_form,
        'standard_package_form': standard_package_form,
        'premium_package_form': premium_package_form,
        # Uncomment these lines if you have forms for description, question, and gallery
        'description_form': description_form,
        'question_form': question_form,
        'gallery_form': gallery_form,
    }
    return render(request, 'create_service.html', context)





@login_required()
def delete_service(request, overview_id):
    overview = get_object_or_404(Overview, pk=overview_id, user=request.user)

    if request.method == 'POST':
        if 'confirm_delete' in request.POST:
            overview.delete()
            return redirect('IntroHome')  # Redirect to a success page or overview list
        else:
            return redirect('IntroHome')  # Redirect to overview details

    return render(request, 'delete_service.html', {'overview': overview})










@login_required()
def edit_service(request, overview_id):
    overview = get_object_or_404(Overview, pk=overview_id)
    basic_package = BasicPackage.objects.get(overview=overview)
    standard_package = StandardPackage.objects.get(overview=overview)
    premium_package = PremiumPackage.objects.get(overview=overview)
    description = Description.objects.get(overview=overview) 
    question = Question.objects.get(overview=overview)
    gallery = Gallery.objects.get(overview=overview)

    overview_form = OverviewForm(instance=overview)
    basic_package_form = BasicPackageForm(instance=basic_package)
    standard_package_form = StandardPackageForm(instance=standard_package)
    premium_package_form = PremiumPackageForm(instance=premium_package)
    description_form = DescriptionForm(instance=description)
    question_form = QuestionForm(instance=question)
    gallery_form = GalleryForm(instance=gallery)

    if request.method == 'POST':
        overview_form = OverviewForm(request.POST, instance=overview)
        basic_package_form = BasicPackageForm(request.POST, instance=basic_package)
        standard_package_form = StandardPackageForm(request.POST, instance=standard_package)
        premium_package_form = PremiumPackageForm(request.POST, instance=premium_package)
        description_form = DescriptionForm(request.POST, instance=description)
        question_form = QuestionForm(request.POST, instance=question)
        gallery_form = GalleryForm(request.POST, request.FILES, instance=gallery)

        if (overview_form.is_valid() and basic_package_form.is_valid() and
            standard_package_form.is_valid() and premium_package_form.is_valid() and
            description_form.is_valid() and question_form.is_valid() and
            gallery_form.is_valid()):
            
            overview_form.save()
            basic_package_form.save()
            standard_package_form.save()
            premium_package_form.save()
            description_form.save()
            question_form.save()
            gallery_form.save()

            return redirect('IntroHome')

    context = {
        'overview_form': overview_form,
        'basic_package_form': basic_package_form,
        'standard_package_form': standard_package_form,
        'premium_package_form': premium_package_form,
        'description_form': description_form,
        'question_form': question_form,
        'gallery_form': gallery_form,
    }
    return render(request, 'edit_service.html', context)




@login_required()
def view_service_profile(request,overview_id):
    overview = get_object_or_404(Overview, pk=overview_id)
    user_profile = UserProfile.objects.get(user=overview.user.id)

    basic_packages = BasicPackage.objects.filter(overview=overview)
    standardpackage = StandardPackage.objects.filter(overview=overview)
    premiumpackage = PremiumPackage.objects.filter(overview=overview)
    description = Description.objects.filter(overview=overview)
    question = Question.objects.filter(overview=overview)
    gallery = Gallery.objects.filter(overview=overview)
    context = {
        'service_profile': overview,
        'basic_packages':basic_packages,
        'standardpackage':standardpackage,
        'premiumpackage':premiumpackage,
        'description':description,
        'question':question,
        'gallery':gallery,
        'user_profile':user_profile

    }
    return render(request,'view_service_profile.html',context)









