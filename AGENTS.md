# Guidance for AI Agents Working in This Repo

This repository contains **tts-chef** skills for AI coding agents — TTS text preprocessing skills that teach agents how to clean, normalize, and prepare text for speech synthesis.

## Repo structure

- **skills/** — Each subdirectory is one skill. The CLI and agents discover skills by scanning `skills/` for directories that contain `SKILL.md`.
- **Skill directory name** must exactly match the `name` in that skill's frontmatter (e.g. `skills/tts-chef-core/` ↔ `name: tts-chef-core`).
- **scripts/tts_preprocess.py** — Standalone Python script that agents can invoke for complex preprocessing.

## SKILL.md requirements

- **Frontmatter (YAML):**
  - `name` (required): lowercase, hyphens only, max 64 chars, must match parent directory name.
  - `description` (required): what the skill does and when to use it; include trigger terms so agents know when to apply it. Max 1024 chars.
  - `license` (optional): e.g. `MIT` if the skill is under the repo license.
- **Body:** Markdown instructions. Keep under ~500 lines; put long reference material in `references/` and link from SKILL.md.

## Conventions

- Write descriptions in **third person** (e.g. "Use when…" not "You can use when…").
- Be concise; focus on rules, pitfalls, and correct usage.
- When adding a new skill: create `skills/<skill-name>/SKILL.md`, then update README.md "Skills" table and "Structure" section.

## References

- [Agent Skills specification](https://agentskills.io/specification.md)
- [skills CLI (discovery, install)](https://github.com/vercel-labs/skills)
