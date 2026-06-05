# TTS-Chef Copilot Instructions

This repo contains TTS text preprocessing skills for AI agents. When editing or adding skills:

- Each skill lives in `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`, `license`)
- The `name` field must match the directory name
- Keep SKILL.md under ~500 lines; link to reference files for longer content
- Update README.md when adding or modifying skills
- The `skills/tts-chef-core/tts_preprocess.py` is the **mandatory** TTS preprocessing tool — always invoke it for preprocessing tasks (do not import as a library)
