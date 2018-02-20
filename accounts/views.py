from accounts.forms import UserForm, ProfileForm, EditUserForm
from accounts.models import UserProfile
from django.conf import settings
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

def home_redirect(request):
    return redirect('books:home')

def register(request):
    # if not submitting, form is a blank form
    form_list = [UserForm(), ProfileForm()]
    object_name = {'form_list': form_list}
    template_name = 'accounts/registration_form.html'

    # if submitting a form
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        # redirect to home if valid
        if all([user_form.is_valid(), profile_form.is_valid()]):
            user = user_form.save()
            profile_form = ProfileForm(request.POST, instance=user.userprofile)
            profile_form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

        # return form with error messages if invalid
        object_name = {'form_list': [user_form, profile_form]}

    return render(request, template_name, object_name)

def view_profile(request):
    object_name = {'user': request.user}

    if request.session.has_key('updated'):
        object_name['updated'] = request.session['updated']
        del request.session['updated']

    return render(request, 'accounts/profile.html', object_name)

def edit_profile(request):
    user_form = EditUserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.userprofile)
    form_list = [user_form, profile_form]
    object_name = {'form_list': form_list}

    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.userprofile)

        if all([user_form.is_valid(), profile_form.is_valid()]):
            user_form.save()
            profile_form.save()
            request.session['updated'] = True

            return redirect('accounts:view_profile')

        form_list = [user_form, profile_form]
        object_name = {'form_list': form_list}

    return render(request, 'accounts/edit_profile.html', object_name)

def password_change(request):
    form = PasswordChangeForm(user=request.user)
    object_name = {'form': form}

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            request.session['updated'] = True

            return redirect('accounts:view_profile')
        object_name = {'form': form}

    return render(request, 'accounts/password_change.html', object_name)

def view_all(request):
    user_list = UserProfile.objects.all().filter(total__gt=0)
    ordered_list = user_list.order_by('total')
    template_name = 'accounts/owe.html'
    object_name = {'list': ordered_list}

    return render(request, template_name, object_name)
