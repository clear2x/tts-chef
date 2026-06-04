---
name: tts-chef-auto
description: Auto language detection and dispatch for TTS preprocessing — detects Chinese, English, or Japanese text and applies the corresponding tts-chef-zh, tts-chef-en, or tts-chef-ja skill rules. Use for mixed-language text, unknown-language text, or when the user doesn't specify a language. Combines all language skills into a single preprocessing pass.
license: MIT
---

# TTS-Chef Auto Language Detection

## When to Use This Skill

Apply when preprocessing text for TTS where the **language is unknown or mixed**. This skill detects the language and dispatches to the appropriate language-specific skill.

**Triggers:** mixed-language text, unknown language, auto-detect, 混合语言, 自动检测语言.

**Related skills:** Dispatches to **tts-chef-zh** (Chinese), **tts-chef-en** (English), or **tts-chef-ja** (Japanese). Uses **tts-chef-core** for universal preprocessing.

## Language Detection Heuristic

### Step 1: Character Classification

Count characters in each category:

```python
cjk_count = count characters in Unicode ranges:
  - CJK Unified Ideographs: U+4E00-U+9FFF (Chinese kanji)
  - Hiragana: U+3040-U+309F
  - Katakana: U+30A0-U+30FF

hiragana_count = count characters in U+3040-U+309F
katakana_count = count characters in U+30A0-U+30FF
latin_count = count characters in A-Z, a-z
```

### Step 2: Classification Rules

```
total_cjk = cjk_count + hiragana_count + katakana_count
cjk_ratio = total_cjk / (total_cjk + latin_count)

if cjk_ratio > 0.6:
    # It's CJK-dominant
    kana_ratio = (hiragana_count + katakana_count) / total_cjk
    if kana_ratio > 0.3:
        language = "ja"  # Japanese has significant kana
    else:
        language = "zh"  # Chinese (mostly hanzi, little/no kana)
elif latin_count / (total_cjk + latin_count) > 0.6:
    language = "en"  # Latin-dominant
else:
    language = "mixed"  # Truly mixed, process per-sentence
```

### Step 3: Per-Sentence Detection (for mixed text)

For truly mixed text, detect language per sentence:

1. Split text into sentences (on `。` `.` `！` `!` `？` `?` `\n`)
2. For each sentence, apply the classification rules above
3. Process each sentence with its detected language's skill

## Processing Strategy

### Short Text (< 50 characters)

Use the dominant language for the entire text.

```python
language = detect(text)
processed = apply_skill(text, language)
```

### Medium Text (50-500 characters)

Detect per paragraph. Apply the dominant language per paragraph.

```python
for paragraph in text.split('\n\n'):
    language = detect(paragraph)
    processed += apply_skill(paragraph, language)
```

### Long Text (> 500 characters)

Detect per sentence for mixed content. Use the dominant language for monolingual content.

```python
# First check if the whole text is monolingual
dominant = detect(text)
if dominant != "mixed":
    processed = apply_skill(text, dominant)
else:
    # Process per sentence
    for sentence in split_sentences(text):
        language = detect(sentence)
        processed += apply_skill(sentence, language)
```

## Dispatch Table

| Detected Language | Skill to Apply |
|-------------------|---------------|
| Chinese (zh) | tts-chef-zh |
| English (en) | tts-chef-en |
| Japanese (ja) | tts-chef-ja |
| Mixed | Per-sentence dispatch |

**Always run tts-chef-core first**, regardless of detected language.

## Complete Auto Pipeline

**MUST invoke `scripts/tts_preprocess.py`** to perform all preprocessing. The script handles language detection and dispatch automatically.

```
Input text
  → python scripts/tts_preprocess.py (handles all pipeline steps, auto-detects language)
  → Output
```

## Edge Cases

| Situation | Action |
|-----------|--------|
| Code-heavy text with comments in multiple languages | Strip code first (tts-chef-core), then detect the comment language |
| Chinese text with English technical terms | Detect as Chinese, apply tts-chef-zh (which includes abbreviation expansion) |
| Japanese text with Chinese loan words | Detect as Japanese (presence of kana), apply tts-chef-ja |
| Numbers and symbols only | No language detection needed — apply tts-chef-core only |
| Empty or whitespace-only text | Return as-is |

## Agent Guidelines

- **MUST invoke `scripts/tts_preprocess.py`** to perform preprocessing. The script auto-detects language and applies the correct rules. Do NOT implement the pipeline manually.
- Default to the language the user is communicating in when uncertain
- For proper nouns that could be either Chinese or Japanese (same kanji), prefer the context language
- Don't over-classify — if 90% of text is one language, treat it as monolingual
- The 60% threshold is a guideline — adjust based on content type (technical docs tend to be more mixed)
