---
name: tts-chef-emotion
description: Optional emotion and speaking-style annotation for TTS — adds emotion tags like [兴奋], [悲伤], [耳语] to control TTS engine tone and pace. Only use when the user explicitly requests emotion control, speaking style, or tone adjustment for TTS output. Provides SSML equivalents where applicable.
license: MIT
---

# TTS-Chef Emotion Annotation

## When to Use This Skill

Apply **only** when the user explicitly requests emotion control or speaking-style adjustment for TTS output. Do not add emotion tags to plain text without user request.

**This is an optional add-on skill.** The base skills (tts-chef-core, tts-chef-zh, tts-chef-en, tts-chef-ja) do NOT include emotion annotation.

## Annotation Syntax

Use square brackets to mark emotion/style regions:

```
[emotion] text content [/]
```

The `[/]` tag resets to the default (neutral) voice.

## Supported Tags

### Emotion Tags

| Tag | Effect | SSML Equivalent |
|-----|--------|-----------------|
| `[平静]` | Neutral, calm voice | `<prosody rate="default" pitch="default">` |
| `[兴奋]` | Excited, higher pitch, faster | `<prosody rate="fast" pitch="high">` |
| `[悲伤]` | Sad, lower pitch, slower | `<prosody rate="slow" pitch="low">` |
| `[惊讶]` | Surprised, elevated pitch | `<prosody rate="default" pitch="high" volume="loud">` |
| `[愤怒]` | Angry, forceful, louder | `<prosody rate="fast" pitch="low" volume="loud">` |
| `[耳语]` | Whispered, soft | `<prosody volume="soft">` |

### Style Tags

| Tag | Effect | SSML Equivalent |
|-----|--------|-----------------|
| `[强调]` | Emphasize the enclosed text | `<emphasis level="strong">` |
| `[缓慢]` | Slow speaking pace | `<prosody rate="slow">` |
| `[快速]` | Fast speaking pace | `<prosody rate="fast">` |

### Reset Tag

| Tag | Effect |
|-----|--------|
| `[/]` | Reset to default (neutral) voice |

## Usage Examples

### Single Emotion

```
[兴奋] 我们终于发布了新版本！ [/]
```

### Mixed Emotions

```
[平静] 今天的天气还不错。 [/]
[兴奋] 但是明天要下雪了！ [/]
[耳语] 据说会很大。 [/]
```

### Nested Style (emphasis inside emotion)

```
[兴奋] 这个功能 [强调] 非常 [/] 强大！ [/]
```

### Long Text with Emotion Shifts

```
[平静] 2024年，我们的团队经历了许多挑战。 [/]
[悲伤] 有几位同事离开了公司。 [/]
[兴奋] 但我们也迎来了新的伙伴，一起攻克了难关！ [/]
[平静] 回顾过去，我们成长了很多。 [/]
```

## Agent Guidelines

### Preprocessing Prerequisite

- **MUST run `python scripts/tts_preprocess.py`** on the text BEFORE adding emotion tags. Emotion annotation applies to already-preprocessed text.

### When to Add Emotion Tags

- **Only when the user asks** for emotion/style control
- When the user describes desired tone: "read this enthusiastically", "make it sound sad", "whisper this part"
- When the user provides a script with stage directions

### How to Choose Emotion Tags

| Content Signal | Suggested Tag |
|---------------|---------------|
| Exclamation marks + positive words | `[兴奋]` |
| Loss, departure, negative events | `[悲伤]` |
| Unexpected outcomes, surprises | `[惊讶]` |
| Criticism, conflict | `[愤怒]` |
| Secrets, private thoughts | `[耳语]` |
| Key points, conclusions | `[强调]` |
| Complex explanations | `[缓慢]` |
| Lists, rapid-fire items | `[快速]` |
| Default narration | `[平静]` or no tag |

### Tag Placement Rules

1. **Keep emotion spans short** — per-sentence, not per-paragraph
2. **Always close tags** — use `[/]` to reset to neutral
3. **Don't stack emotions** — only one active emotion at a time
4. **Reset between sections** — don't let emotions bleed across paragraphs

### What NOT to Do

- ❌ Don't add emotion tags to plain text without user request
- ❌ Don't nest same-type tags: `[兴奋] [兴奋] text [/] [/]`
- ❌ Don't leave unclosed tags
- ❌ Don't use emotion tags as replacement for good punctuation
- ❌ Don't apply emotion to every sentence — only where tone differs from neutral

## Engine Compatibility

| Engine | Emotion Support | Notes |
|--------|----------------|-------|
| Azure TTS | Via SSML | Convert tags to `<prosody>` / `<emphasis>` SSML |
| Google Cloud TTS | Via SSML | Convert tags to `<prosody>` SSML |
| Amazon Polly | Via SSML | Convert tags to `<prosody>` SSML |
| Edge TTS | Limited | Some engines support style tags |
| OpenAI TTS | None | Tags will be ignored (safe degradation) |
| Local TTS (e.g., Coqui) | Varies | Depends on model |
| XTTS / ChatTTS | Varies | Some models support emotion via conditioning |

**Safe degradation:** If an engine doesn't support emotion tags, the tags are simply ignored. The text is still read correctly, just without the emotional variation.

## Converting to SSML

For engines that require SSML, convert the bracket notation:

```
[兴奋] Hello world [/]
```

becomes:

```xml
<speak>
  <prosody rate="fast" pitch="high">Hello world</prosody>
</speak>
```

### Conversion Table

```
[平静]  → <prosody rate="default" pitch="default">
[兴奋]  → <prosody rate="fast" pitch="high">
[悲伤]  → <prosody rate="slow" pitch="low">
[惊讶]  → <prosody rate="default" pitch="high" volume="loud">
[愤怒]  → <prosody rate="fast" pitch="low" volume="loud">
[耳语]  → <prosody volume="soft">
[强调]  → <emphasis level="strong">
[缓慢]  → <prosody rate="slow">
[快速]  → <prosody rate="fast">
[/]     → closing tag (</prosody> or </emphasis>)
```
