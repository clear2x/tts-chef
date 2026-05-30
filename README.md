<div align="center">

# 🎧 TTS-Chef

**AI Agent Skills for TTS Text Preprocessing**

Teach your AI agent how to clean, normalize, and prepare text for speech synthesis.

[![Claude Skill](https://img.shields.io/badge/Claude-Skill-purple)](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills)
[![Cursor Compatible](https://img.shields.io/badge/Cursor-Compatible-blue)](https://docs.cursor.com/context/rules)
[![Copilot Ready](https://img.shields.io/badge/Copilot-Ready-green)](https://docs.github.com/en/copilot)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

</div>

---

## What It Does

Before sending text to a TTS engine, the text needs preprocessing to sound natural:

- **多音字替换** — Fix commonly mispronounced Chinese words (调试→条试)
- **数字转换** — Convert numbers to spoken form (v2.0.1→版本二点零点一)
- **缩写展开** — Spell out abbreviations (API→A P I)
- **文本清洗** — Remove Markdown, HTML, URLs, code syntax
- **情感标注** — Optional emotion tags for expressive speech ([兴奋] hello [/])
- **多语言** — Support for Chinese, English, and Japanese

## Installing

### npx skills (recommended)

Works with Claude Code, Cursor, Copilot, Windsurf, Gemini CLI, and [40+ agents](https://github.com/vercel-labs/skills#supported-agents):

```bash
npx skills add https://github.com/clear2x/tts-chef
```

Target a specific agent:

```bash
npx skills add https://github.com/clear2x/tts-chef --agent cursor
```

### Claude Code

```bash
/plugin marketplace add clear2x/tts-chef
```

### Cursor

**Settings → Rules → Add Rule → Remote Rule (GitHub)** and use `clear2x/tts-chef`.

### Manual

Copy the `skills/` folder into your agent's skill directory:

| Agent | Directory |
|-------|-----------|
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |
| OpenCode | `~/.config/opencode/skills/` |
| OpenAI Codex | `~/.codex/skills/` |
| Gemini CLI | `~/.gemini/skills/` |

## Skills

| Skill | Description |
|-------|-------------|
| **tts-chef-core** | Universal pipeline: text cleaning, Markdown/HTML removal, URL/email/path conversion |
| **tts-chef-zh** | Chinese: polyphone replacement (~200 words), number-to-Chinese, punctuation, sentence breaking |
| **tts-chef-en** | English: abbreviation expansion, number-to-English, symbol reading |
| **tts-chef-ja** | Japanese: kanji reading, number-to-Japanese, particle disambiguation |
| **tts-chef-auto** | Auto language detection, dispatch to the right language skill |
| **tts-chef-emotion** | Optional emotion/speaking-style annotation for expressive TTS |

## Quick Example

Before:
```
# 2024年回顾

我们的API支持HTTPS协议，下载量增长了150%！
调试时，请检查 `${HOME}/.config` 路径下的配置文件。
```

After (Chinese):
```
二零二四年回顾

我们的 A P I 支持 H T T P S 协议，下在量增长了百分之一百五！
条试时，请检查 home .config 路径下的配置文件。
```

## Standalone Script

For use outside of AI agents:

```bash
# Process a file
python scripts/tts_preprocess.py input.txt

# Pipe input
echo "调试代码" | python scripts/tts_preprocess.py -

# Show before/after diff
python scripts/tts_preprocess.py input.txt --dry-run

# Custom rules
python scripts/tts_preprocess.py input.txt --rules custom_rules.json
```

## Structure

```
tts-chef/
  README.md
  CLAUDE.md              # Agent repo guidance (Claude Code)
  AGENTS.md              # Agent repo guidance (generic agents)
  GEMINI.md              # Agent repo guidance (Gemini CLI)
  LICENSE
  .github/
    copilot-instructions.md
  assets/
    tts-chef-logo.svg
    tts-chef-icon.svg
  scripts/
    tts_preprocess.py    # Standalone Python tool
  skills/
    llms.txt             # Skill index for agent discovery
    tts-chef-core/       SKILL.md
    tts-chef-zh/         SKILL.md
    tts-chef-en/         SKILL.md
    tts-chef-ja/         SKILL.md
    tts-chef-auto/       SKILL.md
    tts-chef-emotion/    SKILL.md
  examples/
    chinese-sample.txt
    english-sample.txt
    mixed-sample.txt
```

## Risk Level

**LOW** — Text preprocessing only. No code execution, no network access, no file system writes beyond output.

## License

MIT
