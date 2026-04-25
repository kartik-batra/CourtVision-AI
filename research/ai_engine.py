"""
CourtResearch AI Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summarization strategy: Map-Reduce over the FULL document text.

  1. Extract ALL text from the uploaded file (no truncation).
  2. Split into token-safe chunks (~3000 words each).
  3. MAP   — Groq LLM summarizes each chunk independently.
  4. REDUCE — Groq LLM merges all chunk summaries into one
              final comprehensive legal summary.
  5. Persist the final summary permanently in the DB.

LangGraph orchestrates the pipeline as a typed state machine.
FAISS stores per-chunk embeddings for RAG queries later.
"""
import os
import json
import logging
from typing import TypedDict, List, Optional
from pathlib import Path

from django.conf import settings

logger = logging.getLogger(__name__)


# ─── LangGraph State ─────────────────────────────────────────────────────────

class ResearchState(TypedDict):
    document_id:    int
    document_title: str
    document_text:  str          # full raw extracted text
    chunks:         List[str]    # word-level chunks for MAP phase
    chunk_summaries: List[str]   # per-chunk summaries from MAP phase
    summary:        Optional[str]  # final merged summary (REDUCE)
    key_findings:   Optional[str]  # JSON string
    query:          Optional[str]
    relevant_chunks: List[str]
    final_answer:   Optional[str]
    error:          Optional[str]


# ─── Text Extraction ─────────────────────────────────────────────────────────

def extract_text_from_pdf(file_path: str) -> str:
    """Extract ALL text from PDF — every page, no truncation."""
    try:
        import pdfplumber
        pages = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t and t.strip():
                    pages.append(t.strip())
        text = "\n\n".join(pages)
        logger.info(f"pdfplumber extracted {len(text)} chars from {len(pages)} pages")
        return text
    except Exception as e:
        logger.warning(f"pdfplumber failed ({e}), falling back to PyPDF2")
        try:
            import PyPDF2
            pages = []
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    t = page.extract_text()
                    if t:
                        pages.append(t.strip())
            text = "\n\n".join(pages)
            logger.info(f"PyPDF2 extracted {len(text)} chars")
            return text
        except Exception as e2:
            logger.error(f"PDF extraction completely failed: {e2}")
            return ""


def extract_text_from_file(file_path: str) -> str:
    """Route to the correct extractor based on file extension."""
    ext = Path(file_path).suffix.lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.txt':
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        logger.info(f"Plain-text: extracted {len(text)} chars")
        return text
    elif ext in ('.doc', '.docx'):
        try:
            import docx
            doc = docx.Document(file_path)
            text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
            logger.info(f"docx: extracted {len(text)} chars")
            return text
        except Exception as e:
            logger.error(f"docx extraction failed: {e}")
            return ""
    else:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception:
            return ""


# ─── Chunking ─────────────────────────────────────────────────────────────────

CHUNK_WORDS   = 2800   # words per MAP chunk  (~3500 tokens, safe for 8k context)
CHUNK_OVERLAP = 150    # word overlap between consecutive chunks

