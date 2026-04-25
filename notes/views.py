import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from .models import Note
from documents.models import Document


@login_required
def notes_list(request):
    """Main notes page — list + search + filter."""
    qs = Note.objects.filter(user=request.user)

    q       = request.GET.get('q', '').strip()
    tag     = request.GET.get('tag', '').strip()
    doc_id  = request.GET.get('doc', '').strip()
    pinned  = request.GET.get('pinned', '').strip()

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(tag__icontains=q))
    if tag:
        qs = qs.filter(tag__iexact=tag)
    if doc_id:
        qs = qs.filter(document_id=doc_id)
    if pinned == '1':
        qs = qs.filter(is_pinned=True)

    # All tags for the filter bar
    all_tags = (
        Note.objects.filter(user=request.user)
        .exclude(tag='').values_list('tag', flat=True).distinct().order_by('tag')
    )
    # Documents that have notes
    doc_ids = Note.objects.filter(user=request.user).exclude(document=None)\
                  .values_list('document_id', flat=True).distinct()
    linked_docs = Document.objects.filter(id__in=doc_ids).order_by('title')

    stats = {
        'total':  Note.objects.filter(user=request.user).count(),
        'pinned': Note.objects.filter(user=request.user, is_pinned=True).count(),
        'tagged': Note.objects.filter(user=request.user).exclude(tag='').count(),
    }

    return render(request, 'notes/list.html', {
        'notes':        qs,
        'total_results': qs.count(),
        'all_tags':     all_tags,
        'linked_docs':  linked_docs,
        'stats':        stats,
        'filters':      request.GET,
        'q':            q,
        'active_tag':   tag,
        'active_doc':   doc_id,
        'documents':    Document.objects.all().order_by('title'),
    })


@login_required
def note_create(request):
    """Create a new note — GET shows form, POST saves."""
    documents = Document.objects.all().order_by('title')
    doc_id    = request.GET.get('doc') or request.POST.get('document')

    if request.method == 'POST':
        title   = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        tag     = request.POST.get('tag', '').strip()
        color   = request.POST.get('tag_color', 'gold')
        pinned  = request.POST.get('is_pinned') == 'on'
        doc_pk  = request.POST.get('document') or None

        if not title:
            messages.error(request, 'Title is required.')
            return render(request, 'notes/form.html', {
                'documents': documents, 'action': 'Create',
                'post': request.POST, 'tag_colors': Note.TAG_COLORS,
            })

        doc = None
        if doc_pk:
            try:
                doc = Document.objects.get(id=doc_pk)
            except Document.DoesNotExist:
                pass

        note = Note.objects.create(
            user=request.user, title=title, content=content,
            tag=tag, tag_color=color, is_pinned=pinned, document=doc,
        )
        messages.success(request, f'Note "{note.title}" created.')
        return redirect('notes:detail', pk=note.pk)

    preselected = None
    if doc_id:
        try:
            preselected = Document.objects.get(id=doc_id)
        except Document.DoesNotExist:
            pass

    return render(request, 'notes/form.html', {
        'documents': documents, 'action': 'Create',
        'tag_colors': Note.TAG_COLORS, 'preselected_doc': preselected,
    })


@login_required
def note_detail(request, pk):
    note     = get_object_or_404(Note, pk=pk, user=request.user)
    # Other notes on the same document
    related  = Note.objects.filter(user=request.user, document=note.document)\
                   .exclude(pk=pk)[:5] if note.document else []
    return render(request, 'notes/detail.html', {'note': note, 'related': related})


@login_required
def note_edit(request, pk):
    note      = get_object_or_404(Note, pk=pk, user=request.user)
    documents = Document.objects.all().order_by('title')

    if request.method == 'POST':
        note.title     = request.POST.get('title', '').strip() or note.title
        note.content   = request.POST.get('content', '').strip()
        note.tag       = request.POST.get('tag', '').strip()
        note.tag_color = request.POST.get('tag_color', 'gold')
        note.is_pinned = request.POST.get('is_pinned') == 'on'
        doc_pk         = request.POST.get('document') or None
        note.document  = Document.objects.get(id=doc_pk) if doc_pk else None
        note.save()
        messages.success(request, f'Note "{note.title}" updated.')
        return redirect('notes:detail', pk=note.pk)

    return render(request, 'notes/form.html', {
        'note': note, 'documents': documents,
        'action': 'Edit', 'tag_colors': Note.TAG_COLORS,
    })


@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        title = note.title
        note.delete()
        messages.success(request, f'Note "{title}" deleted.')
        return redirect('notes:notes')
    return render(request, 'notes/delete_confirm.html', {'note': note})


@login_required
@require_POST
def note_toggle_pin(request, pk):
    """AJAX: toggle pin status."""
    note          = get_object_or_404(Note, pk=pk, user=request.user)
    note.is_pinned = not note.is_pinned
    note.save(update_fields=['is_pinned'])
    return JsonResponse({'pinned': note.is_pinned, 'id': note.pk})


@login_required
@require_POST
def note_quick_save(request):
    """AJAX: create a quick note without page reload."""
    try:
        data    = json.loads(request.body)
        title   = data.get('title', '').strip()
        content = data.get('content', '').strip()
        doc_id  = data.get('document_id')
        tag     = data.get('tag', '').strip()
    except Exception:
        return JsonResponse({'error': 'Invalid request.'}, status=400)

    if not title:
        return JsonResponse({'error': 'Title is required.'}, status=400)

    doc = None
    if doc_id:
        try:
            doc = Document.objects.get(id=doc_id)
        except Document.DoesNotExist:
            pass

    note = Note.objects.create(
        user=request.user, title=title, content=content,
        tag=tag, document=doc,
    )
    return JsonResponse({
        'id':         note.pk,
        'title':      note.title,
        'preview':    note.content_preview(),
        'created_at': note.created_at.strftime('%d %b %Y, %H:%M'),
        'detail_url': f'/notes/{note.pk}/',
    })
