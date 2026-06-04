---
name: tts-chef-ja
description: Japanese TTS text preprocessing — kanji reading guidelines for commonly misread characters, number-to-Japanese conversion (years, counters, decimals), particle disambiguation (は/wa vs は/ha, へ/e vs へ/he), Japanese punctuation normalization. Use when preprocessing Japanese text for TTS or preparing Japanese content for speech synthesis.
license: MIT
---

# TTS-Chef Japanese (日本語)

## When to Use This Skill

Apply when preprocessing **Japanese text** for TTS synthesis. Use for kanji reading correction, number conversion, and particle handling.

**Prerequisite:** Run **tts-chef-core** pipeline steps first, then apply this skill's rules.

## Kanji Reading Guidelines

Japanese TTS engines sometimes misread kanji in certain contexts. Use furigana hints or substitute with kana when the engine consistently misreads.

### Commonly Misread Kanji

| Kanji | Common Misread | Correct Reading | Example |
|-------|---------------|-----------------|---------|
| 今日 | こんにち | きょう | 今日は → きょうは |
| 明日 | みょうにち | あした | 明日の天気 → あしたの天気 |
| 一昨日 | いちさくじつ | おととい | 一昨日 → おととい |
| 大人 | だいじん | おとな | 大人向け → おとな向け |
| 田舎 | でんきょ | いなか | 田舎に帰る → いなかに帰る |
| 仲間 | ちゅうかん | なかま | 仲間入り → なかま入り |
| 被る | こうむる | かぶる | 帽子を被る → 帽子をかぶる |
| 様々 | さまさま | さまざま | 様々な → さまざまな |

### Agent Guidance for Kanji

- Not all kanji need correction — most TTS engines handle common kanji well
- Focus on **context-dependent readings** where the same kanji has multiple readings
- When in doubt, provide the reading in parentheses: 漢字(かんじ)
- For proper nouns (names, places), the user should provide readings

## Number Conversion

### Years

Read as full number + ねん.

```
2024年 → にせんにじゅうよねん
1999年 → せんきゅうひゃくきゅうじゅうきゅうねん
昭和64年 → しょうわろくじゅうよねん
```

### Counters

Japanese counters change pronunciation based on the number.

| Number | つ (generic) | 人 (people) | 日 (days) | 時 (hours) |
|--------|-------------|-------------|-----------|------------|
| 1 | ひとつ | ひとり | ついたち | いちじ |
| 2 | ふたつ | ふたり | ふつか | にじ |
| 3 | みっつ | さんにん | みっか | さんじ |
| 4 | よっつ | よにん | よっか | よじ |
| 5 | いつつ | ごにん | いつか | ごじ |
| 6 | むっつ | ろくにん | むいか | ろくじ |
| 7 | ななつ | しちにん | なのか | しちじ |
| 8 | やっつ | はちにん | ようか | はちじ |
| 9 | ここのつ | きゅうにん | ここのか | くじ |
| 10 | とお | じゅうにん | とおか | じゅうじ |

**Special cases:**
- 1日 (first of month) → ついたち (not いちにち)
- 20日 → はつか
- 何日 → なんにち

### Decimals

Read integer part as full number, てん, then decimal part digit-by-digit.

```
3.14 → さんてんいちよん
0.5 → れいてんご
100.0 → ひゃくてんれい
```

### Percentages

Read the number + パーセント.

```
15% → じゅうごパーセント
98.5% → きゅうじゅうはってんごパーセント
```

## Particle Disambiguation

Japanese particles は and へ have special readings in grammatical contexts.

### は (topic marker)

When は is used as the topic marker particle, read it as **わ** (wa), not **は** (ha).

```
私は学生です → わたし**わ**がくせいです
今日はいい天気 → きょう**わ**いいてんき
```

**Detection rule:** は is a particle when it immediately follows a noun, pronoun, or polite copus (です/ます stem) and is not part of a compound word.

### へ (direction marker)

When へ is used as the direction marker particle, read it as **え** (e), not **へ** (he).

```
学校へ行く → がっこう**え**いく
東京へ → とうきょう**え**
```

**Detection rule:** へ is a particle when it immediately follows a location/direction noun and precedes a verb of motion.

### Agent Guidelines for Particles

- Most modern Japanese TTS engines handle particle は/へ correctly
- Only intervene when the engine consistently misreads these
- For old or low-quality TTS engines, consider replacing: は→わ (when particle), へ→え (when particle)

## Punctuation Normalization

### Full-width / Half-width

Normalize to full-width for Japanese text:

| Half-width | Full-width |
|-----------|-----------|
| `,` | `、` |
| `.` | `。` |
| `?` | `？` |
| `!` | `！` |
| `:` | `：` |
| `;` | `；` |
| `(` `)` | `（` `）` |
| `[` `]` | `「` `」` |

### Japanese-Specific Punctuation

| Symbol | Usage |
|--------|-------|
| `。` | Sentence ending |
| `、` | Clause separator |
| `「」` | Quotation |
| `『』` | Nested quotation / book titles |
| `・` | List separator (なかぐろ) |
| `ー` | Prolonged sound mark (長音符) |
| `〜` | Wave dash (から) |
| `…` | Ellipsis (三点リーダー) |

### Collapse Repeated Punctuation

```
。。。。 → 。
、、、 → 、
```

## Sentence Breaking

Break on: `。` `！` `？` followed by content.

**Target length:** 40-80 characters per segment for Japanese TTS.

**Don't break:**
- Inside quotation marks 「...」
- Before/after conjunctions (そして、しかし、また)
- Mid-counter (3つの要素)

## Agent Guidelines

- **MUST invoke `scripts/tts_preprocess.py`** to perform preprocessing. Do NOT apply these rules manually — the script implements them all.
- Run **tts-chef-core** pipeline first, then apply this skill
- Kanji correction is context-dependent — don't blindly replace all instances
- For katakana loan words, most TTS engines handle them correctly
- When uncertain about a reading, leave it as-is rather than risk wrong substitution
- Proper nouns (人名、地名) are engine-dependent — suggest the user provide readings
