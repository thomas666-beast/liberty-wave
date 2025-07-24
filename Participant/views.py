from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from Participant.forms import LoginForm, RegisterForm


# Auth Views

def register_view(request):
    # Redirect authenticated users to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}")

            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    # Redirect authenticated users to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect('dashboard')
        else:
            # Clean up __all__ prefix from error messages
            for error in form.errors.get('__all__', []):
                messages.error(request, str(error).replace('__all__: ', ''))
    else:
        form = LoginForm(request)

    return render(request, 'auth/login.html', {'form': form})

@login_required
def settings_view(request):
    form = PasswordChangeForm(request.user)

    return render(request, 'settings/index.html', {
        'form': form,
        'active_tab': 'password'
    })


@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('settings')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'settings/index.html', {
        'form': form,
        'active_tab': 'password'
    })

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')
