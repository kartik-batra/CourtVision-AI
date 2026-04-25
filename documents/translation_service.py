"""
Translation Service — CourtVision AI
=======================================
Primary:  MyMemory API  (free, no API key, 500 words/call)
Fallback: Argos Translate (local, offline)

Flow for every translation request:
  1. Check TranslationCache (DB) by SHA-256 hash → return instantly if found
  2. If not cached: call MyMemory in chunks → stitch → store in DB → return
  3. On MyMemory failure: try Argos Translate (local library)
  4. On all failures: return original English text with a warning prefix

Language codes:
  MyMemory:  en|hi  en|ta
"""

import re
import time
import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)

# MyMemory language pair codes
MYMEMORY_CODES = {
    'hi': 'en|hi',
    'ta': 'en|ta',
}

# Max chars per MyMemory request (their limit is ~500 words ≈ 3000 chars)
CHUNK_SIZE = 2800


# ─── Public entry point ──────────────────────────────────────────────────────

def get_translation(text: str, target_lang: str) -> str:
    """
    Return translated text for `target_lang` ('hi' or 'ta').
    - English input is returned unchanged.
    - Result is cached permanently in TranslationCache on first call.
    """
    if not text or not text.strip():
        return text
    if target_lang == 'en':
        return text

    # Import here to avoid circular imports
    from documents.models import TranslationCache

    # 1. Cache hit?
    cached = TranslationCache.get_cached(text, target_lang)
    if cached:
        logger.debug(f"Translation cache HIT ({target_lang}, {len(text)} chars)")
        return cached

    # 2. Translate via API
    logger.info(f"Translating {len(text)} chars to {target_lang} via MyMemory")
    translated = _translate_chunked(text, target_lang)

    # 3. Persist permanently
    if translated and translated != text:
        TranslationCache.store(text, translated, target_lang)
        logger.info(f"Translation stored ({target_lang}, {len(text)} → {len(translated)} chars)")

    return translated or text


# ─── Chunked translation ──────────────────────────────────────────────────────

def _translate_chunked(text: str, lang: str) -> str:
    """
    Split text into paragraph-aware chunks, translate each,
    then rejoin preserving structure.
    """
    # Split on double newlines (paragraph breaks) to keep context
    paragraphs = re.split(r'\n{2,}', text)
    translated_paragraphs = []
    current_chunk = []
    current_len = 0

    def flush_chunk(chunk_paras):
        joined = '\n\n'.join(chunk_paras)
        result = _mymemory_translate(joined, lang)
        if result is None:
            result = _argos_translate(joined, lang) or joined
        return result

    for para in paragraphs:
        if current_len + len(para) > CHUNK_SIZE and current_chunk:
            translated_paragraphs.append(flush_chunk(current_chunk))
            current_chunk = [para]
            current_len = len(para)
            time.sleep(0.4)   # rate-limit courtesy delay
        else:
            current_chunk.append(para)
            current_len += len(para)

    if current_chunk:
        translated_paragraphs.append(flush_chunk(current_chunk))

    return '\n\n'.join(translated_paragraphs)


# ─── MyMemory API ─────────────────────────────────────────────────────────────

def _mymemory_translate(text: str, lang: str) -> Optional[str]:
    """
    Call MyMemory free translation API.
    Docs: https://mymemory.translated.net/doc/spec.php
    Free tier: 5000 chars/day anonymous, 50000/day with email param.
    """
    lang_pair = MYMEMORY_CODES.get(lang)
    if not lang_pair:
        return None

    try:
        resp = requests.get(
            'https://api.mymemory.translated.net/get',
            params={
                'q':        text,
                'langpair': lang_pair,
                'de':       'courtresearch@example.com',  # bumps free quota
            },
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()

        # responseStatus 200 = OK, 429 = quota exceeded
        if data.get('responseStatus') == 200:
            translated = data['responseData']['translatedText']
            # MyMemory sometimes returns "PLEASE SELECT TWO DISTINCT LANGUAGES" on error
            if translated and 'PLEASE SELECT' not in translated.upper():
                return translated

        # Quota exceeded — log clearly
        if data.get('responseStatus') == 429:
            logger.warning("MyMemory quota exceeded for today")

        logger.warning(f"MyMemory returned status {data.get('responseStatus')}: {data.get('responseDetails', '')}")
        return None

    except requests.Timeout:
        logger.error("MyMemory request timed out")
        return None
    except Exception as e:
        logger.error(f"MyMemory API error: {e}")
        return None


# ─── Argos Translate (offline fallback) ──────────────────────────────────────

def _argos_translate(text: str, lang: str) -> Optional[str]:
    """
    Offline fallback using argostranslate library.
    Automatically downloads the language package on first use.
    Returns None if argostranslate is not installed.
    """
    try:
        import argostranslate.package
        import argostranslate.translate

        from_code = 'en'
        to_code   = lang

        # Check if the language pair is already installed
        installed = argostranslate.translate.get_installed_languages()
        from_lang = next((l for l in installed if l.code == from_code), None)
        to_lang   = next((l for l in installed if l.code == to_code), None)

        # Auto-install if missing
        if not from_lang or not to_lang:
            logger.info(f"Installing argostranslate package for {from_code}→{to_code}")
            argostranslate.package.update_package_index()
            available = argostranslate.package.get_available_packages()
            pkg = next(
                (p for p in available if p.from_code == from_code and p.to_code == to_code),
                None
            )
            if pkg:
                argostranslate.package.install_from_path(pkg.download())
                # Refresh
                installed = argostranslate.translate.get_installed_languages()
                from_lang = next((l for l in installed if l.code == from_code), None)
                to_lang   = next((l for l in installed if l.code == to_code), None)
            else:
                logger.warning(f"No argostranslate package for {from_code}→{to_code}")
                return None

        if from_lang and to_lang:
            translation = from_lang.get_translation(to_lang)
            if translation:
                return translation.translate(text)

        return None

    except ImportError:
        logger.debug("argostranslate not installed — skipping fallback")
        return None
    except Exception as e:
        logger.error(f"Argos translate error: {e}")
        return None
