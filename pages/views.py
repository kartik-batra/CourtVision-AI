from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


def home(request):
    """Public home/landing page — no login required."""
    if request.user.is_authenticated:
        # Show dashboard stats for logged-in users
        from documents.models import Document, ResearchQuery
        stats = {
            'total_docs':    Document.objects.count(),
            'analysed_docs': Document.objects.filter(status='completed').count(),
            'total_queries': ResearchQuery.objects.count(),
        }
        return render(request, 'pages/home.html', {'stats': stats})
    return render(request, 'pages/home.html', {'stats': None})


def contact(request):
    """Contact + About Us page."""
    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not all([name, email, subject, message]):
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'pages/contact.html', {'post': request.POST})

        # Send email notification
        try:
            send_mail(
                subject=f'[CourtVision AI] Contact: {subject}',
                message=f'From: {name} <{email}>\n\n{message}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER or 'admin@courtvision.ai'],
                fail_silently=True,
            )
        except Exception:
            pass

        messages.success(request, f'Thank you {name}! Your message has been sent. We\'ll get back to you soon.')
        return redirect('pages:contact')

    return render(request, 'pages/contact.html', {'post': None})
