# Operational Rules for Claude Code

These rules ensure safe, predictable development inside this Django project.

## Editing Rules
- ALWAYS output unified diffs.
- NEVER rewrite full files unless newly created.
- Ask for file contents before modifying.
- Keep changes scoped and reversible.

## Structural Rules
- Follow architecture.md as the source of truth.
- Follow Premium Legal UI patterns already established.
- Do not alter IA (site structure) without explicit instruction.
- Do not remove or rename CMS components.

## AI Prompt Rules
- All prompt text belongs in /ai/prompts.
- Do not duplicate prompts across code.
- Ask for confirmation before altering any system-level prompt.

## Booking System Rules
- Treat booking logic as modular and non-destructive.
- Ask before introducing new models or migrations.

## Deployment Rules
- Never touch production settings without explicit command.
- Maintain compatibility with Render (Procfile, build.sh, env vars).

## Behaviour Summary
- Be predictable.
- Be safe.
- Be explicit.
- Never assume.
- Never refactor without permission.
