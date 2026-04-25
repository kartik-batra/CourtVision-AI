import os
import json
import threading
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.db.models import Q
from .models import Document
from .forms import DocumentUploadForm

logger = logging.getLogger(__name__)


# ─── Permission helpers ───────────────────────────────────────────────────────

def superuser_required(view_func):
    """Decorator: only superusers may proceed; others get 403 page."""
    from functools import wraps
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.conf import settings
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        if not request.user.is_superuser:
            return render(request, 'errors/403.html', status=403)
        return view_func(request, *args, **kwargs)
    return wrapper


def all_documents_qs():
    """All documents — superusers upload them, everyone can see them."""
    return Document.objects.all()


# ─── Markdown stripping ───────────────────────────────────────────────────────

import re as _re

def _strip_markdown(text: str) -> str:
    """Remove markdown syntax for plain-text display in search snippets."""
    text = _re.sub(r'^#{1,6}\s*', '', text, flags=_re.MULTILINE)
    text = _re.sub(r'\*{1,3}([^*\n]+)\*{1,3}', r'\1', text)
    text = _re.sub(r'_{1,3}([^_\n]+)_{1,3}', r'\1', text)
    text = _re.sub(r'`[^`]+`', '', text)
    text = _re.sub(r'^\s*[-*+]\s+', '', text, flags=_re.MULTILINE)
    text = _re.sub(r'^\s*\d+\.\s+', '', text, flags=_re.MULTILINE)
    text = _re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = _re.sub(r'\n+', ' ', text)
    text = _re.sub(r'\s{2,}', ' ', text)
    return text.strip()


# ─── Background document processing ──────────────────────────────────────────

def process_document_async(document_id):
    from research.ai_engine import process_document
    from django.utils import timezone
    try:
        doc = Document.objects.get(id=document_id)
        doc.status = 'processing'
        doc.save(update_fields=['status'])
        logger.info(f"Processing document {document_id}: {doc.title}")

        result = process_document(document_id, doc.file.path, doc.title)

        doc.extracted_text       = result['extracted_text']
        doc.summary              = result['summary']
        doc.key_findings         = result['key_findings']
        doc.vector_store_path    = result['vector_store_path']
        doc.word_count           = result.get('word_count', 0)
        doc.chunk_count          = result.get('chunk_count', 0)
        doc.page_count           = doc.extracted_text.count('\n\n') if doc.extracted_text else 0
        doc.summary_generated_at = timezone.now()
        doc.status               = 'completed'
        doc.save()
        logger.info(f"Document {document_id} processed. Words:{doc.word_count} Chunks:{doc.chunk_count}")
    except Exception as e:
        import traceback
        logger.error(f"Document {document_id} failed: {e}\n{traceback.format_exc()}")
        try:
            doc = Document.objects.get(id=document_id)
            doc.status = 'failed'
            doc.save(update_fields=['status'])
        except Exception:
            pass


# ─── Filter helper (shared by list + search) ─────────────────────────────────

def _apply_filters(qs, params):
    q        = params.get('q', '').strip()
    doc_type = params.get('type', '').strip()
    status   = params.get('status', '').strip()
    court    = params.get('court', '').strip()
    date_from = params.get('date_from', '').strip()
    date_to   = params.get('date_to', '').strip()
    sort      = params.get('sort', '-created_at').strip()

    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(case_number__icontains=q) |
            Q(court_name__icontains=q) |
            Q(description__icontains=q) |
            Q(summary__icontains=q)
        )
    if doc_type:  qs = qs.filter(document_type=doc_type)
    if status:    qs = qs.filter(status=status)
    if court:     qs = qs.filter(court_name__icontains=court)
    if date_from: qs = qs.filter(filing_date__gte=date_from)
    if date_to:   qs = qs.filter(filing_date__lte=date_to)

    allowed = ['created_at','-created_at','title','-title',
               'filing_date','-filing_date','file_size','-file_size']
    if sort in allowed:
        qs = qs.order_by(sort)
    return qs


# ─── Document List (all users) ────────────────────────────────────────────────

@login_required
def document_list(request):
    base_qs   = all_documents_qs()
    documents = _apply_filters(base_qs, request.GET)
    court_names = (
        base_qs.exclude(court_name__isnull=True).exclude(court_name='')
               .values_list('court_name', flat=True).distinct().order_by('court_name')
    )
    stats = {
        'total':      base_qs.count(),
        'completed':  base_qs.filter(status='completed').count(),
        'processing': base_qs.filter(status__in=['processing','pending']).count(),
    }
    return render(request, 'documents/list.html', {
        'documents':      documents,
        'total_results':  documents.count(),
        'court_names':    court_names,
        'document_types': Document.DOCUMENT_TYPES,
        'status_choices': Document.STATUS_CHOICES,
        'stats':          stats,
        'filters':        request.GET,
    })


