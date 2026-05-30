[**English**](README.md)

---

<div align="center">

# 🎧 TTS-Chef

**AI Agent 技能 — TTS 文本预处理**

教会你的 AI 代理如何清洗、规范和准备语音合成文本。

[![Claude Skill](https://img.shields.io/badge/Claude-Skill-purple)](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills)
[![Cursor Compatible](https://img.shields.io/badge/Cursor-Compatible-blue)](https://docs.cursor.com/context/rules)
[![Copilot Ready](https://img.shields.io/badge/Copilot-Ready-green)](https://docs.github.com/en/copilot)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

</div>

---

## 功能介绍

在将文本送入 TTS 引擎之前，需要预处理才能让朗读听起来自然：

- **多音字替换** — 修复 TTS 常见误读词（调试→条试）
- **数字转换** — 数字转口语音读法（v2.0.1→版本二点零点一）
- **缩写展开** — 拼读英文缩写（API→A P I）
- **文本清洗** — 去除 Markdown、HTML、URL、代码语法
- **情感标注** — 可选的语气标签，控制语音情感（[兴奋] 你好 [/]）
- **多语言** — 支持中文、英文、日文

## 安装

### npx skills（推荐）

支持 Claude Code、Cursor、Copilot、Windsurf、Gemini CLI 等 [40+ 代理](https://github.com/vercel-labs/skills#supported-agents)：

```bash
npx skills add https://github.com/clear2x/tts-chef
```

指定目标代理：

```bash
npx skills add https://github.com/clear2x/tts-chef --agent cursor
```

### Claude Code

```bash
/plugin marketplace add clear2x/tts-chef
```

### Cursor

**Settings → Rules → Add Rule → Remote Rule (GitHub)**，输入 `clear2x/tts-chef`。

### 手动安装

将 `skills/` 文件夹复制到你代理的技能目录：

| 代理 | 目录 |
|------|------|
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |
| OpenCode | `~/.config/opencode/skills/` |
| OpenAI Codex | `~/.codex/skills/` |
| Gemini CLI | `~/.gemini/skills/` |

## 技能列表

| 技能 | 说明 |
|------|------|
| **tts-chef-core** | 通用管道：文本清洗、Markdown/HTML 去除、URL/邮箱/路径转换 |
| **tts-chef-zh** | 中文：多音字替换（~200 词）、数字转中文、标点、断句 |
| **tts-chef-en** | 英文：缩写展开、数字转英文、符号朗读 |
| **tts-chef-ja** | 日文：汉字注音、数字转日文、助词消歧 |
| **tts-chef-auto** | 自动语言检测，调度对应的语言技能 |
| **tts-chef-emotion** | 可选的情感/语气标注，控制 TTS 语音表现力 |

## 快速示例

预处理前：
```
# 2024年回顾

我们的API支持HTTPS协议，下载量增长了150%！
调试时，请检查 `${HOME}/.config` 路径下的配置文件。
```

预处理后（中文）：
```
二零二四年回顾

我们的 A P I 支持 H T T P S 协议，下在量增长了百分之一百五！
条试时，请检查 home .config 路径下的配置文件。
```

## 独立脚本

不依赖 AI 代理，可直接使用：

```bash
# 处理文件
python scripts/tts_preprocess.py input.txt

# 管道输入
echo "调试代码" | python scripts/tts_preprocess.py -

# 查看前后对比
python scripts/tts_preprocess.py input.txt --dry-run

# 自定义规则
python scripts/tts_preprocess.py input.txt --rules custom_rules.json
```

## 项目结构

```
tts-chef/
  README.md                # 英文文档
  README.zh-CN.md          # 中文文档（本文件）
  CLAUDE.md                # Claude Code 仓库指引
  AGENTS.md                # 通用代理仓库指引
  GEMINI.md                # Gemini CLI 仓库指引
  LICENSE
  .github/
    copilot-instructions.md
  assets/
    tts-chef-logo.svg
    tts-chef-icon.svg
  scripts/
    tts_preprocess.py      # 独立 Python 工具
  skills/
    llms.txt               # 技能索引（代理发现用）
    tts-chef-core/         SKILL.md
    tts-chef-zh/           SKILL.md
    tts-chef-en/           SKILL.md
    tts-chef-ja/           SKILL.md
    tts-chef-auto/         SKILL.md
    tts-chef-emotion/      SKILL.md
  examples/
    chinese-sample.txt
    english-sample.txt
    mixed-sample.txt
```

## 风险等级

**低** — 仅文本预处理，无代码执行、无网络访问、无文件写入。

## 许可证

MIT