def split_into_chunks(text: str,
                      chunk_words: int = CHUNK_WORDS,
                      overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into overlapping word-level chunks."""
    if not text or not text.strip():
        return []
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunk = " ".join(words[i : i + chunk_words])
        if chunk.strip():
            chunks.append(chunk)
        i += chunk_words - overlap
    logger.info(f"Text split into {len(chunks)} chunks "
                f"({len(words)} words, chunk_size={chunk_words})")
    return chunks


# ─── FAISS Vector Store ───────────────────────────────────────────────────────

def create_vector_store(document_id: int, text: str) -> Optional[str]:
    """Build a per-document FAISS index from ALL text chunks."""
    try:
        import faiss, numpy as np
        from sentence_transformers import SentenceTransformer

        chunks = split_into_chunks(text)
        if not chunks:
            return None

        logger.info(f"Building FAISS index for doc {document_id} ({len(chunks)} chunks)")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = np.array(
            model.encode(chunks, show_progress_bar=False, batch_size=32)
        ).astype('float32')

        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)

        store_dir = Path(settings.VECTOR_STORE_PATH) / str(document_id)
        store_dir.mkdir(parents=True, exist_ok=True)
        faiss.write_index(index, str(store_dir / 'index.faiss'))
        with open(store_dir / 'chunks.json', 'w', encoding='utf-8') as f:
            json.dump(chunks, f, ensure_ascii=False)

        logger.info(f"FAISS index saved to {store_dir}")
        return str(store_dir)
    except Exception as e:
        logger.error(f"Vector store creation failed: {e}")
        return None


def search_vector_store(store_path: str, query: str, top_k: int = 5) -> List[str]:
    """Semantic search over the document's FAISS index."""
    try:
        import faiss, numpy as np
        from sentence_transformers import SentenceTransformer

        idx_path    = Path(store_path) / 'index.faiss'
        chunks_path = Path(store_path) / 'chunks.json'
        if not idx_path.exists() or not chunks_path.exists():
            return []

        index = faiss.read_index(str(idx_path))
        with open(chunks_path, 'r', encoding='utf-8') as f:
            chunks = json.load(f)

        model = SentenceTransformer('all-MiniLM-L6-v2')
        q_emb = np.array(model.encode([query])).astype('float32')
        _, idxs = index.search(q_emb, min(top_k, len(chunks)))
        return [chunks[i] for i in idxs[0] if 0 <= i < len(chunks)]
    except Exception as e:
        logger.error(f"Vector search failed: {e}")
        return []


# ─── Groq LLM helper ─────────────────────────────────────────────────────────

def call_groq(system_prompt: str, user_message: str,
              max_tokens: int = 2048, model: str = "meta-llama/llama-4-scout-17b-16e-instruct") -> str:
    """Single Groq API call. Returns the assistant's text."""
    try:
        from groq import Groq
        api_key = settings.GROQ_API_KEY
        if not api_key:
            return ("⚠️ Groq API key not configured. "
                    "Please add GROQ_API_KEY to your .env file.")
        client = Groq(api_key=api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_message},
            ],
            max_tokens=max_tokens,
            temperature=0.15,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Groq API call failed: {e}")
        return f"⚠️ AI service temporarily unavailable: {e}"


# ─── LangGraph Nodes ─────────────────────────────────────────────────────────

# ---------- Node 1: chunk the full text ----------
def node_chunk_document(state: ResearchState) -> ResearchState:
    """Split the FULL extracted text into chunks for MAP phase."""
    text = state.get('document_text', '')
    state['chunks'] = split_into_chunks(text)
    state['chunk_summaries'] = []
    logger.info(f"node_chunk_document → {len(state['chunks'])} chunks")
    return state


# ---------- Node 2: MAP — summarise every chunk ----------
def node_map_summarize(state: ResearchState) -> ResearchState:
    """
    MAP phase: send EACH chunk to Groq independently and collect
    a focused summary for that passage.
    """
    chunks  = state.get('chunks', [])
    title   = state.get('document_title', 'Legal Document')
    summaries = []

    system_prompt = (
        "You are a senior legal analyst specialising in commercial court proceedings. "
        "You will be given a passage from a legal document. "
        "Write a concise factual summary of this passage in 150–250 words, "
        "preserving all parties, dates, legal principles, amounts, and rulings. "
        "Do NOT add commentary; stick strictly to what is in the passage."
    )

    total = len(chunks)
    logger.info(f"MAP phase: summarising {total} chunks for '{title}'")

    for idx, chunk in enumerate(chunks):
        logger.info(f"  MAP chunk {idx+1}/{total} ({len(chunk.split())} words)")
        user_msg = (
            f"Document title: {title}\n"
            f"Passage {idx+1} of {total}:\n\n"
            f"{chunk}\n\n"
            "Write a concise summary of this passage."
        )
        summary = call_groq(system_prompt, user_msg, max_tokens=400)
        summaries.append(summary)

    state['chunk_summaries'] = summaries
    logger.info(f"MAP phase complete — {len(summaries)} chunk summaries collected")
    return state


# ---------- Node 3: REDUCE — merge all chunk summaries ----------
def node_reduce_summary(state: ResearchState) -> ResearchState:
    """
    REDUCE phase: combine ALL chunk summaries into one final
    comprehensive legal summary. This is what gets stored permanently.
    """
    chunk_summaries = state.get('chunk_summaries', [])
    title           = state.get('document_title', 'Legal Document')

    if not chunk_summaries:
        state['summary'] = "No text could be extracted from this document."
        return state

    # Build the combined intermediate text
    combined = "\n\n---\n\n".join(
        f"[Section {i+1}]\n{s}" for i, s in enumerate(chunk_summaries)
    )

    system_prompt = (
        "You are a senior legal analyst specialising in Indian commercial court matters. "
        "You have been given section-by-section summaries of a full legal document. "
        "Your job is to synthesise them into ONE comprehensive, well-structured "
        "legal summary that covers the entire document — not just the beginning. "
        "Use markdown headings. Be thorough, precise, and professional."
    )

    # If the combined summaries are large, send in one shot (they are already
    # compressed and well within the 8k context limit).
    user_msg = (
        f'# Document: "{title}"\n\n'
        f"The following are section-by-section summaries of the complete document "
        f"({len(chunk_summaries)} sections total):\n\n"
        f"{combined}\n\n"
        "Now write the final comprehensive summary covering the FULL document. "
        "Structure it as:\n"
        "1. **Document Overview** — type, parties, jurisdiction, date\n"
        "2. **Background & Context** — facts leading to the dispute\n"
        "3. **Core Legal Issues** — main questions before the court\n"
        "4. **Arguments of the Parties** — plaintiff/defendant positions\n"
        "5. **Court's Analysis & Findings** — reasoning and holdings\n"
        "6. **Final Order / Judgment** — decisions, reliefs granted/refused\n"
        "7. **Commercial & Legal Implications** — significance and precedent\n"
        "8. **Key Dates & Deadlines** — important timelines"
    )

    logger.info(f"REDUCE phase: merging {len(chunk_summaries)} summaries → final summary")
    final_summary = call_groq(system_prompt, user_msg, max_tokens=2500)
    state['summary'] = final_summary
    logger.info("REDUCE phase complete — final summary generated")
    return state