# ─── Case Search (all users) ──────────────────────────────────────────────────

@login_required
def case_search(request):
    base_qs   = all_documents_qs()
    documents = _apply_filters(base_qs, request.GET)
    court_names = (
        base_qs.exclude(court_name__isnull=True).exclude(court_name='')
               .values_list('court_name', flat=True).distinct().order_by('court_name')
    )
    stats = {
        'total':     base_qs.count(),
        'completed': base_qs.filter(status='completed').count(),
        'types':     {},
    }
    for code, label in Document.DOCUMENT_TYPES:
        cnt = base_qs.filter(document_type=code).count()
        if cnt:
            stats['types'][label] = cnt

    return render(request, 'documents/search.html', {
        'documents':      documents,
        'total_results':  documents.count(),
        'court_names':    court_names,
        'document_types': Document.DOCUMENT_TYPES,
        'status_choices': Document.STATUS_CHOICES,
        'stats':          stats,
        'filters':        request.GET,
    })


@login_required
def search_ajax(request):
    base_qs   = all_documents_qs()
    documents = _apply_filters(base_qs, request.GET)
    results = []
    for doc in documents[:30]:
        results.append({
            'id':                doc.id,
            'title':             doc.title,
            'document_type':     doc.get_document_type_display(),
            'document_type_code': doc.document_type,
            'case_number':       doc.case_number or '',
            'court_name':        doc.court_name or '',
            'filing_date':       doc.filing_date.strftime('%d %b %Y') if doc.filing_date else '',
            'status':            doc.status,
            'status_display':    doc.get_status_display(),
            'file_size':         doc.get_file_size_display(),
            'created_at':        doc.created_at.strftime('%d %b %Y'),
            'has_summary':       bool(doc.summary),
            'detail_url':        f'/documents/{doc.id}/',
            'research_url':      f'/research/document/{doc.id}/' if doc.status == 'completed' else '',
            'summary_snippet':   _strip_markdown(doc.summary or '')[:220],
        })
    return JsonResponse({'results': results, 'count': len(results), 'total': base_qs.count()})


# ─── Upload (SUPERUSER ONLY) ──────────────────────────────────────────────────

@superuser_required
def document_upload(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.uploaded_by = request.user
            doc.file_size   = request.FILES['file'].size
            doc.save()
            thread = threading.Thread(target=process_document_async, args=(doc.id,))
            thread.daemon = True
            thread.start()
            messages.success(request, f'"{doc.title}" uploaded. AI analysis started.')
            return redirect('documents:detail', pk=doc.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DocumentUploadForm()
    return render(request, 'documents/upload.html', {'form': form})


# ─── Document Detail (all users, read-only) ───────────────────────────────────

@login_required
def document_detail(request, pk):
    doc = get_object_or_404(Document, id=pk)   # no uploaded_by filter — all users see it
    key_findings = []
    if doc.key_findings:
        try:
            key_findings = json.loads(doc.key_findings)
        except Exception:
            key_findings = []
    return render(request, 'documents/detail.html', {
        'document':     doc,
        'key_findings': key_findings,
    })


# ─── Delete (SUPERUSER ONLY) ──────────────────────────────────────────────────

@superuser_required
def document_delete(request, pk):
    doc = get_object_or_404(Document, id=pk)   # superuser can delete any doc
    if request.method == 'POST':
        title = doc.title
        if doc.vector_store_path and os.path.exists(doc.vector_store_path):
            import shutil
            shutil.rmtree(doc.vector_store_path, ignore_errors=True)
        doc.file.delete()
        doc.delete()
        messages.success(request, f'"{title}" deleted successfully.')
        return redirect('documents:list')
    return render(request, 'documents/delete_confirm.html', {'document': doc})


# ─── Status poll (all users) ──────────────────────────────────────────────────

@login_required
def document_status(request, pk):
    doc = get_object_or_404(Document, id=pk)
    return JsonResponse({'status': doc.status, 'has_summary': bool(doc.summary)})

# ─── Translation AJAX endpoint ────────────────────────────────────────────────

@login_required
def translate_content(request, pk):
    """
    AJAX POST: translate document summary for the requesting user's language.
    Returns cached translation if available, else translates and caches it.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    doc  = get_object_or_404(Document, id=pk)
    lang = 'en'
    try:
        lang = request.user.profile.language
    except Exception:
        pass

    if lang == 'en' or not doc.summary:
        return JsonResponse({'translated': doc.summary or '', 'cached': False, 'lang': lang})

    from documents.translation_service import get_translation
    translated = get_translation(doc.summary, lang)

    # Check if it came from cache
    from documents.models import TranslationCache
    h      = TranslationCache.make_hash(doc.summary)
    cached = TranslationCache.objects.filter(content_hash=h, target_language=lang).exists()

    return JsonResponse({
        'translated': translated,
        'cached':     cached,
        'lang':       lang,
        'chars':      len(translated),
    })