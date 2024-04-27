
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import OverviewForm, BasicPackageForm, StandardPackageForm, PremiumPackageForm, DescriptionForm, QuestionForm, GalleryForm
from Home.models import UserProfile
from django.shortcuts import render, redirect, get_object_or_404
from .models import Overview, BasicPackage, StandardPackage, PremiumPackage, Description, Question, Gallery, RatingService
from django.http import HttpResponseForbidden


@login_required()
def create_job_profile(request, identifier):
    user = get_object_or_404(User, username=identifier)

    current_user = request.user
    if identifier == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")

    if request.method == 'POST':
        overview_form = OverviewForm(request.POST)
        basic_package_form = BasicPackageForm(request.POST, prefix='basic')
        standard_package_form = StandardPackageForm(
            request.POST, prefix='standard')
        premium_package_form = PremiumPackageForm(
            request.POST, prefix='premium')

        # Uncomment these lines if you have additional forms for description, question, and gallery
        description_form = DescriptionForm(request.POST)
        question_form = QuestionForm(request.POST)
        gallery_form = GalleryForm(request.POST, request.FILES)

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
def delete_service(request, username, overview_id):
    overview = get_object_or_404(Overview, pk=overview_id, user=request.user)
    user = get_object_or_404(User, username=username)
    current_user = request.user
    if username == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")

# Handling the deletion of the overview object if the request method is POST
    if request.method == 'POST':
        if 'confirm_delete' in request.POST:
            overview.delete()  # Deleting the overview object
            # Redirecting to the homepage after successful deletion
            return redirect('IntroHome')
        else:
            # Redirecting to the homepage if the deletion is not confirmed
            return redirect('IntroHome')

    return render(request, 'delete_service.html', {'overview': overview})


@login_required()
def edit_service(request, username, overview_id):
    overview = get_object_or_404(Overview, pk=overview_id)
    user = get_object_or_404(User, username=username)
    current_user = request.user

   # Checking if the provided username matches the username of the current logged-in user
    # and if the overview belongs to the current user
    if username == current_user.username and overview.user_id == current_user.id:
        pass
    else:
        return HttpResponseForbidden("Access Denied")
# Retrieving related objects
    basic_package = BasicPackage.objects.get(overview=overview)
    standard_package = StandardPackage.objects.get(overview=overview)
    premium_package = PremiumPackage.objects.get(overview=overview)
    description = Description.objects.get(overview=overview)
    question = Question.objects.get(overview=overview)
    gallery = Gallery.objects.get(overview=overview)

# Initializing form instances with retrieved objects
    overview_form = OverviewForm(instance=overview)
    basic_package_form = BasicPackageForm(instance=basic_package)
    standard_package_form = StandardPackageForm(instance=standard_package)
    premium_package_form = PremiumPackageForm(instance=premium_package)
    description_form = DescriptionForm(instance=description)
    question_form = QuestionForm(instance=question)
    gallery_form = GalleryForm(instance=gallery)

 # Handling form submission
    if request.method == 'POST':
        overview_form = OverviewForm(request.POST, instance=overview)
        basic_package_form = BasicPackageForm(
            request.POST, instance=basic_package)
        standard_package_form = StandardPackageForm(
            request.POST, instance=standard_package)
        premium_package_form = PremiumPackageForm(
            request.POST, instance=premium_package)
        description_form = DescriptionForm(request.POST, instance=description)
        question_form = QuestionForm(request.POST, instance=question)
        gallery_form = GalleryForm(
            request.POST, request.FILES, instance=gallery)
# Validating forms and saving data if valid
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

            # Redirecting to the homepage after successful form submission
            return redirect('IntroHome')

    # Creating a context dictionary with form instances
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
def view_service_profile(request, overview_id):
    overview = get_object_or_404(Overview, pk=overview_id)
    user_profile = UserProfile.objects.get(user=overview.user.id)
    basic_packages = BasicPackage.objects.filter(overview=overview)
    standardpackage = StandardPackage.objects.filter(overview=overview)
    premiumpackage = PremiumPackage.objects.filter(overview=overview)
    description = Description.objects.filter(overview=overview)
    question = Question.objects.filter(overview=overview)
    gallery = Gallery.objects.filter(overview=overview)
    rating_service = RatingService.objects.filter(overview=overview)
    re_profile = UserProfile.objects.get(user=request.user)



    #  # Calculating the overall rating of the service
    total_review_sum = sum(review.review_rating for review in rating_service if review.review_rating is not None)
    overview.overall_rating = round(total_review_sum / rating_service.count()) if rating_service.count() > 0 else 0
    overview.save()

    # Handling form submission for rating and reviews
    if request.method == 'POST':
        rating_value = request.POST.get('rg1')
        title = request.POST.get('review_title')
        review_text = request.POST.get('review_message')
        
        # Checking if the user has already submitted a review
        existing_review = RatingService.objects.filter(overview=overview, reviewer=re_profile).first()
        if existing_review:
            # Updating existing review
            existing_review.review_rating = rating_value
            existing_review.title = title
            existing_review.review = review_text
            existing_review.save()
        else:
            # Creating new review
            RatingService.objects.create(
                overview=overview,
                reviewer=re_profile,
                review_rating=rating_value,
                title=title,
                review=review_text
            )
    else:
        print('No values received from the form')

    # Creating context dictionary with necessary data
    context = {
        'service_profile': overview,
        'basic_packages': basic_packages,
        'standardpackage': standardpackage,
        'premiumpackage': premiumpackage,
        'description': description,
        'question': question,
        'gallery': gallery,
        'user_profile': user_profile,
        'rating_service': rating_service,
        're_profile': re_profile,
        'count_review': rating_service.count(),
    }
    
    # Rendering the view_service_profile.html template with the context
    return render(request, 'view_service_profile.html', context)