# ---------- Node 4: Extract structured key findings ----------
def node_extract_findings(state: ResearchState) -> ResearchState:
    """
    Extract structured key legal findings from the FINAL summary
    (not a truncated chunk), so the findings cover the whole document.
    """
    summary = state.get('summary', '')
    title   = state.get('document_title', 'Legal Document')

    if not summary or summary.startswith("⚠️") or summary.startswith("No text"):
        state['key_findings'] = "[]"
        return state

    system_prompt = (
        "You are a legal research expert. "
        "Extract the most important legal findings from the provided document summary. "
        "Return ONLY a valid JSON array — no markdown fences, no extra text."
    )
    user_msg = (
        f'Document: "{title}"\n\n'
        f"Summary:\n{summary[:4000]}\n\n"
        'Return a JSON array of up to 8 objects, each with exactly these keys:\n'
        '"finding"        — the specific legal finding or holding (1–2 sentences)\n'
        '"legal_principle" — the legal doctrine or principle applied\n'
        '"significance"   — why this matters commercially or legally\n\n'
        'Example: [{"finding":"...","legal_principle":"...","significance":"..."}]'
    )

    raw = call_groq(system_prompt, user_msg, max_tokens=1200)

    # Robust JSON extraction
    try:
        start = raw.find('[')
        end   = raw.rfind(']') + 1
        if start != -1 and end > start:
            parsed = json.loads(raw[start:end])
            state['key_findings'] = json.dumps(parsed)
        else:
            raise ValueError("No JSON array found in response")
    except Exception as e:
        logger.warning(f"key_findings JSON parse failed: {e}. Storing raw.")
        state['key_findings'] = json.dumps([{
            "finding": raw[:500],
            "legal_principle": "See full summary",
            "significance": "Extracted from complete document"
        }])

    return state


# ---------- Node 5: Answer a research query ----------
def node_answer_query(state: ResearchState) -> ResearchState:
    """RAG: retrieve relevant chunks from FAISS, then answer with Groq."""
    query  = state.get('query')
    chunks = state.get('relevant_chunks', [])

    if not query:
        state['final_answer'] = None
        return state

    context = (
        "\n\n---\n\n".join(chunks[:4])
        if chunks
        else (state.get('document_text', '') or '')[:4000]
    )

    system_prompt = (
        "You are an expert commercial court legal researcher. "
        "Answer questions precisely based on the provided document context. "
        "Cite specific sections or passages when possible. "
        "If the answer is not in the context, say so clearly."
    )
    user_msg = (
        f"QUERY: {query}\n\n"
        f"DOCUMENT CONTEXT:\n{context}\n\n"
        "Provide a comprehensive answer with:\n"
        "• Direct answer to the query\n"
        "• Supporting evidence from the document\n"
        "• Relevant legal principles\n"
        "• Practical implications"
    )

    state['final_answer'] = call_groq(system_prompt, user_msg, max_tokens=1400)
    return state


# ─── LangGraph Workflow ───────────────────────────────────────────────────────

def build_summarization_graph():
    """
    Build the document-processing pipeline:
      chunk → map_summarize → reduce_summary → extract_findings
    """
    try:
        from langgraph.graph import StateGraph, END

        wf = StateGraph(ResearchState)
        wf.add_node("chunk",            node_chunk_document)
        wf.add_node("map_summarize",    node_map_summarize)
        wf.add_node("reduce_summary",   node_reduce_summary)
        wf.add_node("extract_findings", node_extract_findings)

        wf.set_entry_point("chunk")
        wf.add_edge("chunk",            "map_summarize")
        wf.add_edge("map_summarize",    "reduce_summary")
        wf.add_edge("reduce_summary",   "extract_findings")
        wf.add_edge("extract_findings", END)

        return wf.compile()
    except Exception as e:
        logger.error(f"Failed to build summarization graph: {e}")
        return None


