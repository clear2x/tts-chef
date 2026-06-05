---
name: tts-chef-en
description: English TTS text preprocessing — abbreviation expansion (API, HTTP, JSON, etc.), number-to-English conversion (years, decimals, percentages, ordinals), symbol reading rules, punctuation normalization for speech. Use when preprocessing English text for TTS or converting technical content to spoken English.
license: MIT
---

# TTS-Chef English

## When to Use This Skill

Apply when preprocessing **English text** for TTS synthesis. Use for converting abbreviations, numbers, and symbols to their spoken English form.

**Prerequisite:** Run **tts-chef-core** pipeline steps first, then apply this skill's rules.

## Abbreviation Expansion

### Acronyms (spell out each letter)

| Abbreviation | Expansion |
|-------------|-----------|
| API | A P I |
| HTTP | H T T P |
| HTTPS | H T T P S |
| SDK | S D K |
| IDE | I D E |
| CLI | C L I |
| GUI | G U I |
| URL | U R L |
| JSON | J S O N |
| XML | X M L |
| HTML | H T M L |
| CSS | C S S |
| SQL | S Q L |
| REST | R E S T |
| JWT | J W T |
| SSH | S S H |
| SSL | S S L |
| DNS | D N S |
| CDN | C D N |
| VPN | V P N |
| TCP | T C P |
| GPU | G P U |
| CPU | C P U |
| RAM | R A M |
| SSD | S S D |
| LLM | L L M |
| GPT | G P T |
| AI | A I |
| ML | M L |
| NLP | N L P |
| DOM | D O M |
| BOM | B O M |
| npm | n p m |
| MIT | M I T |
| UUID | U U I D |
| MD5 | M D five |

### Readable Abbreviations (pronounce naturally)

| Abbreviation | Expansion |
|-------------|-----------|
| IoT | I o T |
| NoSQL | No S Q L |
| OAuth | O Auth |
| SaaS | S a a S |
| PaaS | P a a S |
| IaaS | I a a S |
| K8s | K eight S |
| i18n | i eighteen n |
| l10n | l ten n |
| a11y | a eleven y |
| GraphQL | Graph Q L |
| gRPC | g R P C |

### Tech Terms

| Term | Expansion |
|------|-----------|
| CI/CD | C I C D |
| PR | P R |
| MR | M R |
| RFC | R F C |

**Rule:** Match longest first. Apply case-insensitively. Use word boundaries to avoid matching substrings.

## Number Conversion

### Years

Split into pairs for years >= 2000, read as full number for years < 2000.

```
2024 → twenty twenty-four
1999 → nineteen ninety-nine
1900 → nineteen hundred
2008 → two thousand eight (or twenty oh eight)
```

### Decimals

Read integer part as a number, "point", then decimal part digit-by-digit.

```
3.14 → three point one four
0.618 → zero point six one eight
100.5 → one hundred point five
```

### Percentages

Read the number followed by "percent".

```
15% → fifteen percent
98.5% → ninety-eight point five percent
100% → one hundred percent
0.1% → zero point one percent
```

### Ordinals

| Pattern | Expansion |
|---------|-----------|
| 1st | first |
| 2nd | second |
| 3rd | third |
| 4th | fourth |
| 11th | eleventh |
| 21st | twenty-first |
| 22nd | twenty-second |
| 100th | one hundredth |

Regex: `(\d+)(st|nd|rd|th)` — convert the number to its ordinal word form.

## Symbol Reading

| Symbol | Context | Reading |
|--------|---------|---------|
| `@` | email, mention | at |
| `#` | heading, tag | hash (code context) / number (list context) |
| `/` | path, fraction | slash |
| `\` | escape | backslash |
| `&` | conjunction | and |
| `+` | math, addition | plus |
| `=` | assignment | equals |
| `<` | comparison | less than |
| `>` | comparison | greater than |
| `{` `}` | code | open/close brace |
| `[` `]` | code | open/close bracket |
| `(` `)` | code | open/close parenthesis |
| `|` | code | pipe |
| `_` | code | underscore |
| `*` | code | asterisk |
| `^` | code | caret |
| `~` | range | tilde / approximately |
| `$` | currency | dollars |
| `€` | currency | euros |
| `£` | currency | pounds |
| `¥` | currency | yen |

## Punctuation for TTS

### Ellipses

Normalize ellipses to a pause marker that TTS engines understand.

```
... → ... (keep as natural pause indicator)
…… → ... (normalize to standard ellipsis)
```

### Em Dashes

Treat as sentence breaks for TTS pacing.

```
word — word → word. word. (or keep dash as pause)
```

### Strip Markdown

These are handled by tts-chef-core but repeated here for English-specific guidance:
- Remove `#` headers
- Remove `*bold*` / `**bold**` markers (keep text)
- Remove `[link](url)` → keep link text only

## Agent Guidelines

- **MUST invoke `tts_preprocess.py`** (from tts-chef-core skill directory) to perform preprocessing. Do NOT apply these rules manually — the script implements them all.
- Run **tts-chef-core** pipeline first, then apply this skill
- For abbreviations, check if the context suggests a pronounceable form (e.g., "NASA" as a word vs "N A S A")
- Don't convert numbers inside code blocks or inline code (those are already handled by tts-chef-core)
- Different TTS engines handle numbers differently — some auto-expand numbers natively. Only apply these rules if the engine doesn't handle them.
