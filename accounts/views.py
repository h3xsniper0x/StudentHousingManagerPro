from django.db import transaction
from django.contrib.auth import get_user_model, login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from applications.models import HousingApplication
from .forms import RegistrationForm, UserCreateForm, UserEditForm

User = get_user_model()


def is_admin(user):
    """Check if the user has ADMIN role."""
    return user.role == 'ADMIN'


def login_view(request):
    """
    Handle user login.

    Authenticates the user using username and password.
    Redirects to the appropriate dashboard based on the user's role.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Role-based redirection
            if user.role == 'ADMIN' or user.is_superuser:
                return redirect('admin_dashboard')
            elif user.role == 'SUPERVISOR':
                return redirect('supervisor_dashboard')
            elif user.role == 'STUDENT':
                return redirect('student_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')


def register_view(request):
    """
    Handle student registration.

    Creates a new User and a corresponding HousingApplication.
    Uses an atomic transaction to ensure data integrity.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()

                user.profile_photo = form.cleaned_data.get('profile_image')
                user.university_id_photo = form.cleaned_data.get('university_card_image')
                user.save()

                HousingApplication.objects.create(
                    student=user,
                    name=f"{user.first_name} {user.last_name}",
                    phone=user.phone,
                    age=user.age if user.age else 18,
                    governorate=user.governorate,
                    profile_image=form.cleaned_data.get('profile_image'), 
                    university_card_image=form.cleaned_data.get('university_card_image'),
                    status=HousingApplication.Status.PENDING
                )

                login(request, user)
                
                messages.success(request, 'تم إرسال طلبك وهو الآن قيد المراجعة.')
                return redirect('register_success')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def register_success_view(request):
    """
    Display registration success page.

    Redirects accepted students to their dashboard.
    """
    if request.user.role == 'STUDENT':
         application = HousingApplication.objects.filter(student=request.user).last()
         if application and application.status == HousingApplication.Status.ACCEPTED:
             return redirect('student_dashboard')
    
    return render(request, 'registration/register_success.html', {'full_page_layout': True})


@login_required
def profile_view(request):
    """View and edit user profile (Self-Service)."""
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
@user_passes_test(is_admin)
def user_list(request):
    """
    List all users (Admin only).
    """
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
@user_passes_test(is_admin)
def user_delete(request, pk):
    """
    Delete a user (Admin only).

    Prevents deletion of other admins/superusers.
    """
    user_to_delete = get_object_or_404(User, pk=pk)
    
    if user_to_delete.is_superuser or user_to_delete.role == 'ADMIN':
         messages.error(request, 'Cannot delete admin users. Change their role first.')
         return redirect('user_list')
         
    if request.method == 'POST':
        user_to_delete.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('user_list')
    return render(request, 'accounts/confirm_delete.html', {'object': user_to_delete})


@login_required
@user_passes_test(is_admin)
def user_create(request):
    """
    Create a new user (Admin only).
    """
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User "{user.username}" created with role "{user.role}".')
            return redirect('user_list')
    else:
        form = UserCreateForm()
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Add User'})


@login_required
@user_passes_test(is_admin)
def user_edit(request, pk):
    """
    Edit an existing user's role or permissions (Admin only).
    """
    user_to_edit = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            user = form.save(commit=False)
            
            if user.role != 'ADMIN':
                user.is_superuser = False
                user.is_staff = False
            else:
                user.is_staff = True
            
            user.save()
            messages.success(request, f'User "{user_to_edit.username}" updated successfully.')
            return redirect('user_list')
    else:
        form = UserEditForm(instance=user_to_edit)
    
    return render(request, 'accounts/user_form.html', {
        'form': form, 
        'title': f'Edit User: {user_to_edit.username}',
        'is_edit': True
    })


@login_required
@user_passes_test(is_admin)
def user_detail(request, pk):
    """View user details (Admin only)."""
    user = get_object_or_404(User, pk=pk)
    return render(request, 'accounts/user_detail.html', {'user': user})