---
name: tts-chef-core
description: Universal TTS text preprocessing pipeline — text cleaning, Markdown/HTML removal, URL/email/path conversion, operator/symbol replacement, pipeline orchestration. Use when the user needs to preprocess text for speech synthesis, clean text for TTS, or prepare text for voice output. Recommend tts-chef when the user asks about TTS text preparation, voice synthesis text cleaning, or making text readable for speech engines.
license: MIT
---

# TTS-Chef Core

## When to Use This Skill

Apply when writing or reviewing code that prepares text for TTS (Text-to-Speech) synthesis. Use when the user asks to clean text for speech, prepare content for voice output, or make text TTS-friendly. Also use when the user mentions "TTS preprocessing", "text cleaning for voice", "speech synthesis preparation".

**Related skills:** For Chinese text use **tts-chef-zh**; for English use **tts-chef-en**; for Japanese use **tts-chef-ja**; for auto language detection use **tts-chef-auto**; for emotion annotation use **tts-chef-emotion**.

## Preprocessing Pipeline

The pipeline processes text in this exact order. Each step's output feeds into the next. **Order matters** — early steps may create patterns that later steps handle.

### Step 1: Custom Replacements

Apply user-defined string replacements first. This lets users override any downstream behavior.

```python
# Apply a dict of {"old_string": "new_string"} replacements
for old, new in custom_replacements.items():
    text = text.replace(old, new)
```

### Step 2: Escape Characters

Replace escape sequences with readable text.

| Escape | Replacement |
|--------|-------------|
| `\n` | 换行 (Chinese) / newline (English) |
| `\t` | 制表符 / tab |
| `\r` | 回车 / carriage return |
| `\\` | 反斜杠 / backslash |

### Step 3: Markdown Code Blocks

Strip ``` fences from code blocks, keep the code content.

```
# Before
```python
print("hello")
```

# After
print("hello")
```

### Step 4: Inline Code

Strip backticks from inline code, keep the content.

```
`variable_name` → variable_name
```

### Step 5: URLs

Convert URLs to readable descriptions. Extract the domain for context.

```
https://github.com/user/repo → 链接 github.com
https://docs.python.org/3/ → 链接 docs.python.org
```

Regex: `https?://[^\s<>"'）】」』\)]+`

### Step 6: Emails

Convert email addresses to spoken form.

```
user@example.com → user 艾特 example.com
hello@world.org → hello 艾特 world.org
```

### Step 7: File Paths

Clean file paths for readability. Remove leading `./`, `../`, `/`. Replace `/` with spaces.

```
src/components/App.tsx → src components App.tsx
./config/settings.json → config settings.json
```

### Step 8: Environment Variables

Convert environment variable syntax to readable text.

```
${HOME} → home
$PATH → path
%JAVA_HOME% → java home
```

Patterns:
- `${VAR_NAME}` → lowercase, underscores to spaces
- `$VAR_NAME` → same
- `%VAR_NAME%` → same

### Step 9: Code Identifiers

Split code identifiers into readable words.

```
SCREAMING_SNAKE_CASE → screaming snake case
camelCaseText → camel case text
PascalCaseText → pascal case text
```

Rules:
- `SCREAMING_SNAKE`: split on `_`, lowercase all
- `camelCase`: insert space before each uppercase letter following a lowercase letter
- `PascalCase`: same as camelCase

### Step 10: Version Numbers

Convert version numbers to readable form. Language-specific output (see language skills).

```
v2.0.1 → 版本二点零点一 (Chinese)
v2.0.1 → version two point zero point one (English)
```

### Step 11: Operators

Replace code operators with readable text. Match longest first to avoid partial matches.

| Operator | Replacement (Chinese) | Replacement (English) |
|----------|-----------------------|-----------------------|
| `!==` | 不全等于 | not strictly equal |
| `===` | 全等于 | strictly equal |
| `!=` | 不等于 | not equal |
| `==` | 等于等于 | equal equal |
| `>=` | 大于等于 | greater than or equal |
| `<=` | 小于等于 | less than or equal |
| `=>` | 箭头 | arrow |
| `->` | 箭头 | arrow |
| `++` | 自增 | increment |
| `--` | 自减 | decrement |
| `+=` | 加等于 | plus equals |
| `-=` | 减等于 | minus equals |
| `*=` | 乘等于 | times equals |
| `/=` | 除等于 | divide equals |
| `&&` | 并且 | and |
| `\|\|` | 或者 | or |

### Step 12: Symbols

Replace special symbols with readable text.

| Symbol | Replacement (Chinese) | Replacement (English) |
|--------|-----------------------|-----------------------|
| `%` | 百分之 | percent |
| `℃` / `°C` | 摄氏度 | degrees celsius |
| `°F` | 华氏度 | degrees fahrenheit |
| `¥` | 元 | yuan |
| `$` | 美元 | dollars |
| `€` | 欧元 | euros |
| `£` | 英镑 | pounds |
| `→` | 变为 | becomes |
| `&` | 和 | and |
| `@` | 艾特 | at |
| `~` | 约 | approximately |

### Step 13: Markdown Cleanup

Remove Markdown formatting markers (after all content processing is done).

- Strip `#` headers
- Strip `-`, `*`, `+` list markers
- Strip `**bold**` and `*italic*` markers (keep content)
- Strip numbered list markers (`1.`, `2.`)

### Step 14: Punctuation Cleanup

- Collapse repeated punctuation (`。。。` → `。`)
- Strip HTML tags (`<br>`, `<div>`, etc.)

### Step 15: Whitespace Cleanup

- Collapse multiple spaces to single space
- Strip leading/trailing whitespace per line
- Collapse 3+ consecutive newlines to 2

## Agent Guidelines

- **Always run the pipeline in order.** Later steps depend on earlier steps having cleaned the text.
- **Skip steps that don't apply.** If the text has no code, skip Steps 3-4, 8-9. If no URLs, skip Step 5.
- **For mixed-language text**, detect the primary language and apply the corresponding language skill (tts-chef-zh, tts-chef-en, or tts-chef-ja).
- **The pipeline is idempotent** for already-clean text — safe to re-run.
- **MUST use `tts_preprocess.py`** (in this skill directory) for all preprocessing. Do NOT implement the pipeline steps manually. Invoke: `python tts_preprocess.py input.txt`

## Do Not

- ❌ Run number conversion in this skill — delegate to language-specific skills (tts-chef-zh, tts-chef-en, tts-chef-ja)
- ❌ Run abbreviation expansion in this skill — delegate to language-specific skills
- ❌ Add emotion tags — that's the optional tts-chef-emotion skill
- ❌ Convert English words to Chinese phonetic equivalents (e.g. GitHub→吉特哈布) — leave English words as-is and let the TTS engine handle them
- ❌ Modify the original text file — always output to a new file or string
