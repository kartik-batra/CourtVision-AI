from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from .forms import LoginForm, RegisterForm, SetNewPasswordForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('documents:list')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('documents:list')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    else:
        form = LoginForm()
    return render(request, 'authentication/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('documents:list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to CourtResearch AI.')
            return redirect('documents:list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'authentication/register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('authentication:login')


@login_required
def profile_view(request):
    return render(request, 'authentication/profile.html', {'user': request.user})

# ── Password Reset — Step 1: Enter email ─────────────────────────────────────

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        if not email:
            messages.error(request, 'Please enter your email address.')
            return render(request, 'authentication/password_reset.html')
        users = User.objects.filter(email__iexact=email)
        if users.exists():
            _send_reset_email(request, users.first())
        return redirect('authentication:password_reset_done')
    return render(request, 'authentication/password_reset.html')


def _send_reset_email(request, user):
    uid       = urlsafe_base64_encode(force_bytes(user.pk))
    token     = default_token_generator.make_token(user)
    reset_url = request.build_absolute_uri(
        f"/auth/password-reset/confirm/{uid}/{token}/"
    )
    subject   = "Reset your CourtResearch AI password"
    html_body = render_to_string('authentication/email/password_reset_email.html', {
        'user': user, 'reset_url': reset_url,
        'protocol': 'https' if request.is_secure() else 'http',
        'domain': request.get_host(),
    })
    plain_body = (
        f"Hello {user.get_full_name() or user.username},\n\n"
        f"Reset link (valid 1 hour):\n{reset_url}\n\n"
        f"If you did not request this, ignore this email.\n\nCourtResearch AI"
    )
    try:
        send_mail(
            subject=subject, message=plain_body, html_message=html_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email], fail_silently=False,
        )
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Password reset email failed: {e}")


# ── Password Reset — Step 2: Done ────────────────────────────────────────────

def password_reset_done(request):
    return render(request, 'authentication/password_reset_done.html')


# ── Password Reset — Step 3: Set new password ─────────────────────────────────

def password_reset_confirm(request, uidb64, token):
    try:
        uid  = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        return render(request, 'authentication/password_reset_invalid.html', status=400)

    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            messages.success(request, 'Your password has been reset. You can now sign in.')
            return redirect('authentication:password_reset_complete')
    else:
        form = SetNewPasswordForm()

    return render(request, 'authentication/password_reset_confirm.html', {
        'form': form, 'uidb64': uidb64, 'token': token, 'user': user,
    })


# ── Password Reset — Step 4: Complete ────────────────────────────────────────

def password_reset_complete(request):
    return render(request, 'authentication/password_reset_complete.html')

# ── Language Selection ────────────────────────────────────────────────────────

@login_required
def set_language(request):
    """Save user language preference and redirect back."""
    lang = request.POST.get('language', 'en')
    if lang not in ('en', 'hi', 'ta'):
        lang = 'en'
    try:
        profile = request.user.profile
        profile.language = lang
        profile.save(update_fields=['language'])
    except Exception:
        pass
    # Store in session too for immediate effect
    request.session['user_language'] = lang
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)