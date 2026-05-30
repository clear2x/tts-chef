# TTS-Chef: AI Agent Skill for TTS Text Preprocessing

## Overview

tts-chef is an open-source AI Agent Skill that teaches agents how to preprocess text before TTS (Text-to-Speech) synthesis. It covers text cleaning, sentence breaking, number conversion, abbreviation expansion, multilingual handling, and optional emotion annotation.

The project follows the [Agent Skills](https://agentskills.io) specification and supports one-click installation via `npx skills add`, compatible with 40+ agents (Claude Code, Cursor, Copilot, Gemini CLI, Windsurf, etc.).

## Architecture

### Skill Decomposition

Skills are split by language (lightweight per-load) with an optional emotion add-on:

| Skill | Responsibility | Triggers |
|-------|---------------|----------|
| **tts-chef-core** | Universal pipeline: text cleaning, Markdown/HTML removal, URL/email/path conversion, pipeline orchestration | TTS preprocessing, text cleaning, speech synthesis prep, voice synthesis |
| **tts-chef-zh** | Chinese polyphone replacement, number-to-Chinese, punctuation normalization, sentence breaking | Chinese TTS, polyphone, Chinese numbers, Chinese reading, 中文朗读, 多音字 |
| **tts-chef-en** | English abbreviation expansion, number-to-English, punctuation, symbol reading | English TTS, English abbreviation, English reading, text-to-speech English |
| **tts-chef-ja** | Japanese kanji reading rules, number-to-Japanese, particle handling | 日本語 TTS, Japanese reading, 日文朗读 |
| **tts-chef-auto** | Auto language detection, dispatch to corresponding language skill | auto detect, mixed language, unknown language, 混合语言 |
| **tts-chef-emotion** | Emotion/speaking-style annotation syntax (optional) | emotion tag, TTS emotion, speaking style, 情感标注, 语气控制 |

Base skills (core + zh/en/ja/auto) contain NO emotion logic. Users install `tts-chef-emotion` separately when needed.

### Directory Structure

```
tts-chef/
├── README.md                        # Project intro, badges, install guide, skill table
├── CLAUDE.md                        # Repo guidance for Claude Code
├── AGENTS.md                        # Repo guidance for generic agents (same content as CLAUDE.md)
├── GEMINI.md                        # Repo guidance for Gemini CLI
├── LICENSE                          # MIT
├── .github/
│   └── copilot-instructions.md      # GitHub Copilot repo-wide instructions
├── assets/
│   ├── tts-chef-logo.svg            # Project logo
│   └── tts-chef-icon.svg            # Square icon for badges/marketplace
├── scripts/
│   └── tts_preprocess.py            # Standalone executable preprocessing script
├── skills/
│   ├── llms.txt                     # Skill index for agent discovery
│   ├── tts-chef-core/
│   │   └── SKILL.md
│   ├── tts-chef-zh/
│   │   └── SKILL.md
│   ├── tts-chef-en/
│   │   └── SKILL.md
│   ├── tts-chef-ja/
│   │   └── SKILL.md
│   ├── tts-chef-auto/
│   │   └── SKILL.md
│   └── tts-chef-emotion/
│       └── SKILL.md
└── examples/
    ├── chinese-sample.txt
    ├── english-sample.txt
    └── mixed-sample.txt
```

### SKILL.md Format

Each SKILL.md follows the Agent Skills specification:

```yaml
---
name: tts-chef-core          # lowercase, hyphens, matches directory name
description: ...             # what it does + trigger terms, max 1024 chars
license: MIT
---

# Markdown body with rules, examples, do/don't
```

## Skill Content Design

### tts-chef-core

The universal preprocessing pipeline. Applies to all languages.

**Pipeline order (matter):**
1. Custom replacements (user-defined)
2. Escape character replacement (`\n` -> "换行")
3. Markdown code blocks (strip fences, keep content)
4. Inline code (strip backticks)
5. URLs -> readable text ("链接 domain.com")
6. Emails -> readable text ("user 艾特 domain.com")
7. File paths -> cleaned readable text
8. Environment variables (`$VAR`, `${VAR}`, `%VAR%`) -> lowercase with spaces
9. Code identifiers (SCREAMING_SNAKE, camelCase, PascalCase) -> split words
10. Version numbers (`v2.0.1` -> language-specific)
11. Operators (`===`, `!=`, `&&`, etc.) -> readable text
12. Numbers (language-specific, handled by language skills)
13. Symbols (`%`, `$`, `→`, etc.) -> readable text
14. Abbreviations (language-specific)
15. Language-specific rules (polyphone, etc.)
16. Markdown cleanup (headers, lists, bold/italic)
17. Punctuation cleanup
18. Whitespace cleanup

**Agent guidance:**
- Always run the pipeline in order
- For mixed-language text, detect primary language and apply that skill's rules
- The pipeline is idempotent for already-clean text
- Skip steps that don't apply (e.g., no code in a novel)

### tts-chef-zh

Chinese-specific preprocessing rules.

**Polyphone replacement table:**
- Maps ~200 common polyphone words to homophone substitutes
- Organized by pronunciation group (调tiáo, 处chǔ, 重chóng, etc.)
- Agent applies longest-match-first

**Number conversion:**
- Years: 2024年 -> 二零二四年
- Percentages: 15% -> 十五百分之
- Decimals: 3.14 -> 三点一四
- Versions: v2.0.1 -> 版本二点零点一

**Punctuation:**
- English punctuation -> Chinese punctuation (for Chinese text)
- Collapse repeated punctuation (。。。 -> 。)

**Sentence breaking:**
- Break on 。！？ followed by content
- Respect quote boundaries
- Preserve list structure

**Abbreviation expansion:**
- API -> A P I
- HTTP -> H T T P
- (Full table of ~100 tech abbreviations)

### tts-chef-en

English-specific preprocessing rules.

**Abbreviation expansion:**
- Acronyms: API -> "A P I", HTTP -> "H T T P"
- Readable abbreviations: IoT -> "I o T", NoSQL -> "No S Q L"
- Tech terms: CI/CD -> "C I C D"

**Number conversion:**
- Years: 2024 -> "twenty twenty-four"
- Decimals: 3.14 -> "three point one four"
- Percentages: 15% -> "fifteen percent"
- Ordinals: 1st -> "first", 2nd -> "second"

**Symbol reading:**
- @ -> "at"
- # -> "hash" / "number"
- / -> "slash"
- & -> "and"

**Punctuation for TTS:**
- Strip Markdown formatting
- Normalize ellipses (...) to pauses
- Handle em-dashes as sentence breaks

### tts-chef-ja

Japanese-specific preprocessing rules.

**Kanji reading guidelines:**
- Common kanji that TTS engines frequently misread
- Provide furigana hints where needed
- Handle ateji (当て字) and gikun (義訓)

**Number conversion:**
- Years: 2024年 -> にせんにじゅうよねん
- Counters: 1つ -> ひとつ, 2人 -> ふたり
- Decimal: 3.14 -> さんてんいちよん

**Particle handling:**
- は (wa) vs は (ha) disambiguation
- へ (e) vs へ (he) disambiguation

**Punctuation:**
- Normalize full-width/half-width
- Handle Japanese-specific punctuation (、。！？「」)

### tts-chef-auto

Auto language detection and dispatch.

**Detection heuristic:**
1. Count CJK characters vs Latin characters
2. If >60% CJK:
   - Check for hiragana/katakana -> Japanese
   - Otherwise -> Chinese
3. If >60% Latin -> English
4. Mixed -> apply per-sentence detection, dispatch each sentence to its language skill

**Agent guidance:**
- For short text (<50 chars), use the dominant language
- For long text, process per-paragraph or per-sentence
- When uncertain, default to the language the user is communicating in

### tts-chef-emotion

Optional emotion annotation for TTS engines that support it.

**Annotation syntax:**
```
[emotion] text [/emotion]
```

**Supported tags:**
- `[平静]` / `[/]` - neutral/calm (reset)
- `[兴奋]` - excited
- `[悲伤]` - sad
- `[惊讶]` - surprised
- `[愤怒]` - angry
- `[耳语]` - whisper
- `[强调]` - emphasis
- `[缓慢]` - slow pace
- `[快速]` - fast pace

**Agent guidance:**
- Only use when the user explicitly asks for emotion control
- Don't add emotion tags to plain text
- Match emotion to content tone (exclamation marks suggest excitement, etc.)
- Keep emotion spans short (per-sentence, not per-paragraph)
- Close tags explicitly with `[/]` to reset

**Engine compatibility notes:**
- Some engines ignore emotion tags (safe degradation)
- Provide equivalent SSML where possible
- List known compatible engines per tag

## Installation

### npx skills (recommended, supports 40+ agents)

```bash
# Install all skills
npx skills add https://github.com/<user>/tts-chef

# Install specific skill only
npx skills add https://github.com/<user>/tts-chef --skill tts-chef-zh

# Target specific agent
npx skills add https://github.com/<user>/tts-chef --agent cursor
```

### Claude Code

```bash
/plugin marketplace add <user>/tts-chef
```

### Cursor

Settings -> Rules -> Add Rule -> Remote Rule (GitHub) -> `<user>/tts-chef`

### Manual / Clone

Copy `skills/` folder to the agent's skill directory:

| Agent | Directory |
|-------|-----------|
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |
| OpenCode | `~/.config/opencode/skills/` |
| OpenAI Codex | `~/.codex/skills/` |
| Gemini CLI | `~/.gemini/skills/` |
| GitHub Copilot | `.github/copilot-instructions.md` |

## Script Tool

`scripts/tts_preprocess.py` is a standalone Python script that agents can invoke directly.

**Usage:**
```bash
# Process a file
python tts_preprocess.py input.txt

# With output file
python tts_preprocess.py -i in.txt -o out.txt

# Pipe input
echo "调试代码" | python tts_preprocess.py -

# Custom rules
python tts_preprocess.py input.txt --rules custom_rules.json

# Dry-run (show diff)
python tts_preprocess.py input.txt --dry-run
```

Agents should prefer implementing rules directly in code (from SKILL.md knowledge), but can fall back to invoking the script for complex preprocessing.

## Examples

Three example files demonstrating before/after preprocessing for each language, included in `examples/`.

## Risk Level

**LOW** - Text preprocessing only. No code execution, no network access, no file system writes beyond output.

## License

MIT
