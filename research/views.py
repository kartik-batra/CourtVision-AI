from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
import json
from documents.models import Document, ResearchQuery


def _all_docs_qs():
    """All documents are visible to every authenticated user."""
    return Document.objects.all()


@login_required
def research_interface(request, pk):
    doc = get_object_or_404(Document, id=pk)  # any user can access
    previous_queries = ResearchQuery.objects.filter(
        user=request.user, document=doc
    ).order_by('-created_at')[:15]
    return render(request, 'research/interface.html', {
        'document':         doc,
        'previous_queries': previous_queries,
    })


@login_required
@require_POST
def submit_query(request, pk):
    doc = get_object_or_404(Document, id=pk)  # any user can query

    try:
        data  = json.loads(request.body)
        query = data.get('query', '').strip()
    except Exception:
        query = request.POST.get('query', '').strip()

    if not query:
        return JsonResponse({'error': 'Query cannot be empty.'}, status=400)
    if doc.status != 'completed':
        return JsonResponse({'error': 'Document is still being processed. Please wait.'}, status=400)

    from research.ai_engine import research_query as ai_query
    result = ai_query(
        document_id=doc.id,
        vector_store_path=doc.vector_store_path or '',
        document_text=doc.extracted_text or '',
        document_title=doc.title,
        query=query,
    )

    answer  = result['answer']
    sources = result['sources']

    # ── Translate answer if user has a non-English language set ──────────────
    user_lang = 'en'
    try:
        user_lang = request.user.profile.language
    except Exception:
        pass

    translated_answer = answer
    translation_cached = False
    if user_lang != 'en' and answer:
        from documents.translation_service import get_translation
        from documents.models import TranslationCache
        translated_answer = get_translation(answer, user_lang)
        h = TranslationCache.make_hash(answer)
        translation_cached = TranslationCache.objects.filter(
            content_hash=h, target_language=user_lang
        ).exists()

    # ── Persist original English answer permanently ───────────────────────────
    rq = ResearchQuery.objects.create(
        user=request.user,
        document=doc,
        query_text=query,
        response_text=answer,                # always store English original
        sources=sources,
        response_length=len(answer),
    )

    return JsonResponse({
        'answer':             translated_answer,   # send translated to UI
        'answer_original':    answer,              # also send English for reference
        'sources':            sources,
        'query_id':           rq.id,
        'detail_url':         f'/research/query/{rq.id}/',
        'lang':               user_lang,
        'translation_cached': translation_cached,
    })


@login_required
def query_detail(request, query_id):
    rq = get_object_or_404(ResearchQuery, id=query_id, user=request.user)
    related = ResearchQuery.objects.filter(
        user=request.user, document=rq.document
    ).exclude(id=rq.id).order_by('-created_at')[:8]
    return render(request, 'research/query_detail.html', {
        'query':   rq,
        'related': related,
    })


@login_required
def delete_query(request, query_id):
    rq = get_object_or_404(ResearchQuery, id=query_id, user=request.user)
    if request.method == 'POST':
        rq.delete()
        return redirect('research:history')
    return JsonResponse({'error': 'POST required'}, status=405)


@login_required
def research_history(request):
    base_qs = ResearchQuery.objects.filter(
        user=request.user
    ).select_related('document').order_by('-created_at')

    q      = request.GET.get('q', '').strip()
    doc_id = request.GET.get('doc', '').strip()
    sort   = request.GET.get('sort', '-created_at')

    if q:
        base_qs = base_qs.filter(
            Q(query_text__icontains=q) |
            Q(response_text__icontains=q) |
            Q(document__title__icontains=q) |
            Q(document__case_number__icontains=q)
        )
    if doc_id:
        base_qs = base_qs.filter(document_id=doc_id)
    if sort in ['-created_at', 'created_at', 'document__title']:
        base_qs = base_qs.order_by(sort)

    doc_ids = (
        ResearchQuery.objects.filter(user=request.user)
        .exclude(document__isnull=True)
        .values_list('document_id', flat=True).distinct()
    )
    docs_with_queries = Document.objects.filter(id__in=doc_ids).order_by('title')

    stats = {
        'total':          ResearchQuery.objects.filter(user=request.user).count(),
        'docs_researched': doc_ids.count(),
    }

    return render(request, 'research/history.html', {
        'queries':               base_qs,
        'total_results':         base_qs.count(),
        'documents_with_queries': docs_with_queries,
        'stats':                 stats,
        'filters':               request.GET,
        'q':                     q,
        'selected_doc':          doc_id,
    })

@login_required
def translate_query_response(request, query_id):
    """
    AJAX POST: return translated response for a saved research query.
    Checks TranslationCache first, translates + caches on miss.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    rq   = get_object_or_404(ResearchQuery, id=query_id, user=request.user)
    lang = 'en'
    try:
        lang = request.user.profile.language
    except Exception:
        pass

    if lang == 'en' or not rq.response_text:
        return JsonResponse({'translated': rq.response_text or '', 'cached': False, 'lang': lang})

    from documents.translation_service import get_translation
    from documents.models import TranslationCache

    translated = get_translation(rq.response_text, lang)
    h = TranslationCache.make_hash(rq.response_text)
    cached = TranslationCache.objects.filter(content_hash=h, target_language=lang).exists()

    return JsonResponse({
        'translated': translated,
        'cached':     cached,
        'lang':       lang,
        'chars':      len(translated),
    })