def build_query_graph():
    """Lightweight graph for answering a single research query."""
    try:
        from langgraph.graph import StateGraph, END
        wf = StateGraph(ResearchState)
        wf.add_node("answer_query", node_answer_query)
        wf.set_entry_point("answer_query")
        wf.add_edge("answer_query", END)
        return wf.compile()
    except Exception as e:
        logger.error(f"Failed to build query graph: {e}")
        return None


# ─── Public API ──────────────────────────────────────────────────────────────

def process_document(document_id: int, file_path: str, title: str) -> dict:
    """
    Called on every upload. Runs the full pipeline:
      1. Extract ALL text (no truncation)
      2. Build FAISS vector store
      3. Map-Reduce summarization of the COMPLETE document via LangGraph
      4. Extract key legal findings
    Returns a dict suitable for direct storage in Document model fields.
    """
    # ── Step 1: Extract full text ────────────────────────────────────────────
    logger.info(f"[doc {document_id}] Extracting text from: {file_path}")
    text = extract_text_from_file(file_path)
    word_count = len(text.split()) if text else 0
    logger.info(f"[doc {document_id}] Extracted {len(text)} chars / {word_count} words")

    if not text.strip():
        logger.warning(f"[doc {document_id}] No text extracted — returning empty result")
        return {
            'extracted_text': '',
            'summary': '⚠️ No text could be extracted from this document. '
                       'Ensure the file is a readable PDF or text file.',
            'key_findings': '[]',
            'vector_store_path': '',
            'word_count': 0,
            'chunk_count': 0,
        }

    # ── Step 2: FAISS vector store ────────────────────────────────────────────
    logger.info(f"[doc {document_id}] Building FAISS vector store")
    vector_path = create_vector_store(document_id, text)

    # ── Step 3 & 4: LangGraph map-reduce summarization ───────────────────────
    graph = build_summarization_graph()
    chunks = split_into_chunks(text)

    initial_state: ResearchState = {
        'document_id':     document_id,
        'document_title':  title,
        'document_text':   text,
        'chunks':          [],
        'chunk_summaries': [],
        'summary':         None,
        'key_findings':    None,
        'query':           None,
        'relevant_chunks': [],
        'final_answer':    None,
        'error':           None,
    }

    if graph:
        try:
            logger.info(f"[doc {document_id}] Running LangGraph map-reduce pipeline "
                        f"({len(chunks)} chunks)")
            result = graph.invoke(initial_state)
            logger.info(f"[doc {document_id}] LangGraph pipeline complete")
        except Exception as e:
            logger.error(f"[doc {document_id}] LangGraph failed: {e} — running fallback")
            result = node_chunk_document(initial_state)
            result = node_map_summarize(result)
            result = node_reduce_summary(result)
            result = node_extract_findings(result)
    else:
        logger.warning(f"[doc {document_id}] LangGraph unavailable — running nodes directly")
        result = node_chunk_document(initial_state)
        result = node_map_summarize(result)
        result = node_reduce_summary(result)
        result = node_extract_findings(result)

    return {
        'extracted_text':   text,
        'summary':          result.get('summary') or 'Summary generation failed.',
        'key_findings':     result.get('key_findings') or '[]',
        'vector_store_path': vector_path or '',
        'word_count':       word_count,
        'chunk_count':      len(chunks),
    }


def research_query(document_id: int, vector_store_path: str,
                   document_text: str, document_title: str, query: str) -> dict:
    """
    Answer a user research query using FAISS retrieval + Groq.
    """
    chunks = []
    if vector_store_path:
        chunks = search_vector_store(vector_store_path, query)

    graph = build_query_graph()
    state: ResearchState = {
        'document_id':     document_id,
        'document_title':  document_title,
        'document_text':   document_text,
        'chunks':          [],
        'chunk_summaries': [],
        'summary':         None,
        'key_findings':    None,
        'query':           query,
        'relevant_chunks': chunks,
        'final_answer':    None,
        'error':           None,
    }

    if graph:
        try:
            result = graph.invoke(state)
        except Exception as e:
            logger.error(f"Query graph failed: {e}")
            result = node_answer_query(state)
    else:
        result = node_answer_query(state)

    return {
        'answer':  result.get('final_answer') or 'Could not generate an answer.',
        'sources': chunks[:4],
    }
